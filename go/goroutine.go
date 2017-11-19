package main

import (
	"fmt"
	"sync"
	"time"
)

func worker(name string, timeInSecs int64, wg *sync.WaitGroup) {
	defer wg.Done()

	fmt.Println("[STARTED]", name, ": Should take", timeInSecs, "seconds")

	// sleep for a while to simulate time consumed by event
	time.Sleep(time.Duration(timeInSecs) * time.Second)

	fmt.Println("[FINISHED]", name)
}

type task struct {
	name          string
	durationInSec int64
}

func main() {
	var startTime = time.Now()
	var wg sync.WaitGroup

	var tasks = []task{
		{"Task 1 - Longer Jump", 6},
		{"Task 2 - Short Jump", 2},
		{"Task 3 - Long Jump", 4},
	}

	for _, task := range tasks {
		wg.Add(1)
		// try remove the `go` to run our tasks without
		// concurrency and see the diff in total execution time.
		go worker(task.name, task.durationInSec, &wg)
	}

	fmt.Println("→", len(tasks), "tasks are executed as go routines..")

	// go routine can't exist if the main thread has exited.
	// use `wg.Wait()` so the main thread won't exit before
	// items in WaitGroup finished.
	wg.Wait()

	fmt.Println("Total execution time:", time.Since(startTime), "seconds")
}
