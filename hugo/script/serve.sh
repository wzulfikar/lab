# serve.sh runs hugo dev server for local development

# make env vars accessible by hugo
export $(cat .env)

HUGO_LOCAL_DEV=true \
BUILD_ID=$(git describe --always) \
hugo server -F -D --config ./config.dev.toml
