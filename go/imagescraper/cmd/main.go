package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"sync"

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

	defer fmt.Println("Done ✔")

	if newUrl, from, to, pageOk := getUrlPage(url); pageOk {
		var wg sync.WaitGroup
		for i := from; i <= to; i++ {
			wg.Add(1)
			go func(i int) {
				targetUrl := newUrl + strconv.Itoa(i)
				fmt.Printf("[START] %s\n", targetUrl)

				imagescraper.Scrape(targetUrl, selector, dir)
				fmt.Println("[DONE] %d\n", url)
				wg.Done()
			}(i)
		}
		wg.Wait()
		return
	}

	fmt.Println("Scraping images from", url)
	imagescraper.Scrape(url, selector, dir)
}

func getUrlPage(url string) (string, int, int, bool) {
	param := strBetween(url, "[", "]")
	if param == "" || !strings.Contains(param, "-") {
		return "", 0, 0, false
	}

	page := strings.Split(param, "-")
	if len(page) != 2 {
		return "", 0, 0, false
	}
	page1, err := strconv.Atoi(page[0])
	if err != nil {
		return "", 0, 0, false
	}
	page2, err := strconv.Atoi(page[1])
	if err != nil {
		return "", 0, 0, false
	}

	if page1 >= page2 {
		log.Fatal("ERROR: URL contains invalid page. `page1` must be smaller than `page2`.")
	}

	url = strings.Replace(url, "["+param+"]", "", -1)
	return url, page1, page2, true
}

func strBetween(str string, a string, b string) string {
	// Get substring between two strings.
	posFirst := strings.Index(str, a)
	if posFirst == -1 {
		return ""
	}
	posLast := strings.Index(str, b)
	if posLast == -1 {
		return ""
	}
	posFirstAdjusted := posFirst + len(a)
	if posFirstAdjusted >= posLast {
		return ""
	}
	return str[posFirstAdjusted:posLast]
}
