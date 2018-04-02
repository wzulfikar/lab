package alprgo

import (
	"fmt"
	"log"

	"github.com/pkg/errors"
	fsnotify "gopkg.in/fsnotify.v1"
)

type AlprHandlerInterface interface {
	Handle(imagePath string)
}

func Watch(path string, handler AlprHandlerInterface) error {
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
						handler.Handle(imagePath)
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
