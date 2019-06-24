dev:
	HUGO_LOCAL_DEV=true hugo server -F -D --config ./config.dev.toml

snapshot:
	hugo && git add -A && git commit -m "hugo snapshot" && git push
	@echo "done."

build:
	hugo --minify && git add ../docs

publish:
	git commit -m 'hugo: update blog content'
	git push
	@echo "done."