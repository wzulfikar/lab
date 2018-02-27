package templates

const Mutations = `package resolvers

import (
	"context"
)

func (rr *{{.RootResolver}}) Create{{.TypeName}}(ctx context.Context, args struct{ID graphql.ID}) (*{{.ResolverName}}, error) {
	
	panic("TODO: handle Create{{.TypeName}} mutation")
	
	// Sample code:
	// o, err := NewBusiness(*args.Request)
	// if err != nil {
	// 	return nil, app.Error(err)
	// }

	return &{{.TypeName}}{rr: rr, o: o}, nil
}
`
