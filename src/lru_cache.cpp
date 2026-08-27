#include "lru_cache.h"

LRUCache::LRUCache(size_t capacity) : capacity_(capacity) {}

// Get: O(1) — hashmap lookup + move to front
std::optional<std::vector<SearchResult>> LRUCache::get(const std::string& query) {
    std::lock_guard<std::mutex> lock(mutex_);

    auto it = cache_map_.find(query);
    if (it == cache_map_.end()) return std::nullopt;  // cache miss

    // Move accessed entry to front (most recently used)
    cache_list_.splice(cache_list_.begin(), cache_list_, it->second);
    return it->second->second;  // cache hit
}

// Put: O(1) — insert at front, evict from back if over capacity
void LRUCache::put(const std::string& query, const std::vector<SearchResult>& results) {
    std::lock_guard<std::mutex> lock(mutex_);

    auto it = cache_map_.find(query);
    if (it != cache_map_.end()) {
        // Already cached — update and move to front
        it->second->second = results;
        cache_list_.splice(cache_list_.begin(), cache_list_, it->second);
        return;
    }

    // Insert new entry at front
    cache_list_.emplace_front(query, results);
    cache_map_[query] = cache_list_.begin();

    // Evict LRU entry (back of list) if over capacity
    if (cache_map_.size() > capacity_) {
        auto last = cache_list_.end();
        --last;
        cache_map_.erase(last->first);
        cache_list_.pop_back();
    }
}

void LRUCache::clear() {
    std::lock_guard<std::mutex> lock(mutex_);
    cache_list_.clear();
    cache_map_.clear();
}
