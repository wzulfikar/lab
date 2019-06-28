# initiate dist directory if not exist
if [ ! -d dist ]; then
	git clone https://github.com/wzulfikar/wzulfikar.com.git dist
else
	git pull origin master
fi

# make env vars accessible by hugo
export $(cat .env)

# generate static files
BUILD_ID=$(git describe --always) hugo --minify

# push static files to remote repo
(
	cd dist
	git add .
	git commit -m 'build'
	git push -u origin master
)

echo "updating algolia index.."
yarn index:sync