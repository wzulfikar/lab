package main

import (
	"fmt"
	"os"

	"github.com/plivo/plivo-go"
)

func main() {
	if len(os.Args) < 3 {
		fmt.Println("USAGE : plivo <plivo key>")
		fmt.Println("SAMPLE: plivo NDEwYWQ2Mjg3...SDFkjsdf23")
		return
	}

	key := os.Args[1]
	client, err := plivo.NewClient(key, &plivo.ClientOptions{})
	if err != nil {
		panic(err)
	}
	// client.Messages.Create(plivo.MessageCreateParams{
	// 	Src:  "60142616200",
	// 	Dst:  "601111220034",
	// 	Text: "Hello, world!",
	// })

	client.Calls.Create(plivo.CallCreateParams{
		From:      "60123123123",
		To:        "60123123123",
		AnswerURL: "http://example.com",
	})

	fmt.Println("Done ✔")
}
