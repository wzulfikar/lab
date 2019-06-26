/* 
 * custom.js will be appended at end of html body.
 */

// open external code runner in new tab
$('a:contains("Run in")').each((i, el) => {
	el.target = '_blank'
	console.log(el)
})

// decorate collapsible details
$('summary.collapsible').click(e => {
	e.target.innerText = e.target.innerText == 'collapse'
		? 'expand'
		: 'collapse'
})

// handle footnote popup
const inlinePopupOpts = {
	$pswp: $('.pswp')[0],
	options: {
		index: 0, 
		bgOpacity: 0.8,
		showHideOpacity: true
	},
	item: {
		w		: 800, // temp default size
		h 		: 600, // temp default size
	}
}

// formats to display in photoswipe popup
const rePopupAsset = /(.gif|.png|.jpg|.jpeg|.mp4)/

// attach photoswipe to anchor tags which href is an image
$('a').each((i, el) => {
	let href = el.href

	// handle links from footnote markup
	if (href.includes('/#fn:')) {
		const id = el.href.split('#').splice(1)[0]
		const footnoteItemEl = document.getElementById(id)
		
		// replace `#fn:{footnote id}` href with actual link
		href = footnoteItemEl.innerText.replace('[return]', '').trim()

		// append baseURL to href if href is relative
		if (href.startsWith('/')) {
			const fullPathHref = window.location.origin + href
			footnoteItemEl.innerHTML = footnoteItemEl
				.innerHTML
				.replace(href, `<a href=${fullPathHref}>${fullPathHref}</a>`)
		}
	}

	// ignore if href is not supported asset
	if (!rePopupAsset.test(href)) {
		return
	}

	// attach photoswipe
	const item = Object.assign({}, inlinePopupOpts.item)
	$(el).click(e => {
		e.preventDefault()

		// handle mp4
		if (href.endsWith('.mp4')) {
			const v = document.createElement('video')
			v.src = href
			v.controls = true
			v.autoplay = true
			v.loop = true
			v.style.top = '51%'
			v.style.left = '51%'
			v.style.position = 'absolute'
			v.style.maxWidth = '90%'
			v.style.maxHeight = '80%'
			v.style.transform = 'translate(-50%, -50%)'

			item.html = v.outerHTML
		} else {
			item.src = href
			item.msrc = href
		}
		item.title = href.split('/').splice(-1)[0]

		// trigger photoswipe
		new PhotoSwipe(
			inlinePopupOpts.$pswp, 
			PhotoSwipeUI_Default, 
			[item], 
			inlinePopupOpts.options
		).init();
	})
})