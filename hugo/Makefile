dev:
	HUGO_LOCAL_DEV=true hugo server -F -D --config ./config.dev.toml

snapshot:
	hugo && git add -A && git commit -m "hugo snapshot" && git push
	@echo "done."

build:
	hugo && git add ../docs

publish:
	git push
	@echo "done."