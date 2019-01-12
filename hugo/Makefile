
serve:
	HUGO_LOCAL_DEV=true hugo server -F -D

deploy:
	hugo && git add -A && git commit -m "Build hugo 🔨" && git push
	@echo "Done!"
