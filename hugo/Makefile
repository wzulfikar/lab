dev:
	./script/dev.sh

snapshot:
	hugo && git add -A && git commit -m "hugo snapshot" && git push
	@echo "done."

publish:
	yarn index && ./script/publish.sh
