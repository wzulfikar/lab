package alprgo

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"time"

	"github.com/pkg/errors"
)

type ExecHandler struct {
	AdjustStdout        bool
	Country             string
	ProcessedImagesPath string
}

func NewExecHandler(adjustStdout bool, country, processedImagesPath string) *ExecHandler {
	return &ExecHandler{adjustStdout, country, processedImagesPath}
}

func (h *ExecHandler) Handle(imagePath string) {
	alprResult := &alprResult{}
	if err := alprResult.exec(imagePath, h.AdjustStdout, "-c", h.Country); err != nil {
		fmt.Println(err)
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

	processedPath := fmt.Sprintf("%s/%s/%s", path, h.ProcessedImagesPath, processedImage)
	if err := os.Rename(imagePath, processedPath); err != nil {
		log.Println("moveProcessedImageErr:", err)
	}
}

func (r *alprResult) exec(imagePath string, adjustStdout bool, args ...string) error {
	cmd := "alpr"
	args = append(args, "-j", imagePath)
	log.Println("Processing image:", cmd, args)

	b, err := exec.Command(cmd, args...).Output()
	if err != nil {
		return errors.Wrap(err, "exec output")
	}

	if adjustStdout {
		b = bytes.TrimLeft(b, "[ INFO:0] Initialize OpenCL runtime...")
	}

	return json.Unmarshal(b, r)
}

// generated from https://mholt.github.io/json-to-go/
type alprResult struct {
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
