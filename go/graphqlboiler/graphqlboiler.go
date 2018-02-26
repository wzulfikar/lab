// generate graphql resolvers and schema
// based on struct
//
// sample code:
//
// 	graphqlboiler.Boil(graphqlboiler.Tpl{
//		RootResolver: "RootResolver",
//		schema:       Person{},
//	}, "./graphqlboiler/")
package graphqlboiler

import (
	"fmt"
	"os"
	"reflect"
	"strings"
)

// sample schema
type SampleSchemaPerson struct {
	Name    string
	Age     int
	married bool `json:"-"`
}

type resolverField struct {
	name      string
	fieldType string
}

type Tpl struct {
	RootResolver string
	Schema       interface{}
}

func Boil(tpl Tpl, path string) {
	typeName := string(reflect.TypeOf(tpl.Schema).Name())
	tplResolver := tplResolver(typeName, tpl.RootResolver)

	fields := reflectFields(tpl.Schema)

	tplResolverFields := tplResolverFields(resolverName(typeName), fields)
	tplQueryResult := tplQueryResult(typeName, tpl.RootResolver)
	tplSchema := tplSchema(typeName, fields)

	mustWrite(path+strings.ToLower(typeName)+".go", tplResolver+tplResolverFields)
	mustWrite(path+strings.ToLower(typeName)+"_result.go", tplQueryResult)
	mustWrite(path+strings.ToLower(typeName)+"_schema.go", tplSchema)
}

func resolverName(typeName string) string {
	return strings.ToLower(typeName[0:1]) + typeName[1:] + "Resolver"
}

func reflectFields(schema interface{}) (fields []resolverField) {
	rv := reflect.ValueOf(schema)
	for i := 0; i < rv.NumField(); i++ {
		fld := rv.Field(i)
		typeFld := rv.Type().Field(i)

		// don't generate resolver for fields
		// with json tag "-"
		if typeFld.Tag.Get("json") == "-" {
			continue
		}

		fields = append(fields, resolverField{typeFld.Name, fld.Type().Name()})
	}
	return fields
}

func mustWrite(filename, content string) {
	file, err := os.Create(filename)
	if err != nil {
		panic(fmt.Sprintf("Cannot create file: %v", err))
	}
	defer file.Close()
	fmt.Fprintf(file, content)
}
