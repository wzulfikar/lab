package main

import (
	"fmt"
	"log"
	"time"

	"github.com/fatih/color"
	"github.com/rs/xid"
	"github.com/satori/go.uuid"
	"github.com/teris-io/shortid"
)

func main() {

	terisshortid()
	rs_xid()
	satoriuuid()
}

func terisshortid() {
	defer timer("github.com/teris-io/shortid")()
	fmt.Println("\n=== Generator used: github.com/teris-io/shortid ===\n")

	// initialize generator
	sid, err := shortid.New(1, shortid.DefaultABC, 2342)
	if err != nil {
		log.Fatal(err)
	}

	// // generate the short id
	var id string
	for i := 0; i < 5; i++ {
		id, err = sid.Generate()
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("shortid %d: %s\n", i+1, id)
	}
}

func satoriuuid() {
	defer timer("github.com/satori/go.uuid")()
	fmt.Println("\n=== Generator used: github.com/satori/go.uuid ===\n")

	for i := 0; i < 5; i++ {
		fmt.Printf("uuid %d: %s\n", i+1, uuid.NewV4())
	}

	// Parsing UUID from string input
	u2, err := uuid.FromString("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	if err != nil {
		fmt.Println("Something went wrong: %s", err)
	}
	fmt.Println("\nTest parsing uuid from string")
	fmt.Println("Successfully parsed:", u2)
}

func rs_xid() {
	defer timer("github.com/rs/xid")()
	fmt.Println("\n=== Generator used: github.com/rs/xid ===\n")

	for i := 0; i < 5; i++ {
		fmt.Printf("xid %d: %s\n", i+1, xid.New())
	}
}

func timer(taskName string) func() {
	start := time.Now()
	return func() {
		color.Cyan("\n=== " + taskName + " done in " + time.Since(start).String() + " ===\n")
	}
}
