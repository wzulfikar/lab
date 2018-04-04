package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"strconv"

	"github.com/willf/pad"
)

func main() {
	file := "generator.txt"

	fmt.Println("Generating strings into", file)

	var b bytes.Buffer
	generate(&b)
	write(&b, file)

	fmt.Printf("Done ✔")
}

func write(b *bytes.Buffer, file string) {
	err := ioutil.WriteFile(file, b.Bytes(), 0644)
	if err != nil {
		log.Fatal(err)
	}
}

func generate(b *bytes.Buffer) {
	generateID(b, 10, 18, 1, 9999)
}

func generateID(b *bytes.Buffer, fromYear, toYear, semesterCount, studentCount int) {
	if semesterCount > 3 {
		fmt.Println("`semesterCount` can't exceed max number of 3")
		return
	}
	if studentCount > 9999 {
		fmt.Println("`studentCount` can't exceed max number of 9999")
		return
	}

	for year := fromYear; year <= toYear; year++ {
		for semester := 1; semester <= semesterCount; semester++ {
			for count := 0; count <= studentCount; count++ {
				b.WriteString(fmt.Sprintf("%d%d%s\n", year, semester, pad.Left(strconv.Itoa(count), 4, "0")))
			}
		}
	}
}
