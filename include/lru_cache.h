#pragma once
#include "types.h"
#include <list>
#include <unordered_map>
#include <string>
#include <vector>
#include <optional>
#include <mutex>

class LRUCache {
public:
    explicit LRUCache(size_t capacity);

    // Get cached results for a query string
    std::optional<std::vector<SearchResult>> get(const std::string& query);

    // Store results for a query string
    void put(const std::string& query, const std::vector<SearchResult>& results);

    void clear();
    size_t size() const { return cache_map_.size(); }

private:
    size_t capacity_;

    // List stores (query, results) — front = most recently used
    std::list<std::pair<std::string, std::vector<SearchResult>>> cache_list_;

    // Map: query → iterator into cache_list_ for O(1) access
    std::unordered_map<std::string,
        std::list<std::pair<std::string, std::vector<SearchResult>>>::iterator> cache_map_;

    mutable std::mutex mutex_;
};
