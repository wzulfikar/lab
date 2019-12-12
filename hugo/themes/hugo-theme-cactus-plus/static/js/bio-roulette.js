// Hi there,
// you've come this far to see
// the "bio roulette". Thanks!

const quote = (...args) => {
	const [byline, word] = [args.shift(), args.join("<br/>")]
	return `<i>${word}</i></br>– ${byline}`
}

const words = [
	"What should I put for bio?", 
	"Is this my bio now?",
	"AWS – <i>'Anything' Web Service</i>",
	"BIO – <i>Back in Office</i>",
	"IMO – <i>I Made One</i>",
	"WWW – <i>World Will Wait</i>",
	"WWW – <i>World Wide Wallet</i>",

	quote("Muhammad Ali", "Don't count the days. Make the days count."),
	quote("The Jogging Baboon", "It gets easier. Every day it gets a little easier.", "But you got to do it every day."),
	quote("Batman", "I'm Batman"),
];

// get random number as index (including `min`, excluding `max`)
const [min, max] = [0, words.length]
const randomIdx = Math.floor(Math.random() * max) + min

// update header bio
document.getElementById('header--bio').innerHTML = words[randomIdx]