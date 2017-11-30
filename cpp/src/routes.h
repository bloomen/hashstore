#pragma once
#include "store.h"
#include <served/served.hpp>
#include <iostream>


namespace routes {


const std::string KEY = "k";
const std::string VALUE = "v";
const std::string INDEX = "i";
const std::string NIL = "";


struct clear {
    clear(store& s) : s_(s) {}
    void operator()(served::response& res, const served::request&) {
        const auto size = s_.size();
        s_.clear();
        res.set_status(200);
        res << std::to_string(size);
    }
private:
    store& s_;
};


struct size {
    size(store& s) : s_(s) {}
    void operator()(served::response& res, const served::request&) {
        res << std::to_string(s_.size());
        res.set_status(200);
    }
private:
    store& s_;
};


struct get {
    get(store& s) : s_(s) {}
    void operator()(served::response& res, const served::request& req) {
        const auto key = req.query.get(KEY);
        const auto index = req.query.get(INDEX);
        if (key.empty() && index.empty()) {
            res.set_status(400);
            return;
        }
        if (!key.empty()) {
            const auto value = s_.get(key);
            if (value) {
                res << *value;
                res.set_status(200);
                return;
            } else {
                res << NIL;
                res.set_status(204);
                return;
            }
        }
        if (!index.empty()) {
            std::size_t ind;
            std::stringstream ss(index);
            if (!(ss >> ind)) {
                res.set_status(400);
                return;
            }
            const auto k = s_.key(ind);
            if (k) {
                res << *k;
                res.set_status(200);
                return;
            } else {
                res << NIL;
                res.set_status(204);
                return;
            }
        }
    }
private:
    store& s_;
};


struct put {
    put(store& s) : s_(s) {}
    void operator()(served::response& res, const served::request& req) {
        const auto key = req.query.get(KEY);
        const auto value = req.query.get(VALUE);
        if (key.empty() || value.empty()) {
            res.set_status(400);
            return;
        }
        const auto old_value = s_.get(key);
        s_.put(key, value);
        if (old_value) {
            res << *old_value;
            res.set_status(205);
            return;
        } else {
            res << NIL;
            res.set_status(200);
            return;
        }
    }
private:
    store& s_;
};


struct remove {
    remove(store& s) : s_(s) {}
    void operator()(served::response& res, const served::request& req) {
        const auto key = req.query.get(KEY);
        if (key.empty()) {
            res.set_status(400);
            return;
        }
        const auto old_value = s_.get(key);
        if (old_value) {
            s_.remove(key);
            res << *old_value;
            res.set_status(200);
            return;
        } else {
            res << NIL;
            res.set_status(204);
            return;
        }
    }
private:
    store& s_;
};


}
