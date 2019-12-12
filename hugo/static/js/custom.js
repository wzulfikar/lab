/* 
 * custom.js will be appended at end of html body.
 */

//  add style to active nav item
const path = window.location.pathname
const pathNoSlash = path.replace(/\//g, '')
if (pathNoSlash) {
	const navItem = $(`nav a[href$=${pathNoSlash}]`)[0]
	if (navItem) {
		navItem.className = 'cta'
	}
}

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
$('a, img.cover-image').each((i, el) => {
	let href = el.href

	// some adjustment if element is image.
	if (el.tagName == 'IMG') {
		// only enable photoswipe on image with no '#feature' suffix.
		if (!el.src.endsWith('#featured')) {
			href = el.src
			el.style.cursor = 'pointer'
		}
	}

	// handle links from footnote markup
	if (href && href.includes('/#fn:')) {
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

// lazy load embedded repl
$('details.show-repl-it').click(function(e) {
	const $this = $(this)
	if ($this.attr('loaded')) {
		return
	}
	const loadingIndicator = $this.find('div.repl-loading-indicator')[0]
	const loader = $this.find('div.repl-loader')[0]
	const iframe = document.createElement('iframe')
	iframe.id = (new Date()).getTime()
	iframe.height = '400px'
	iframe.width = '100%'
	iframe.src = loader.attributes.src.value
	iframe.scrolling = 'no'
	iframe.frameborder = 'no'
	iframe.allowtransparency = "true" 
	iframe.allowfullscreen = "true" 
	iframe.sandbox = "allow-forms allow-pointer-lock allow-popups allow-same-origin allow-scripts allow-modals"
	loader.replaceWith(iframe)
	$this.attr('loaded', true)
	document.getElementById(iframe.id).onload = function() {
		loadingIndicator.remove()
	}
})

// decoreate headers as link
document.querySelectorAll('h1[id],h2[id],h3[id]').forEach(el => {
	const id = el.id
	const text = el.innerText

	const styled = `<a href='#${id}'>${text}</a>`
	el.innerHTML = styled
})
