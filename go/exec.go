package main

import (
	"fmt"
	"os/exec"
	"strings"
)

func main() {
	alpr := "docker"
	exec_cmd(alpr)
}

// https://stackoverflow.com/questions/20437336/how-to-execute-system-command-in-golang-with-unknown-arguments
func exec_cmd(cmd string) {
	parts := strings.Fields(cmd)
	head := parts[0]
	parts = parts[1:]

	out, err := exec.Command(head, parts...).Output()
	if err != nil {
		fmt.Printf("%s", err)
	}
	fmt.Printf("%s", out)
	// wg.Done() // Need to signal to waitgroup that this goroutine is done
}
