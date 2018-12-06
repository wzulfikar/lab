// Use the //export comment (eg. line 9)
// to annotate functions you wish
// to make accessible to
// other languages.
package main

import "C"

//export Hello
func Hello() *C.char {
	return C.CString("Hello world from Go!")
}

// an empty main function must be declared
func main() {}
