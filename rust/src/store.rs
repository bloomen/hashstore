use std::collections::HashMap;
use std::option::Option;
use serde_json;
use std::fs::File;
use std::io::prelude::*;
use std::error::Error;

pub struct Store {
    filename: String,
    map: HashMap<String, String>,
}

impl Store {
    pub fn new() -> Store {
        let mut s = Store {
            filename: "hashstore.db".to_string(),
            map: HashMap::new(),
        };
        match File::open(&s.filename) {
            Ok(mut file) => {
                let mut map_str = String::new();
                match file.read_to_string(&mut map_str) {
                    Ok(_) => {
                        s.map = serde_json::from_str(&map_str).unwrap();
                    }
                    Err(_) => {
                        panic!("error reading from {}", s.filename);
                    }
                }
                s
            }
            Err(_) => s,
        }
    }
    pub fn clear(&mut self) {
        self.map.clear();
        self.save();
    }
    pub fn size(&self) -> usize {
        self.map.len()
    }
    pub fn put(&mut self, key: String, value: String) {
        self.map.insert(key, value);
        self.save();
    }
    pub fn get(&self, key: &String) -> Option<String> {
        self.map.get(key).cloned()
    }
    pub fn key(&self, index: usize) -> Option<String> {
        let mut i: usize = 0;
        for (ref key, _value) in &self.map {
            if i == index {
                return Some((*key).clone());
            }
            i += 1;
        }
        None
    }
    pub fn remove(&mut self, key: &String) {
        self.map.remove(key);
        self.save();
    }
    fn save(&self) {
        let map_str = serde_json::to_string(&self.map).unwrap();
        let mut file = match File::create(&self.filename) {
            Err(why) => panic!("could not create {}: {}", self.filename, why.description()),
            Ok(file) => file,
        };
        if let Err(why) = file.write_all(map_str.as_bytes()) {
            panic!(
                "could not write to {}: {}",
                self.filename,
                why.description()
            )
        }
    }
}
