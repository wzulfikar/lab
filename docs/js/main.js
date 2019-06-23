// To make images retina, add a class "2x" to the img element
// and add a <image-name>@2x.png image. Assumes jquery is loaded.

function isRetina() {
	var mediaQuery = "(-webkit-min-device-pixel-ratio: 1.5),\
					  (min--moz-device-pixel-ratio: 1.5),\
					  (-o-min-device-pixel-ratio: 3/2),\
					  (min-resolution: 1.5dppx)";
 
	if (window.devicePixelRatio > 1)
		return true;
 
	if (window.matchMedia && window.matchMedia(mediaQuery).matches)
		return true;
 
	return false;
};
 
function retina() {
	if (!isRetina()) 
		return;

	$("img.2x").map(function(i, image) {
		var path = $(image).attr("src");
		path = path.replace(".png", "@2x.png");
		path = path.replace(".jpg", "@2x.jpg");
		$(image).attr("src", path);
	});
};

$(document).ready(retina);

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
const rePopupAsset = /(.gif|.png|.jpg|.jpeg)/

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
		console.log("h:", href)
		return
	}
	console.log("attaching:", href)
	// attach photoswipe
	const opts = inlinePopupOpts
	$(el).click(e => {
		e.preventDefault()

		opts.item.src = href
		opts.item.msrc = href
		opts.item.title = href.split('/').splice(-1)[0]

		// trigger photoswipe
		new PhotoSwipe(
			opts.$pswp, 
			PhotoSwipeUI_Default, 
			[opts.item], 
			opts.options
		).init();
	})
})
