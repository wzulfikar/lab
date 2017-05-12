package main

import (
	"fmt"
	"strings"
)

func do(s1, s2 string) int {
	s1 = strings.ToLower(s1)
	s2 = strings.ToLower(s2)
	if s1 < s2 {
		return -1
	} else if s1 > s2 {
		return 1
	}
	return 0
}

// func Test(t *testing.T) {
// 	assert.Equal(t, do("aaaa", "aaaA"), 0)
// 	assert.Equal(t, do("abs", "Abz"), -1)
// 	assert.Equal(t, do("abcdefg", "AbCdEfF"), 1)
// }

func main() {
	var s1, s2 string
	fmt.Scan(&s1, &s2)
	fmt.Println(do(s1, s2))
}
