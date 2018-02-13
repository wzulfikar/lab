package main

import (
	"fmt"
	"time"

	"github.com/gorhill/cronexpr"
)

func main() {
	// cron docs: https://godoc.org/github.com/robfig/cron
	cronExpr := "0 8 * * * *"
	nextTimes := cronexpr.MustParse(cronExpr).NextN(time.Now(), 5)

	fmt.Printf("Next 5 times of cron expression `%s`:\n", cronExpr)
	for i, next := range nextTimes {
		fmt.Printf("%d. %s\n", i+1, next)
	}
}
