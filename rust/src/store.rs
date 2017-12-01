use std::collections::HashMap;
use std::option::Option;

pub struct Store {
    filename: String,
    map: HashMap<String, String>,
}

impl Store {
    pub fn new() -> Store {
        Store {
            filename: "hashstore.db".to_string(),
            map: HashMap::new(),
        }
    }
    pub fn clear(&mut self) {
        self.map.clear();
    }
    pub fn size(&self) -> usize {
        self.map.len()
    }
    pub fn put(&mut self, key: String, value: String) {
        self.map.insert(key, value);
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
    }
}
