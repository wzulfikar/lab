package alprgo

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"

	"github.com/openalpr/openalpr/src/bindings/go/openalpr"
)

type BindingHandler struct {
	Country             string
	Config              string
	RuntimeDir          string
	ProcessedImagesPath string
	Alpr                *openalpr.Alpr
}

func NewBindingHandler(country, config, runtimeDir string) *BindingHandler {
	alpr := openalpr.NewAlpr(country, config, runtimeDir)
	processedImagesPath := "processed"
	return &BindingHandler{country, config, runtimeDir, processedImagesPath, alpr}
}

func (h *BindingHandler) Handle(imagePath string) {
	h.handle(imagePath)
}

func (h *BindingHandler) handle(imagePath string) {
	alprResult, err := h.Alpr.RecognizeByFilePath(imagePath)
	if err != nil {
		fmt.Println("alprResultErr:", err)
		return
	}

	var plates []string
	minConfidence := float32(85.0)
	hit := "HIT"

	for _, result := range alprResult.Plates {
		for i, candidate := range result.TopNPlates {
			if candidate.OverallConfidence > minConfidence && i < 3 {
				plates = append(plates, candidate.Characters)
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

	processedPath := fmt.Sprintf("%s/%s/%s", path, h.ProcessedImagesPath, processedImage)
	err = os.Rename(imagePath, processedPath)
	if err != nil {
		log.Println("moveProcessedImageErr:", err)
	}
}
