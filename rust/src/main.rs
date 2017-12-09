extern crate civet;
extern crate conduit;
extern crate conduit_router;

mod store;
use store::Store;

mod routes;

use std::sync::mpsc::channel;
use std::sync::{Arc, Mutex};

use civet::{Config, Server};
use conduit_router::RouteBuilder;


fn main() {
    let s = Arc::new(Mutex::new(Store::new()));

    let port = 5003;
    let host = "127.0.0.1";

    let mut router = RouteBuilder::new();

    router.get("/clear", routes::Clear::new(s.clone()));
    router.get("/size", routes::Size::new(s.clone()));
    router.get("/get", routes::Get::new(s.clone()));
    router.get("/put", routes::Put::new(s.clone()));
    router.get("/remove", routes::Remove::new(s.clone()));

    let mut cfg = Config::new();
    cfg.port(port).threads(1);
    let _server = Server::start(cfg, router);

    println!("Serving on {}:{}", host, port);

    // Preventing process exit.
    let (_tx, rx) = channel::<()>();
    rx.recv().unwrap();
}
