package main

import (
	"net/http"
	"net/url"

	"github.com/cssivision/reverseproxy"
)

func main() {
	path, err := url.Parse("https://github.com")
	if err != nil {
		panic(err)
		return
	}

	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		proxy := reverseproxy.NewReverseProxy(path)
		proxy.ServeHTTP(w, r)
	})

	http.ListenAndServe(":8080", handler)
}
