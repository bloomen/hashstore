#pragma once
#include <unordered_map>
#include <string>
#include <fstream>
#include <cstddef>
#include <sstream>
#include <vector>
#include <boost/optional.hpp>
#include <boost/serialization/serialization.hpp>
#include <boost/serialization/unordered_map.hpp>
#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/text_oarchive.hpp>


class store {
public:

    store() {
        std::ifstream file(filename_);
        if (file.good()) {
            boost::archive::text_iarchive iarch(file);
            iarch >> map_;
        }
    }

    void clear() {
        map_.clear();
        save();
    }

    std::size_t size() const {
        return map_.size();
    }

    void put(const std::string& key, const std::string& value) {
        map_[key] = value;
        save();
    }

    boost::optional<std::string> get(const std::string& key) const {
        auto iter = map_.find(key);
        if (iter != map_.end()) {
            return iter->second;
        }
        return {};
    }

    boost::optional<std::string> key(std::size_t index) const {
        std::size_t i = 0;
        for (const auto& pair : map_) {
            if (i == index) {
                return pair.first;
            }
            ++i;
        }
        return {};
    }

    void remove(const std::string& key) {
        map_.erase(key);
        save();
    }

private:

    void save() {
        std::ofstream file(filename_);
        boost::archive::text_oarchive oarch(file);
        oarch << map_;
    }

    std::unordered_map<std::string, std::string> map_;
    std::string filename_ = "hashstore.db";
};
