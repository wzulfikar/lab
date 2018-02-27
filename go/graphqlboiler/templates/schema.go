package templates

const Schema = `package resolvers

var {{.TypeName}}Schema = ` + "`" + `
type {{.TypeName}} {
	{{.SchemaFields}}
}

input {{.TypeName}}Filter {
	// TODO: add fields for filter 
}

` + "` + {{.TypeName}}Result" + `

var {{.TypeName}}Result = ` + "`" + `
type {{.TypeName}}Result implements QueryResult {
	totalCount: Int!
	pageInfo: PageInfo!
	items: [{{.TypeName}}]!
}
` + "`" + `

var {{.TypeName}}Query = ` + "`" + `
{{.TypeNameLowerCase}}(id: ID!): {{.TypeName}}!
` + "`" + `

var {{.TypeName}}Mutations = ` + "`" + `
create{{.TypeName}}(id: ID!): {{.TypeName}}!
` + "`"
