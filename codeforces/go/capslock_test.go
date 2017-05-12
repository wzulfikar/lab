package main

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func do(s string) string {
	if length := len(s); length > 10 {
		return fmt.Sprintf("%c%d%c", s[0], length-2, s[length-1])
	}
	return s
}

func Test(t *testing.T) {
	a := assert.New(t)
	a.Equal("Caps", do("cAPS"))
	a.Equal("Lock", do("Lock"))
}

func main() {
	var n int
	var s string
	fmt.Scan(&n)
	for n > 0 {
		fmt.Scan(&s)
		fmt.Println(do(s))
		n--
	}
}
