// run the program and generate the version string:
// go run -ldflags "-X 'main.VersionString=1.0 (beta)'" gogenerate.go
//
// you can also use -ldflags in `go build`:
// go run -ldflags "-X 'main.VersionString=1.0 (beta)'" gogenerate.go
package main

import (
	"fmt"
)

var VersionString = "(unset)"

func main() {
	fmt.Println("Version:", VersionString)
}
