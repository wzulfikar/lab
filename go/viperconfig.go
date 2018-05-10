package main

import (
	"bytes"
	"io/ioutil"
	"log"
	"path"

	"github.com/davecgh/go-spew/spew"
	"github.com/spf13/viper"
)

func main() {
	v := viper.New()
	if err := addViperConfig(v, "/path/to/config.json"); err != nil {
		log.Fatal(err)
	}

	spew.Dump(v.Get("asdf"))
}

func addViperConfig(v *viper.Viper, conf string) error {
	ext := path.Ext(conf)
	v.SetConfigType(ext[1:])

	data, err := ioutil.ReadFile(conf)
	if err != nil {
		return err
	}

	if err := v.ReadConfig(bytes.NewBuffer(data)); err != nil {
		return err
	}

	return nil
}
