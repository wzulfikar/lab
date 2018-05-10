package main

import (
	"fmt"
	"path"
)

func main() {
	file := "/user/test/test.json"
	fmt.Println("dir:", path.Dir(file))
	fmt.Println("base:", path.Base(file))
	fmt.Println("ext:", path.Ext(file))
	fmt.Println("clean:", path.Clean(file))

	_, split := path.Split(file)
	fmt.Println("split:", split)
}
