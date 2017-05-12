package main

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func do(s string) string {
	// your code here
	return s
}

// test the code here and comment
// it before submitting to codeforces
func Test(t *testing.T) {
	a := assert.New(t)
	a.Equal("yo", do("yo"))
}

func main() {
	var in string
	fmt.Scan(&in)
}
