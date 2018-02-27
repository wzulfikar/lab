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
	"bytes"
	"fmt"
	"html/template"
	"log"
	"os"
	"reflect"
	"strings"

	"github.com/jinzhu/inflection"
	"github.com/wzulfikar/lab/go/graphqlboiler/templates"
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
	resolverName := strings.ToLower(typeName[0:1]) + typeName[1:] + "Resolver"
	fields := reflectFields(tpl.Schema)

	model := strings.ToUpper(typeName[0:1]) + typeName[1:]
	modelPlural := inflection.Plural(model)

	data := struct {
		TypeName,
		TypeNameLowerCase,
		SchemaFields,
		ModelPlural,
		ResolverName,
		RootResolver string
	}{
		typeName,
		strings.ToLower(typeName[0:1]) + typeName[1:],
		schemaFields(fields),
		modelPlural,
		resolverName,
		tpl.RootResolver,
	}

	fmt.Println("Generating graphqlboiler for struct `" + typeName + "`")

	tplResolver, err := parseTpl(templates.Resolver, data)
	if err != nil {
		log.Fatal(err)
	}

	tplResolverFields := tplResolverFields(resolverName, fields)
	fmt.Println("✔ Resolver fields template")

	tplQueryResult, err := parseTpl(templates.QueryResult, data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("✔ Query result template")

	tplSchema, err := parseTpl(templates.Schema, data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("✔ Schema template")

	mustWrite(path+strings.ToLower(typeName)+".go", tplResolver+tplResolverFields)
	mustWrite(path+strings.ToLower(typeName)+"_result.go", tplQueryResult)
	mustWrite(path+strings.ToLower(typeName)+"_schema.go", tplSchema)
	fmt.Println("✔ Write templates to file")
	fmt.Println("[DONE!]\n")
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
		resolvers += `
func (r *` + resolverName + `) ` + field.name + `() (` + fldType + `, error) {
	return r.o.` + field.name + `, nil
}
`
	}
	return strings.TrimRight(resolvers, "\n") + "\n"
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

func schemaFields(fields []resolverField) string {
	var schemaFields string
	for _, field := range fields {
		fldType := strings.ToUpper(field.fieldType[0:1]) + field.fieldType[1:]
		fldName := strings.ToLower(field.name[0:1]) + field.name[1:]
		schemaFields += fmt.Sprintf("\t%s: %s!\n", fldName, fldType)
	}

	return strings.TrimRight(strings.TrimLeft(schemaFields, "\t"), "\n")
}

func parseTpl(tplString string, data interface{}) (string, error) {
	t, err := template.New("").Parse(tplString)
	if err != nil {
		return "", err
	}

	var tpl bytes.Buffer
	if err := t.Execute(&tpl, data); err != nil {
		return "", err
	}

	return tpl.String(), nil
}

func mustWrite(filename, content string) {
	file, err := os.Create(filename)
	if err != nil {
		panic(fmt.Sprintf("Cannot create file: %v", err))
	}
	defer file.Close()
	fmt.Fprintf(file, content)
}
