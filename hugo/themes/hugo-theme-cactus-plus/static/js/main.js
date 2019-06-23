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
const footnotePopup = {
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

$('sup.footnote-ref a').each((i, el) => {
	const id = el.href.split('#').splice(1)[0]
	const footnoteItemEl = document.getElementById(id)
	const href = footnoteItemEl.innerText.replace('[return]', '').trim()
	if (!rePopupAsset.test(href)) {
		return
	}

	// append baseURL to href if href is relative
	if (href.startsWith('/')) {
		const fullPathHref = window.location.origin + href
		footnoteItemEl.innerHTML = footnoteItemEl
			.innerHTML
			.replace(href, `<a href=${fullPathHref}>${fullPathHref}</a>`)
	}

	$(el).click(e => {
		e.preventDefault()

		footnotePopup.item.src = href
		footnotePopup.item.msrc = href
		footnotePopup.item.title = href.split('/').splice(-1)[0]

		// display photoswipe
		new PhotoSwipe(
			footnotePopup.$pswp, 
			PhotoSwipeUI_Default, 
			[footnotePopup.item], 
			footnotePopup.options
		)
		.init();
	})
})