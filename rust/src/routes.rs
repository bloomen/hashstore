use civet::response;
use conduit::{Request, Response, Handler};
use conduit_router::RequestParams;
use std::collections::HashMap;
use store::Store;
use std::error::Error;
use std::sync::{Arc, Mutex};
use std::io::Cursor;


static KEY: &'static str = "k";
static VALUE: &'static str = "v";
static INDEX: &'static str = "i";
static NIL: &'static str = "";


fn log_req(req: &Request) {
    print!("{} {}", req.remote_addr(), req.path());
    match req.query_string() {
        Some(value) => println!(" {}", value),
        None => println!(""),
    }
}


pub struct Clear {
    s: Arc<Mutex<Store>>,
}

impl Clear {
    pub fn new(s: Arc<Mutex<Store>>) -> Clear {
        Clear { s: s }
    }
}

impl Handler for Clear {
    fn call(&self, req: &mut Request) -> Result<Response, Box<Error + Send>> {
        log_req(req);
        let mut o = self.s.lock().unwrap();
        o.clear();
        Ok(response(200, HashMap::new(), NIL.as_bytes()))
    }
}


pub struct Size {
    s: Arc<Mutex<Store>>,
}

impl Size {
    pub fn new(s: Arc<Mutex<Store>>) -> Size {
        Size { s: s }
    }
}

impl Handler for Size {
    fn call(&self, req: &mut Request) -> Result<Response, Box<Error + Send>> {
        log_req(req);
        let o = self.s.lock().unwrap();
        let size = o.size().to_string();
        Ok(response(
            200,
            HashMap::new(),
            Cursor::new(size.as_bytes().to_owned()),
        ))
    }
}


pub struct Get {
    s: Arc<Mutex<Store>>,
}

impl Get {
    pub fn new(s: Arc<Mutex<Store>>) -> Get {
        Get { s: s }
    }
}

impl Handler for Get {
    fn call(&self, req: &mut Request) -> Result<Response, Box<Error + Send>> {
        log_req(req);
        let o = self.s.lock().unwrap();
        let key = req.params().find(KEY);
        let index = req.params().find(INDEX);
        if key.is_none() && index.is_none() {
            return Ok(response(400, HashMap::new(), NIL.as_bytes()));
        } else if key.is_some() {
            match o.get(&key.unwrap().to_string()) {
                Some(value) => Ok(response(
                    200,
                    HashMap::new(),
                    Cursor::new(value.as_bytes().to_owned()),
                )),
                None => Ok(response(204, HashMap::new(), NIL.as_bytes())), 
            }
        } else {
            let i = index.unwrap().to_string().parse::<usize>();
            if i.is_err() {
                return Ok(response(400, HashMap::new(), NIL.as_bytes()));
            } else {
                match o.key(i.unwrap()) {
                    Some(k) => Ok(response(
                        200,
                        HashMap::new(),
                        Cursor::new(k.as_bytes().to_owned()),
                    )),
                    None => Ok(response(204, HashMap::new(), NIL.as_bytes())), 
                }
            }
        }
    }
}


pub struct Put {
    s: Arc<Mutex<Store>>,
}

impl Put {
    pub fn new(s: Arc<Mutex<Store>>) -> Put {
        Put { s: s }
    }
}

impl Handler for Put {
    fn call(&self, req: &mut Request) -> Result<Response, Box<Error + Send>> {
        log_req(req);
        let mut o = self.s.lock().unwrap();
        let key = req.params().find(KEY);
        let value = req.params().find(VALUE);
        if key.is_none() || value.is_none() {
            return Ok(response(400, HashMap::new(), NIL.as_bytes()));
        } else {
            let k = key.unwrap().to_string();
            let v = value.unwrap().to_string();
            match o.get(&k) {
                Some(value) => {
                    o.put(k, v);
                    Ok(response(
                        205,
                        HashMap::new(),
                        Cursor::new(value.as_bytes().to_owned()),
                    ))
                }
                None => {
                    o.put(k, v);
                    Ok(response(200, HashMap::new(), NIL.as_bytes()))
                } 
            }
        }
    }
}


pub struct Remove {
    s: Arc<Mutex<Store>>,
}

impl Remove {
    pub fn new(s: Arc<Mutex<Store>>) -> Remove {
        Remove { s: s }
    }
}

impl Handler for Remove {
    fn call(&self, req: &mut Request) -> Result<Response, Box<Error + Send>> {
        log_req(req);
        let mut o = self.s.lock().unwrap();
        let key = req.params().find(KEY);
        if key.is_none() {
            return Ok(response(400, HashMap::new(), NIL.as_bytes()));
        } else {
            let k = key.unwrap().to_string();
            match o.get(&k) {
                Some(value) => {
                    o.remove(&k);
                    Ok(response(
                        200,
                        HashMap::new(),
                        Cursor::new(value.as_bytes().to_owned()),
                    ))
                }
                None => Ok(response(204, HashMap::new(), NIL.as_bytes())), 
            }
        }
    }
}
