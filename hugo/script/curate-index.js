const fs = require('fs')
const matter = require('gray-matter')

const idxPath = __dirname + '/../static/lunr-index'
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
        
        let index = {
            uri,
            date: parsed.data.date,
            title: parsed.data.title,
            body: parsed.content
                .replace(/\n/g, ' ')
                .replace(/(style=\".+\")|(src=\".+\")|(class=\"[a-zA-Z0-9-_ ]+\")/ig, '')
                .replace(/(\*|\\n|\/i|\/p|span|div|iframe|(\s+\/\s+)|(\s+p\s+))/ig, '')
                .replace(/\.\s+!/g, '. ')
                .trim(),
            tags: item.tags,
        }
        curated.push(index)
    } catch (e) { /* no-op */ }
})

// write new index
fs.writeFileSync(idxPath + '/curated.json', JSON.stringify(curated));
console.log(`[INFO] index curated. collected ${curated.length} out of ${idx.length}.`)