package main

import "fmt"

func main() {
	test := "hello*"
	fmt.Println(test[0 : len(test)-1])
}
