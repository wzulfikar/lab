serve:
	go run server.go

build:
	GOARCH=wasm GOOS=js go build -o lib.wasm main.go

# download wasm_exec.js script that will
# work with go1.11.2 wasm binary
wasm_exec.js:
	wget https://raw.githubusercontent.com/golang/go/release-branch.go1.11/misc/wasm/wasm_exec.js

deploy:
	cp lib.wasm index.html wasm_exec.js dist/
	surge dist
