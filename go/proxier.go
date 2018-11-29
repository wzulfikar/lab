package main

import (
	"fmt"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"time"
)

type Prox struct {
	target *url.URL
	proxy  *httputil.ReverseProxy
}

func NewProxy(target string) *Prox {
	url, _ := url.Parse(target)
	return &Prox{target: url, proxy: httputil.NewSingleHostReverseProxy(url)}
}

var listenAddr = "127.0.0.1:9001"

type transport struct{}

func (t *transport) RoundTrip(request *http.Request) (*http.Response, error) {
	start := time.Now()
	response, err := http.DefaultTransport.RoundTrip(request)
	if err != nil {
		// failed to reach upstream
		return nil, err
	}

	elapsed := time.Since(start)
	key := request.Method + " " + request.URL.Path
	log.Println(elapsed, key)
	return response, nil
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("usage: proxier <origin url>")
		fmt.Println("example: proxier http://localhost:8888")
		return
	}

	origin, _ := url.Parse(os.Args[1])
	director := func(req *http.Request) {
		req.Header.Add("X-Forwarded-Host", req.Host)
		req.Header.Add("X-Origin-Host", origin.Host)
		req.URL.Scheme = "http"
		req.URL.Host = origin.Host
	}

	proxy := &httputil.ReverseProxy{
		Director:  director,
		Transport: &transport{},
	}

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		proxy.ServeHTTP(w, r)
	})

	log.Printf("proxier is listening at %s", listenAddr)
	log.Printf("all requests will be forwarded to %s", origin)
	log.Fatal(http.ListenAndServe(listenAddr, nil))
}
