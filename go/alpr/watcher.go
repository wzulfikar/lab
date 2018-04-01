package alprgo

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"

	"github.com/pkg/errors"
	fsnotify "gopkg.in/fsnotify.v1"
)

type AlprHandler interface {
	Handle(imagePath string, alprResult *AlprResult, err error)
}

func Watch(path string, handler AlprHandler) error {
	if path == "" {
		return errors.New("path can't be empty")
	}

	fmt.Println("alprwatcher started. Watching " + path)

	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		return errors.Wrap(err, "NewWatcher")
	}
	defer watcher.Close()

	done := make(chan bool)
	go func() {
		for {
			select {
			case event := <-watcher.Events:
				// log.Println("event:", event.Name, event.Op)
				if event.Op == event.Op&fsnotify.Create && event.Name != ".DS_Store" {
					go func(imagePath string) {
						log.Println("new file:", imagePath)

						r := &AlprResult{}
						err := r.From(imagePath, "-c", "eu")
						handler.Handle(imagePath, r, err)
					}(event.Name)
				}
			case err := <-watcher.Errors:
				log.Fatal("watcher.Errors", err)
			}
		}
	}()
	err = watcher.Add(path)
	if err != nil {
		return errors.Wrap(err, "watcher.Add")
	}
	<-done

	return nil
}

const processedImagesPath = "processed"

type DefaultAlprHandler struct{}

func (h *DefaultAlprHandler) Handle(imagePath string, alprResult *AlprResult, err error) {
	if err != nil {
		fmt.Println("alprResultErr:", err)
		return
	}

	var plates []string
	minConfidence := 85.0
	hit := "HIT"

	for _, result := range alprResult.Results {
		for i, candidate := range result.Candidates {
			if candidate.Confidence > minConfidence && i < 3 {
				plates = append(plates, candidate.Plate)
			}
		}
	}

	if len(plates) == 0 {
		fmt.Println("No license detected")
		hit = "MISS"
	} else {
		fmt.Println(plates)
	}

	// move processed image
	path := filepath.Dir(imagePath)
	imageFile := filepath.Base(imagePath)

	ts := time.Now().Format("2006-01-02-150405")
	processedImage := fmt.Sprintf("%s-%s__%s", ts, hit, imageFile)

	processedPath := fmt.Sprintf("%s/%s/%s", path, processedImagesPath, processedImage)
	err = os.Rename(imagePath, processedPath)
	if err != nil {
		log.Println("moveProcessedImageErr:", err)
	}
}
