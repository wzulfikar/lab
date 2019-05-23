document.querySelectorAll('h1[id],h2[id],h3[id]').forEach(el => {
	const id = el.id
	const text = el.innerText
	const firstLetter = text[0]
	const trailingLetters = text.substring(1)

	const styled = `<a href='#${id}'><span class="header--first-letter">${firstLetter}</span>${trailingLetters}</a>`
	el.innerHTML = styled
})
