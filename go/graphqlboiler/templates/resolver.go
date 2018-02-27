package templates

const Resolver = `package resolvers

import (
	"context"
)

type {{.TypeName}} struct {
	rr *{{.RootResolver}}
	o  *models.{{.TypeName}}
}

func (rr *{{.RootResolver}}) {{.TypeName}}(ctx context.Context, args struct{ID graphql.ID}) (*{{.ResolverName}}, error) {
	panic("TODO: initialize object for resolver")
	o := &models.{{.TypeName}}{} 
	return &{{.TypeName}}{rr: rr, o: o}, nil
}`
