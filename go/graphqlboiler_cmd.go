package main

import "github.com/wzulfikar/lab/go/graphqlboiler"

// sample struct
type Person struct {
	Name    string
	Age     int
	married bool `json:"-"`
}

func main() {
	// SampleSchemaPerson
	graphqlboiler.Boil(graphqlboiler.Tpl{
		RootResolver: "RootResolver",
		Schema:       Person{},
	}, "./resolvers/")
}
