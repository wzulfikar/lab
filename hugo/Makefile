dev:
	HUGO_LOCAL_DEV=true \
	BUILD_ID=$(shell git describe --always) \
	hugo server -F -D --config ./config.dev.toml

snapshot:
	hugo && git add -A && git commit -m "hugo snapshot" && git push
	@echo "done."

publish:
	./publish.sh
