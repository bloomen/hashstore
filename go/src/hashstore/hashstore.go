package main

import (
	"lib"
	"log"
	"net/http"
	"os"
)

func main() {
	s := lib.NewStore()

	host := "127.0.0.1"
	port := "5004"
	listen := host + ":" + port

	logger := log.New(os.Stdout, "", log.Ltime)

	http.HandleFunc("/clear", lib.Clear(logger, s))
	http.HandleFunc("/size", lib.Size(logger, s))
	http.HandleFunc("/get", lib.Get(logger, s))
	http.HandleFunc("/put", lib.Put(logger, s))
	http.HandleFunc("/remove", lib.Remove(logger, s))

	logger.Println("Serving on http://" + listen)
	logger.Fatal(http.ListenAndServe(listen, nil))
}
