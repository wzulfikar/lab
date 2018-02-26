package graphqlboiler

import (
	"fmt"
	"strings"

	"github.com/jinzhu/inflection"
)

func tplResolver(typeName, RootResolver string) string {
	return `package resolvers

import (
	"context"
)

type ` + resolverName(typeName) + ` struct {
	rr *` + RootResolver + `
	o  *models.` + typeName + `
}

func (rr *` + RootResolver + `) ` + typeName + `(ctx context.Context, args struct{ID graphql.ID}) (*` + resolverName(typeName) + `, error) {
	panic("TODO: initialize object for resolver")
	o := &models.` + typeName + `{} 
	return &` + resolverName(typeName) + `{rr: rr, o: o}, nil
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
		resolvers += `func (r *` + resolverName + `) ` + field.name + `() (` + fldType + `, error) {
	return r.o.` + field.name + `, nil
}

`
	}
	return strings.TrimRight(resolvers, "\n") + "\n"
}

func tplSchema(typeName string, fields []resolverField) string {
	var schemaFields string
	for _, field := range fields {
		fldType := strings.ToUpper(field.fieldType[0:1]) + field.fieldType[1:]
		fldName := strings.ToLower(field.name[0:1]) + field.name[1:]
		schemaFields += fmt.Sprintf("\t%s: %s!\n", fldName, fldType)
	}

	schemaFields = strings.TrimRight(strings.TrimLeft(schemaFields, "\t"), "\n")

	return `package resolvers

var ` + typeName + `Schema = ` + "`" + `
type ` + typeName + ` {
	` + schemaFields + `
}

input ` + typeName + `Filter {
	// TODO: add fields for filter 
}

` + "` + " + typeName + `Result

var ` + typeName + "Result = `" + `
type ` + typeName + `Result implements QueryResult {
	totalCount: Int!
	pageInfo: PageInfo!
	items: [` + typeName + `]!
}
` + "`" + `

var ` + typeName + `Query = ` + "`" + `
` + (strings.ToLower(typeName[0:1]) + typeName[1:]) + `(id: ID!): ` + typeName + `!
` + "`"
}

func tplQueryResult(typeName, rootResolver string) string {
	model := strings.ToUpper(typeName[0:1]) + typeName[1:]
	modelPlural := inflection.Plural(model)
	return `package resolvers

import (
	"context"
	"fmt"

	"github.com/volatiletech/sqlboiler/queries/qm"
	"gitlab.com/wzulfikar/iiumtestimony/models"
	"gitlab.com/wzulfikar/iiumtestimony/modules/graphql/app"
)

type ` + typeName + `ResultResolver struct {
	totalCount int64
	pageInfo   *app.PageInfoResolver
	items      []*` + typeName + `Resolver
}

func (r *` + typeName + `ResultResolver) PageInfo() *app.PageInfoResolver {
	return r.pageInfo
}

type ` + typeName + `Filter struct {
	// Add ` + typeName + ` filter here
}

type ` + typeName + `esArgs struct {
	Page   *app.PageArgs
	Filter *` + typeName + `Filter
}

func (rr *` + rootResolver + `) ` + modelPlural + `(ctx context.Context, args *` + typeName + `esArgs) (*` + typeName + `ResultResolver, error) {
	var mods []qm.QueryMod

	if args.Filter != nil {
		whereMods, err := app.WhereMods([]app.MaybeMod{
			// Add mods for qm.Where here. See: app.MaybeMod
		})
		if err != nil {
			return nil, err
		}

		mods = append(mods, whereMods...)
	}

	count, err := models.` + modelPlural + `(rr.Db, mods...).Count()
	if err != nil {
		return nil, nil
	}

	pageInfo, err := args.Page.PageInfo(count)
	if err != nil {
		return nil, err
	}

	mods = append(mods, pageInfo.QM()...)

	o, err := models.` + modelPlural + `(rr.Db, mods...).All()
	if err != nil {
		return nil, err
	}

	result := &` + typeName + `ResultResolver{
		totalCount: count,
		pageInfo:   pageInfo.Resolver(),
	}
	for _, row := range o {
		result.items = append(result.items, &` + typeName + `Resolver{rr: rr, o: row})
	}

	return result, nil
}

func (r *` + typeName + `ResultResolver) TotalCount() (int32, error) {
	return int32(r.totalCount), nil
}

func (r *` + typeName + `ResultResolver) Items() ([]*` + typeName + `Resolver, error) {
	return r.items, nil
}
`
}
