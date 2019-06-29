const { appId, searchKey, indexName } = HUGO_ENV.algolia
const search = instantsearch({
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
		// perform the regular search & display the search results
		helper.search();
		searchResults.show();
	}
});
search.addWidget(
    instantsearch.widgets.searchBox({
		loadingIndicator: 'loading..',
		container: '#search-box',
		placeholder: ' \uf002 Search site',
		autofocus: false,
    })
);
search.addWidget(
    instantsearch.widgets.currentRefinedValues({
        container: '#current-refined-values',
        // This widget can also contain a clear all link to remove all filters,
        // we disable it in this example since we use `clearAll` widget on its own.
        clearAll: false
    })
);
search.addWidget(
    instantsearch.widgets.refinementList({
        container: '#refinement-list',
        attributeName: 'categories'
    })
);

const months = [
	'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
	'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',
]

search.addWidget(
    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            empty: 'No results found',
            item: hit => {
				let date = hit.date && new Date(hit.date)
				if (date) {
					date = `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`
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

search.start();

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
