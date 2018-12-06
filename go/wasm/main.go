// inspired from https://tutorialedge.net/golang/go-webassembly-tutorial/
package main

import (
	"syscall/js"
)

func sayHello(i []js.Value) {
	targetEl := i[0].String()
	js.Global().Get("document").Call("getElementById", targetEl).Set("value", "Hello wasm from Go!")
}

func registerCallbacks() {
	// bind `sayHello` in web env to above `sayHello` function
	js.Global().Set("sayHello", js.NewCallback(sayHello))
}

func main() {
	c := make(chan struct{}, 0)

	println("go wasm is initialized")
	js.Global().Get("document").Call("wasmReady")

	registerCallbacks()

	<-c
}
