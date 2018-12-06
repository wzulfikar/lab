# this directory demonstrates the interop of go codes
# in other languages by utilizing c shared object (the `.so` binary).
# flow:
# - write the go codes (hello.go)
# - compile to shared object (hello.so)
# - import the .so file in other languages to call the go code

build:
	go build -o hello.so -buildmode=c-shared hello.go

run-c:
	gcc -o hello.bin hello-caller.c ./hello.so
	./hello.bin

run-node:
	node hello-caller.js

run-python:
	python hello-caller.py

run-ruby:
	ruby hello-caller.rb
