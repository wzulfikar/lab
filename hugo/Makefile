serve:
	HUGO_LOCAL_DEV=true hugo server -F -D

snapshot:
	hugo && git add -A && git commit -m "hugo snapshot" && git push
	@echo "done."

publish:
	git push
	@echo "done."