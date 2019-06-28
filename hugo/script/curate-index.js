const fs = require('fs')
const matter = require('gray-matter')

const idxPath = __dirname + '/../static/algolia-index'
const idx = require(idxPath + '/raw.json')
console.log(`[INFO] loaded ${idx.length} indices`)

let curated = []
idx.forEach((item, i) => {
    const { content } = item
    try {
        let parsed = matter(content)
        if (parsed.data.draft || parsed.data.disableIndexing) {
            return
        }
        let uri = item.uri.replace(/_index$/, '').toLowerCase()
        if (uri.endsWith('.id')) {
            uri = '/' + uri.split('_index.').reverse().join('')
        }
        
        // sanitize parsed content
        parsed.content = parsed.content
            .replace(/\n/g, ' ')
            .replace(/(style=\".+\")|(class=\"[a-zA-Z0-9-_ ]+\")/ig, '')
            .replace(/(\*|\\n|\/p|\s+!|span|div|iframe|(\s+\/\s+)|(\s+p\s+))/ig, '')
            .replace(/\.\s{2,}/g, '. ')
            .trim()

        let [summary, body] = ['', parsed.content]
        if (body.includes('--more--')) {
            [summary, body] = parsed.content.split('--more--').map(section => section.trim())
        }

        let type = uri.includes('/posts') ? 'POST' : 'PAGE'

        const { date, title, tags } = parsed.data
        let index = {
            objectID: uri,  // manually set objectID for algolia
            coverImage: parsed.data.coverImg,
            date,
            type,
            title,
            summary,
            body,
            tags,
        }
        curated.push(index)
    } catch (e) { /* no-op */ }
})

// write new index
fs.writeFileSync(idxPath + '/curated.json', JSON.stringify(curated, null, 4));
console.log(`[INFO] index curated. collected ${curated.length} out of ${idx.length}.`)