package slackwebhook

import (
	"errors"
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/ashwanthkumar/slack-go-webhook"
	"github.com/spf13/viper"
)

type webhook struct {
	webhook string
	server  string
}

var channels = map[string]bool{}
var origins = map[string]bool{}

func NewHandler(server, configDir string) func(w http.ResponseWriter, r *http.Request) {
	v := viper.New()

	v.AddConfigPath(configDir)
	if err := v.ReadInConfig(); err != nil {
		log.Fatal(err)
	}

	for _, o := range v.GetStringSlice("origins") {
		origins[o] = true
	}
	for _, c := range v.GetStringSlice("channels") {
		channels[c] = true
	}

	w := &webhook{v.GetString("webhook"), server}
	if v.GetString("webhook") == "" || len(origins) == 0 || len(channels) == 0 {
		log.Fatal("Invalid configuration")
	}

	return w.handlePayload
}

func (w *webhook) Send(payload slack.Payload) error {
	if payload.Channel == "" {
		return fmt.Errorf("Channel cannot be empty")
	}

	if !channels[payload.Channel] {
		return fmt.Errorf("Invalid channel: %s", payload.Channel)
	}

	err := slack.Send(w.webhook, "", payload)
	if len(err) > 0 {
		return err[0]
	}
	return nil
}

// test:
// curl -d "channel=#test&text=hello+world&author=yolo" -X POST http://localhost:9090
func (o *webhook) handlePayload(w http.ResponseWriter, r *http.Request) {
	var err error
	var site, redirect string
	var skipThankyou, wantJson bool

	defer func() {
		if wantJson {
			if err != nil {
				http.Error(w, `{"ok":false,"msg":"`+err.Error()+`"}`, http.StatusBadRequest)
				return
			}
			fmt.Fprintf(w, `{"ok":true,"msg":"Payload sent"}`)
		} else {
			if err != nil {
				w.Write([]byte(templateFormError(err.Error(), site)))
				return
			}

			if redirect == "" {
				redirect = site
			}
			if skipThankyou {
				http.Redirect(w, r, redirect, http.StatusSeeOther)
				return
			}
			w.Write([]byte(templateFormSubmitted(redirect)))
		}
	}()

	// cors
	origin := strings.SplitAfter(r.Header.Get("Origin"), "://")
	referer := strings.SplitAfter(r.Header.Get("Referer"), "://")

	if len(origin) < 2 {
		if len(referer) > 1 && referer[1] != o.server {
			err = errors.New("Bad referer")
			return
		}
		err = errors.New("Invalid origin")
		return
	} else if !origins[origin[1]] {
		err = errors.New("Bad origin")
		return
	}

	// prepare slack payload
	attachment := &slack.Attachment{}
	payload := slack.Payload{
		Username:  "WebFormBot",
		IconEmoji: ":robot_face:",
	}

	r.ParseForm()

	// honeypot
	if strings.Join(r.Form["_gotcha"], "") != "" {
		return
	}

	wantJson = strings.Join(r.Form["_json"], "") == "true"
	if err = checkParams(r); err != nil {
		return
	}

	for k, v := range r.Form {
		switch strings.ToLower(k) {
		// app specific (underscore prefix)
		case "_site":
			site = strings.Join(v, "")
		case "_redirect":
			redirect = strings.Join(v, "")
		case "_skipthankyou":
			if strings.Join(v, "") == "true" {
				skipThankyou = true
			}

		// slack message
		case "text":
			payload.Text = strings.Join(v, "")
		case "channel":
			payload.Channel = strings.Join(v, "")

		// slack attachment
		case "attachmentcolor":
			color := strings.Join(v, "")
			attachment.Color = &color

		// slack fields
		default:
			attachment = attachment.AddField(slack.Field{Title: k, Value: strings.Join(v, "")})
		}
	}

	payload.Attachments = []slack.Attachment{*attachment}
	err = o.Send(payload)
	if strings.Contains(err.Error(), "no such host") {
		err = errors.New("Error connecting to slack")
	}
}

func checkParams(r *http.Request) error {
	// check site
	if strings.Join(r.Form["_site"], "") == "" {
		return errors.New("`_site` parameter is required")
	}
	return nil
}
