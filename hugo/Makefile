dev:
	./script/dev.sh

snapshot:
	hugo && git add -A && git commit -m "hugo snapshot" && git push
	@echo "done."

publish:
	./script/publish.sh

sync-index:
	@echo "updating algolia index.."
	@yarn index:sync