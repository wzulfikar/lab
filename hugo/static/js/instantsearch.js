const { appId, searchKey, indexName } = HUGO_ENV.algolia

const subIndexTrigger = '/'
const subIndex = instantsearch({
    appId,
    apiKey: searchKey,
    indexName: 'personal',
    searchParameters: {
        hitsPerPage: 5,
	},
});
  
const mainIndex = instantsearch({
    appId,
    apiKey: searchKey,
    indexName,
    searchParameters: {
        hitsPerPage: 5,
	},
	searchFunction: function(helper) {
		var searchResults = $('#hits');
		if (helper.state.query === '') {
			searchResults.hide()
			return
		}
		
		let subIndexQuery = ''
		if (helper.state.query.startsWith(subIndexTrigger)) {
			subIndexQuery = helper.state.query.replace(subIndexTrigger, '')
		}

		if (subIndexQuery.length) {
			subIndex.helper.setQuery(subIndexQuery).search();
			subIndex.helper.search()
		} else {
			// perform the regular search & display the search results
			helper.search();
		}
		searchResults.show();
	}
});

mainIndex.addWidget(
    instantsearch.widgets.searchBox({
		loadingIndicator: 'loading..',
		container: '#search-box',
		placeholder: ' \uf002 Search site',
		autofocus: false,
    })
);

const months = [
	'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
	'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
]

mainIndex.addWidget(
    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            empty: 'No results found',
            item: hit => {
				let date = hit.date && new Date(hit.date)
				if (date) {
					date = `${months[date.getMonth()].toUpperCase()} ${date.getDate()}, ${date.getFullYear()}`
				}

				let tags = hit.tags 
					? '· ' + hit.tags.map(tag => `<span class="tag">${tag}</span>`).join(', ')
					: '';

				return `
					<div class="hit-title">
						<a href="${hit.objectID}">
							${hit.coverImage ? `<img src="${hit.coverImage}"/>` : ''}
							<h4>
								${hit._highlightResult.title.value}
								<span class="subtitle">${date || hit._highlightResult.type.value} ${tags}</span>
							</h4>
							<span class="summary">
							${hit.summary
								? hit._highlightResult.summary.value 
								: hit._highlightResult.body.value.split(' ').splice(0, 35).join(' ')}
							</span>
						</a>
					</div>
					<hr/>`
			}
        }
    })
);

subIndex.addWidget(
    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            empty: 'No results found',
            item: hit => {
				let date = hit.timestamp && new Date(hit.timestamp)
				if (date) {
					date = `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`
				}

				return `
					<div class="hit-title">
						<a href="${hit.url}">
							<h4>
								<img src="${hit.thumbsUrl}" style="width: 40px; margin: 0px 0.5em 0px 0.2em; display: inline-block;"/>
								<div style="display: inline-block; vertical-align: sub;">
									<span>${hit._highlightResult.title.value}</span>
									<span class="subtitle">${hit._highlightResult.description.value}</span>
									<span class="subtitle" style="font-weight: 400;">${date}</span>
								</div>
							</h4>
							<span class="summary">
							${hit.text.endsWith('.jpg')
								? `<img src="${hit.text}"/>`
								: hit._highlightResult.text.value.split(' ').splice(0, 35).join(' ')}
							</span>
						</a>
					</div>
					<hr/>`
			}
        }
    })
);

mainIndex.start();
subIndex.start();

$searchBoxInput = $('input.ais-search-box--input')
$wrapper = $('#instantsearch-wrapper')
$hitsWrapper = $('div#hits')
$resetWrapper = $('span.ais-search-box--reset-wrapper')
$('a#trigger-search').click(() => {
    $wrapper.toggle()
})

$resetWrapper.click(e => {
	$searchBoxInput.val('')
	$searchBoxInput.focus()
})

$searchBoxInput.focus(e => {
	e.target.style.width = '140px'
	e.target.style.paddingRight = '2.2em'
})

$searchBoxInput.blur(e => {
	if (!e.target.value.trim().length) {
		e.target.style.width = ''
		e.target.style.paddingRight = ''
		e.target.value = ''
		$resetWrapper.hide()
	}
})

// use https://keycode.info to get keycode number
window.addEventListener("keyup", function (e) {
	// press '/' to start searching
	if (e.keyCode == '191' && !$searchBoxInput.is(':focus')) {
		$searchBoxInput.focus()
		return
	}
	
	// press 'esc' to exit search box
	if (e.keyCode == '27') {
		$searchBoxInput.val('')
		$searchBoxInput.trigger('blur')
		$hitsWrapper.hide()
		return
	}
}, false);
