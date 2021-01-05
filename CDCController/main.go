package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/tarm/serial"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

/*
Program for reading data from CDC and sending it to HUB
First argument is path to CDC device and second is URL to hub (with http:// included)

POST /hub/buttonPressed - When button is pressed (empty body)
POST /hub/accData - When acc data is received (body contains JSON formatted data)

 */

type TypeStruct struct {
	Type string `json:"type"`
}

type AccStruct struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
	Z float64 `json:"z"`
}
func main() {

	c := &serial.Config{Name: os.Args[1], Baud: 115200}
	s, err := serial.OpenPort(c)
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewReader(s)
	var typeObject TypeStruct
	var accObject AccStruct

	for {
		line, _, err := scanner.ReadLine()
		if err != nil {
			log.Fatalf("error when reading: %s", err.Error())
		}

		err = json.Unmarshal(line, &typeObject)
		if err != nil {
			log.Fatalf("error when reading: %s", err.Error())
		}
		if typeObject.Type == "acc" {

			err = json.Unmarshal(line, &accObject)
			if err != nil {
				log.Fatalf("error when reading: %s", err.Error())
			}

			fmt.Printf("X: %.3f - Y: %.3f - Z: %.3f", accObject.X, accObject.Y, accObject.Z)
			sendAccData(accObject)

		}else if typeObject.Type == "button" {
			fmt.Println("Button pressed")
			sendButtonPress()
		}else {
			fmt.Println("Unknown CDC Command")
		}
	}

}

func sendButtonPress() {

	req, err := http.NewRequest("POST", os.Args[2] + "/hub/buttonPressed", nil)
	if err != nil {
		fmt.Println(err)
		return
	}

	client := &http.Client{
		Timeout: time.Second * 1,
	}

	res, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return
	}

	defer res.Body.Close()
	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		fmt.Println(err)
		return
	}

	if res.StatusCode != http.StatusOK {
		fmt.Println(string(body))
		return
	}

}

func sendAccData(accData AccStruct) {

	accDataBytes, err := json.Marshal(accData)
	if err != nil {
		fmt.Println(err)
		return
	}

	req, err := http.NewRequest("POST", os.Args[2] + "/hub/accData", bytes.NewBuffer(accDataBytes))
	if err != nil {
		fmt.Println(err)
		return
	}

	client := &http.Client{
		Timeout: time.Second * 1,
	}

	res, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return
	}

	defer res.Body.Close()
	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		fmt.Println(err)
		return
	}

	if res.StatusCode != http.StatusOK {
		fmt.Println(string(body))
		return
	}

}
