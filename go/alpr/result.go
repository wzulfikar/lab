package alprgo

import (
	"encoding/json"
	"log"
	"os/exec"
)

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

func (r *AlprResult) From(imagePath string, args ...string) error {
	cmd := "/usr/bin/alpr"
	args = append(args, "-j", imagePath)
	log.Println("Processing image:", cmd, args)

	bytes, err := exec.Command(cmd, args...).Output()
	if err != nil {
		return err
	}

	return json.Unmarshal(bytes, r)
}
