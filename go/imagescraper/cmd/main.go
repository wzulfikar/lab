package main

import (
	"fmt"
	"os"

	"github.com/wzulfikar/lab/go/imagescraper"
)

// <div class="card__thumbnail">
//     <img src="http://www.iium.edu.my/imagecache/staff_small/9999999/3760.jpg" alt="Mohamed Ridza Wahiddin" title="Mohamed Ridza Wahiddin">
// </div>

// scraper file:///Users/strawhat/Desktop/Faculties.webarchive ".card__thumbnail img"
// output: {image title|alt}_{filename}.jpg
func main() {
	if len(os.Args) < 3 {
		fmt.Println("Usage: scraper [url] [selector] [dir]")
		return
	}

	url := os.Args[1]
	selector := os.Args[2]
	dir := os.Args[3]

	imagescraper.Scrape(url, selector, dir)
}
