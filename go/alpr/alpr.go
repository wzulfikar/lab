package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/pkg/errors"
	fsnotify "gopkg.in/fsnotify.v1"
)

const processedImagesPath = "processed"

func main() {
	path := os.Getenv("ALPR_PATH")

	// TODO: walk thru unprocessed files
	// o, err := exec_cmd("alpr -c eu -j /data/bab15-ok-alpr.jpeg")
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// fmt.Printf("%s", o)
	alprWatcher(path, handleAlpr)

	// license := spew.Dump(alprResult.Results)
}

func handleAlpr(imagePath string, alprResult *AlprResult, err error) {
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
	// spew.Dump(alprResult)
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

func exec_cmd(cmd string, args ...string) ([]byte, error) {
	parts := strings.Fields(cmd)
	head := parts[0]
	parts = parts[1:]

	if len(args) > 0 {
		parts = append(parts, args...)
	}

	return exec.Command(head, parts...).Output()
}

func alpr(imagePath string) (*AlprResult, error) {
	cmd := `/usr/bin/alpr -c eu -j`
	log.Println("Processing image: " + cmd + " " + imagePath)

	bytes, err := exec_cmd(cmd, imagePath)
	if err != nil {
		return nil, err
	}

	result := &AlprResult{}
	if err := json.Unmarshal(bytes, result); err != nil {
		return nil, errors.Wrap(err, "json")
	}

	return result, nil
}

// generated from https://mholt.github.io/json-to-go/
type AlprResult struct {
	Version           int     `json:"version"`
	DataType          string  `json:"data_type"`
	EpochTime         int64   `json:"epoch_time"`
	ImgWidth          int     `json:"img_width"`
	ImgHeight         int     `json:"img_height"`
	ProcessingTimeMs  float64 `json:"processing_time_ms"`
	RegionsOfInterest []struct {
		X      int `json:"x"`
		Y      int `json:"y"`
		Width  int `json:"width"`
		Height int `json:"height"`
	} `json:"regions_of_interest"`
	Results []struct {
		Plate            string  `json:"plate"`
		Confidence       float64 `json:"confidence"`
		MatchesTemplate  int     `json:"matches_template"`
		PlateIndex       int     `json:"plate_index"`
		Region           string  `json:"region"`
		RegionConfidence int     `json:"region_confidence"`
		ProcessingTimeMs float64 `json:"processing_time_ms"`
		RequestedTopn    int     `json:"requested_topn"`
		Coordinates      []struct {
			X int `json:"x"`
			Y int `json:"y"`
		} `json:"coordinates"`
		Candidates []struct {
			Plate           string  `json:"plate"`
			Confidence      float64 `json:"confidence"`
			MatchesTemplate int     `json:"matches_template"`
		} `json:"candidates"`
	} `json:"results"`
}

func alprWatcher(path string, handleAlpr func(string, *AlprResult, error)) {
	fmt.Println("alprWatcher started. Watching " + path)

	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		log.Fatal(err, "fsnotify.NewWatcher")
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
						result, err := alpr(imagePath)
						handleAlpr(imagePath, result, err)
					}(event.Name)
				}
			case err := <-watcher.Errors:
				log.Println("watcher.Errors:", err)
			}
		}
	}()
	err = watcher.Add(path)
	if err != nil {
		log.Fatal("wacher.Add", err)
	}
	<-done
}
