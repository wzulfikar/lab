## Hugo Site: wzulfikar.com

- `make publish`: build static files and send to github page
- `make publish sync-index`: publish and sync algolia index

**Note on Algolia app key**

- don't expose admin key (`ALGOLIA_ADMIN_KEY`) to frontend. use `ALGOLIA_SEARCH_KEY` instead.
- docs: https://www.algolia.com/doc/guides/security/api-keys/