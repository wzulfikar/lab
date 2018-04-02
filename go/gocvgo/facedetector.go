// face detector usage:
//
//	// color for the rect when faces detected
// 	fd, err := NewFaceDetector(cascadeClassifierXmlFile, color.RGBA{0, 0, 255, 0})
//  if err != nil {
// 		log.Fatal(err)
// 	}
// 	defer fd.Close()
//
// 	fd.Draw(img)
// 	window.IMShow(img)
package gocvgo

import (
	"fmt"
	"image"
	"image/color"
	"log"

	"gocv.io/x/gocv"
)

type FaceDetector struct {
	XmlFile    string
	RectColor  color.RGBA
	classifier gocv.CascadeClassifier
}

func NewFaceDetector(xmlFile string, RectColor color.RGBA) (*FaceDetector, error) {
	// load classifier to recognize faces
	classifier := gocv.NewCascadeClassifier()
	if !classifier.Load(xmlFile) {
		return nil, fmt.Errorf("Error reading cascade file: %v\n", xmlFile)
	}

	return &FaceDetector{xmlFile, RectColor, classifier}, nil
}

// When face presents, draw rectangular with given
// color `RectColor` along with the label.
func (fd *FaceDetector) Draw(img *gocv.Mat, label string) {
	// detect faces
	rects := fd.classifier.DetectMultiScale(*img)
	if len(rects) > 0 {
		log.Printf("%s found: %d\n", label, len(rects))
	}

	// draw a rectangle around each face on the original image,
	// along with text label
	for _, r := range rects {
		gocv.Rectangle(img, r, fd.RectColor, 3)

		size := gocv.GetTextSize(label, gocv.FontHersheyPlain, 1.2, 2)
		pt := image.Pt(r.Min.X+(r.Min.X/2)-(size.X/2), r.Min.Y-2)
		gocv.PutText(img, label, pt, gocv.FontHersheyPlain, 1.2, fd.RectColor, 2)
	}
}

func (fd *FaceDetector) Close() {
	fd.classifier.Close()
}
