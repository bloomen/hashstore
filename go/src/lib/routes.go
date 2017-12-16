package lib

import (
	"io"
	"log"
	"net/http"
	"strconv"
)

const (
	skey   string = "k"
	svalue string = "v"
	sindex string = "i"
	snil   string = ""
)

func logReq(log *log.Logger, r *http.Request) {
	log.Println(r.RemoteAddr + " " + r.RequestURI)
}

func queryParam(p string, r *http.Request) string {
	params, ok := r.URL.Query()[p]
	if !ok || len(params) < 1 {
		return ""
	} else {
		return params[0]
	}
}

func Clear(log *log.Logger, s *Store) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		logReq(log, r)
		size := strconv.Itoa(s.size())
		s.clear()
		w.WriteHeader(http.StatusOK)
		io.WriteString(w, size)
	}
}

func Size(log *log.Logger, s *Store) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		logReq(log, r)
		w.WriteHeader(http.StatusOK)
		io.WriteString(w, strconv.Itoa(s.size()))
	}
}

func Get(log *log.Logger, s *Store) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		logReq(log, r)
		key := queryParam(skey, r)
		index := queryParam(sindex, r)
		if key == "" && index == "" {
			w.WriteHeader(http.StatusBadRequest)
		} else if key != "" {
			value := s.get(&key)
			if value != nil {
				w.WriteHeader(http.StatusOK)
				io.WriteString(w, *value)
			} else {
				w.WriteHeader(http.StatusNoContent)
				io.WriteString(w, snil)
			}
		} else if index != "" {
			ind, err := strconv.Atoi(index)
			if err != nil {
				w.WriteHeader(http.StatusBadRequest)
			} else {
				k := s.key(ind)
				if k != nil {
					w.WriteHeader(http.StatusOK)
					io.WriteString(w, *k)
				} else {
					w.WriteHeader(http.StatusNoContent)
					io.WriteString(w, snil)
				}
			}
		}
	}
}

func Put(log *log.Logger, s *Store) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		logReq(log, r)
		key := queryParam(skey, r)
		value := queryParam(svalue, r)
		if key == "" || value == "" {
			w.WriteHeader(http.StatusBadRequest)
		} else {
			old_value := s.get(&key)
			s.put(&key, &value)
			if old_value != nil {
				w.WriteHeader(http.StatusResetContent)
				io.WriteString(w, *old_value)
			} else {
				w.WriteHeader(http.StatusOK)
				io.WriteString(w, snil)
			}
		}
	}
}

func Remove(log *log.Logger, s *Store) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		logReq(log, r)
		key := queryParam(skey, r)
		if key == "" {
			w.WriteHeader(http.StatusBadRequest)
		} else {
			old_value := s.get(&key)
			if old_value != nil {
				s.remove(&key)
				w.WriteHeader(http.StatusOK)
				io.WriteString(w, *old_value)
			} else {
				w.WriteHeader(http.StatusNoContent)
				io.WriteString(w, snil)
			}
		}
	}
}
