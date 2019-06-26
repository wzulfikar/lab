dev:
	HUGO_LOCAL_DEV=true hugo server -F -D --config ./config.dev.toml

snapshot:
	hugo && git add -A && git commit -m "hugo snapshot" && git push
	@echo "done."

deploy:
	hugo --minify && \
	cd dist && \
	git init && \
	git add . && \
	git commit -m 'build' && \
	git remote add origin https://github.com/wzulfikar/wzulfikar.com.git && \
	git push -u origin master

publish:
	git commit -m 'hugo: update blog content'
	git push
	@echo "done."