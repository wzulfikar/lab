// Send email using AWS SES using gomail
// with aws smtp creds (without aws sdk)
package main

import (
	"fmt"
	"os"

	"gopkg.in/gomail.v2" //go get gopkg.in/gomail.v2
)

// adjust config below based on your aws account.
// how to get the config:
// 1. visit https://console.aws.amazon.com/ses/home
// 2. navigate to "SMTP Settings"
// 3. take note of the server name and port
// 4. click "Create My SMTP Credentials" to create smtp user & password
var awsconf = struct {
	smtpuser, smtppass, host string
	port                     int
}{
	smtpuser: os.Getenv("AWS_SES_SMTP_USER"),
	smtppass: os.Getenv("AWS_SES_SMTP_PASS"),

	// adjust the host according to your configuration
	host: "email-smtp.us-east-1.amazonaws.com",
	port: 465,
}

const (
	// The name of the configuration set to use for this message.
	// If you comment out or remo3ve this variable, you will also need to
	// comment out or remove the header below.
	// ConfigSet = "ses-inbound-s3"

	// The subject line for the email.
	Subject = "Amazon SES Test (Gomail)"

	// The HTML body for the email.
	HtmlBody = "<html><head><title>SES Sample Email</title></head><body>" +
		"<h1>Amazon SES Test Email (Gomail)</h1>" +
		"<p>This email was sent with " +
		"<a href='https://aws.amazon.com/ses/'>Amazon SES</a> using " +
		"the <a href='https://github.com/go-gomail/gomail/'>Gomail " +
		"package</a> for <a href='https://golang.org/'>Go</a>.</p>" +
		"</body></html>"

	//The email body for recipients with non-HTML email clients.
	TextBody = "This email was sent with Amazon SES using the Gomail package."

	// The tags to apply to this message. Separate multiple key-value pairs
	// with commas.
	// If you comment out or remove this variable, you will also need to
	// comment out or remove the header on line 80.
	// Tags = "genre=test,genre2=test2"

	// The character encoding for the email.
	CharSet = "UTF-8"
)

func main() {
	// sender address must be verified with Amazon SES.
	sender := os.Getenv("AWS_SES_SENDER_EMAIL")
	senderName := "AWS SES Test"

	// If your account is still in the sandbox,
	// recipient address must be verified.
	// read more about aws ses sandobx:
	// https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html
	recipient := os.Getenv("TO")

	// Create a new message.
	m := gomail.NewMessage()

	fmt.Println("- sending AWS SES email..")
	fmt.Println("  from:", m.FormatAddress(sender, senderName))
	fmt.Println("  to:", recipient)

	// Set the main email part to use HTML.
	m.SetBody("text/html", HtmlBody)

	// Set the alternative part to plain text.
	m.AddAlternative("text/plain", TextBody)

	// Construct the message headers, including a Configuration Set and a Tag.
	m.SetHeaders(map[string][]string{
		"From":    {m.FormatAddress(sender, senderName)},
		"To":      {recipient},
		"Subject": {Subject},
		// Comment or remove the next line if you are not using a configuration set
		// "X-SES-CONFIGURATION-SET": {ConfigSet},
		// Comment or remove the next line if you are not using custom tags
		// "X-SES-MESSAGE-TAGS": {Tags},
	})

	// Send the email.
	d := gomail.NewPlainDialer(
		awsconf.host,
		awsconf.port,
		awsconf.smtpuser,
		awsconf.smtppass)

	// Display an error message if something goes wrong; otherwise,
	// display a message confirming that the message was sent.
	if err := d.DialAndSend(m); err != nil {
		fmt.Println(err)
	} else {
		fmt.Println("Email sent!")
	}
}
