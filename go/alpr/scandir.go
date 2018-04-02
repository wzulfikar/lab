package alprgo

import (
	"fmt"
	"io/ioutil"
	"path/filepath"
)

func ScanDir(dir string, h AlprHandlerInterface) error {
	files, err := ioutil.ReadDir(dir)
	if err != nil {
		return err
	}

	for _, f := range files {
		if !f.IsDir() && f.Name() != ".DS_Store" {
			fmt.Printf("Found: %s\n", f.Name())
			h.Handle(filepath.Join(dir, f.Name()))
		}
	}
	return nil
}
