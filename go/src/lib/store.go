package lib

import (
	"bytes"
	"encoding/gob"
	"io/ioutil"
)

type Store struct {
	filename string
	data     map[string]string
}

func NewStore() *Store {
	s := Store{
		filename: "hashstore.db",
		data:     make(map[string]string),
	}
	data, err := ioutil.ReadFile(s.filename)
	if err == nil {
		buffer := new(bytes.Buffer)
		buffer.Write(data)
		err = gob.NewDecoder(buffer).Decode(&s.data)
		if err != nil {
			panic(err)
		}
	}
	return &s
}

func (s *Store) clear() {
	s.data = make(map[string]string)
	s.save()
}

func (s *Store) size() int {
	return len(s.data)
}

func (s *Store) put(key *string, value *string) {
	s.data[*key] = *value
	s.save()
}

func (s *Store) get(key *string) *string {
	if value, ok := s.data[*key]; ok {
		return &value
	} else {
		return nil
	}
}

func (s *Store) key(index int) *string {
	i := 0
	for key, _ := range s.data {
		if i == index {
			return &key
		}
		i++
	}
	return nil
}

func (s *Store) remove(key *string) {
	delete(s.data, *key)
	s.save()
}

func (s *Store) save() {
	buffer := new(bytes.Buffer)
	err := gob.NewEncoder(buffer).Encode(s.data)
	if err != nil {
		panic(err)
	}
	err = ioutil.WriteFile(s.filename, buffer.Bytes(), 0644)
	if err != nil {
		panic(err)
	}
}
