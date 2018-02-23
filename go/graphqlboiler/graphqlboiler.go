// generate graphql resolvers and schema
// based on struct
//
// sample code:
//
// 	graphqlboiler.Boil(graphqlboiler.Tpl{
//		RootResolver: "RootResolver",
//		schema:       Person{},
//	}, "./graphqlboiler/")
//

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
	tplSchema := tplSchema(typeName, fields)

	mustWrite(path+strings.ToLower(typeName)+".go", tplResolver+tplResolverFields)
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

func tplResolver(typeName, RootResolver string) string {
	return `package resolvers

import (
	"context"
)

type ` + resolverName(typeName) + ` struct {
	rr *` + RootResolver + `
	o  *models.` + typeName + `
}

func (rr *` + RootResolver + `) ` + typeName + `(ctx context.Context, args struct{ID graphql.ID}) (*` + resolverName(typeName) + `, err) {
	// TODO: initialize object for resolver
	o := &models.` + typeName + `{} 
	return *` + resolverName(typeName) + `{rr: rr, o: o}
}

`
}

func tplResolverFields(resolverName string, fields []resolverField) string {
	var resolvers string
	var fldType string
	for _, field := range fields {
		switch field.fieldType {
		case "uint":
			fldType = "int32"
		default:
			fldType = field.fieldType
		}
		resolvers += `func (r *` + resolverName + `) ` + field.name + `(` + fldType + `, error) {
	return r.o.` + field.name + `
}

`
	}
	return resolvers
}

func tplSchema(typeName string, fields []resolverField) string {
	var schemaFields string
	for _, field := range fields {
		fldType := strings.ToUpper(field.fieldType[0:1]) + field.fieldType[1:]
		schemaFields += fmt.Sprintf("\t%s: %s!\n", field.name, fldType)
	}

	schemaFields = strings.TrimRight(strings.TrimLeft(schemaFields, "\t"), "\n")

	return `package resolvers

var ` + typeName + `Schema = ` + "`" + `
type ` + typeName + ` {
	` + schemaFields + `
}` + "`" + `

var ` + typeName + `Query = ` + "`" + `
` + (strings.ToLower(typeName[0:1]) + typeName[1:]) + `(id: ID!): ` + typeName + `!
` + "`"
}
