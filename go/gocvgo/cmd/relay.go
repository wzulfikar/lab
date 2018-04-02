package main

import (
	"fmt"
	"image/color"
	"log"
	"os"

	"github.com/wzulfikar/lab/go/gocvgo"
	"gocv.io/x/gocv"
)

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Usage:\n\trelay {classifierfile} {videourl}")
		return
	}

	// prepare classifier
	fd, err := gocvgo.NewFaceDetector(os.Args[1], color.RGBA{0, 0, 255, 0})
	if err != nil {
		log.Fatal(err)
	}
	defer fd.Close()

	url := os.Args[2]
	log.Println("Opening video at", url)
	v, err := gocv.VideoCaptureFile(url)
	if err != nil {
		fmt.Printf("error opening video capture file: %v\n", url)
		return
	}
	defer v.Close()
	relay(v, url, fd)
}

func relay(video *gocv.VideoCapture, title string, fd *gocvgo.FaceDetector) {
	// open display window
	window := gocv.NewWindow("Video Relay: " + title)
	defer window.Close()

	// prepare image matrix
	img := gocv.NewMat()
	defer img.Close()

	log.Println("Started relaying video")
	for {
		if ok := video.Read(&img); !ok {
			fmt.Printf("cannot read file %d\n", title)
			return
		}
		if img.Empty() {
			continue
		}

		fd.Draw(&img, "Human")

		// show the image in the window, and wait 1 millisecond
		window.IMShow(img)
		if window.WaitKey(1) >= 0 {
			break
		}
	}
}
