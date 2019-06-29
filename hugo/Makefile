dev:
	./script/dev.sh

snapshot:
	hugo && git add -A && git commit -m "hugo snapshot" && git push
	@echo "done."

build:
	./script/publish.sh --build-only

publish:
	./script/publish.sh

sync-index:
	@echo "updating algolia index.."
	@yarn index:sync