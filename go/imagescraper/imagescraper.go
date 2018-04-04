// scrape image from given url with selector
package imagescraper

import (
	"fmt"
	"log"
	"net/http"
	"net/url"
	"path/filepath"
	"strings"
	"sync"

	"github.com/PuerkitoBio/goquery"
	"github.com/pkg/errors"
	"github.com/wzulfikar/lab/go/getty"
)

func Scrape(targetUrl, selector, dir string) []string {
	res, err := http.Get(targetUrl)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()

	if res.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", res.StatusCode, res.Status)
	}

	urlParsed, err := url.Parse(targetUrl)
	if err != nil {
		log.Fatal(errors.Wrap(err, "url.Parse"))
	}
	baseUrl := fmt.Sprintf("%s://%s", urlParsed.Scheme, urlParsed.Host)

	// Load the HTML document
	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		log.Fatal(err)
	}

	var wg sync.WaitGroup

	var images []string

	// Find the review items
	doc.Find(selector).Each(func(i int, s *goquery.Selection) {
		// For each item found, get the band and title
		src, ok := s.Attr("src")
		if !ok {
			fmt.Printf("node[%d] does not have `src` attribute\n", i)
			return
		}

		if strings.HasPrefix(src, "/") {
			src = baseUrl + src
		}

		file := filepath.Base(src)

		filename := file
		if text, ok := s.Attr("title"); ok {
			filename = text + "_" + filename
		} else if text, ok := s.Attr("alt"); ok {
			filename = text + "_" + filename
		}
		filename = strings.Replace(filename, " ", "_", -1)

		wg.Add(1)
		go func(src, filename, dir string) {
			defer wg.Done()
			if err := getty.Get(src, filename, dir); err != nil {
				log.Printf("Failed to download image from %s: %v\n", src, err)
				return
			}
			images = append(images, src)
			log.Println("Image downloaded:", filename)
		}(src, filename, dir)
	})

	wg.Wait()
	return images
}
