// get html page, process using goquery
// and output jsonified data.
package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"

	"github.com/PuerkitoBio/goquery"
)

// <div class="card__thumbnail">
//     <img src="http://www.iium.edu.my/imagecache/staff_small/9999999/3760.jpg" alt="Mohamed Ridza Wahiddin" title="Mohamed Ridza Wahiddin">
// </div>

// scraper file:///Users/strawhat/Desktop/Faculties.webarchive ".card__thumbnail img"
// output: {image title|alt}_{filename}.jpg
func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: scraper [url] [selector]")
		return
	}

	url := os.Args[1]
	selector := os.Args[2]

	Scrape(url, selector)
}

func Scrape(url, selector string) {
	res, err := http.Get(url)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	if res.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", res.StatusCode, res.Status)
	}

	// Load the HTML document
	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Find the review items
	doc.Find(selector).Each(func(i int, s *goquery.Selection) {
		// For each item found, get the band and title
		src := s.Find("src").Text()
		title := s.Find("title").Text()
		alt := s.Find("alt").Text()

		if err := getty.Get(src); err != nil {
			fmt.Printf("Failed to download image at %s. Error: %v\n", src, err)
			return
		}

		file := filepath.Base(src)
		filename := fmt.Sprintf("%s_%s", title, file)
		fmt.Println("Image downloaded:", filename)
	})
}
