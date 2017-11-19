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
	var wg sync.WaitGroup

	var tasks = []task{
		{"Task 1 - Longer Jump", 8},
		{"Task 2 - Short Jump", 3},
		{"Task 3 - Long Jump", 6},
	}

	for _, task := range tasks {
		wg.Add(1)
		go worker(task.name, task.durationInSec, &wg)
	}

	fmt.Println("→", len(tasks), "tasks are executed as go routines..")

	// go routine can't exist if the main thread has exited.
	// use `wg.Wait()` so the main thread won't exit before
	// items in WaitGroup finished.
	wg.Wait()
}
