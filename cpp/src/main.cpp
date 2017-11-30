#include <served/served.hpp>
#include "store.h"
#include "routes.h"


int main() {
    store s;

    served::multiplexer mux;
    mux.use_before([](served::response&, served::request& req) {
        std::cout << req.source() << " " << req.url().URI() << std::flush;
    });
    mux.use_after([](served::response& res, served::request&) {
        std::cout << " " << res.status() << std::endl;
    });

    mux.handle("/clear").get(routes::clear{s});
    mux.handle("/size").get(routes::size{s});
    mux.handle("/get").get(routes::get{s});
    mux.handle("/put").get(routes::put{s});
    mux.handle("/remove").get(routes::remove{s});

    const std::string host = "127.0.0.1";
    const std::string port = "5002";
    served::net::server server(host, port, mux);
    std::cout << "Serving on " << host << ":" << port << std::endl;
    server.run();
}
