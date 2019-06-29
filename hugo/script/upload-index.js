// upload index file to algolia

require('dotenv').config()
const algoliasearch = require('algoliasearch')

const appId = process.env.ALGOLIA_APP_ID
const adminKey = process.env.ALGOLIA_ADMIN_KEY
const indexName = process.env.ALGOLIA_INDEX_NAME

const client = algoliasearch(appId, adminKey);
const index = client.initIndex(indexName);

const data = require(__dirname + '/../static/algolia-index/curated.json')
index.addObjects(data, (err, content) => {
    if (err) {
        console.log('[ERROR] failed to upload index to algolia:', err.message)
        return
    }
    const dashboardUrl = `https://www.algolia.com/apps/${appId}/explorer/browse/${indexName}`
    console.log('[INFO] index uploaded. see at dashboard:', dashboardUrl);
});