// naive wrapper of os/exec
package yell

import (
	"bytes"
	"errors"
	"fmt"
	"os/exec"
)

func Yell(name string, arg ...string) (bytes.Buffer, error) {
	var out bytes.Buffer
	var stderr bytes.Buffer

	cmd := exec.Command(name, arg...)
	cmd.Stdout = &out
	cmd.Stderr = &stderr
	err := cmd.Run()
	if err != nil {
		return bytes.Buffer{}, errors.New(fmt.Sprintf("%s: %s", err.Error(), stderr.String()))
	}
	return out, nil
}
