#pragma once
#include "inverted_index.h"
#include "lru_cache.h"
#include "types.h"
#include <string>
#include <vector>

class QueryEngine {
public:
    explicit QueryEngine(InvertedIndex& index, LRUCache& cache);

    // Main entry: parse and execute a query, return ranked results
    std::vector<SearchResult> search(const std::string& query, int top_k = 10);

private:
    InvertedIndex& index_;
    LRUCache& cache_;

    // Ranked TF-IDF search (default)
    std::vector<SearchResult> ranked_search(const std::vector<std::string>& terms, int top_k);

    // Boolean AND: docs containing ALL terms
    std::vector<SearchResult> boolean_and(const std::vector<std::string>& terms);

    // Boolean OR: docs containing ANY term
    std::vector<SearchResult> boolean_or(const std::vector<std::string>& terms);

    // Detect if query is a boolean query ("AND", "OR", "NOT" keywords)
    bool is_boolean_query(const std::string& query) const;

    // Parse boolean query into operator + terms
    std::vector<SearchResult> execute_boolean(const std::string& query);

    // Build a snippet from document body
    std::string make_snippet(const std::string& body, int max_len = 150) const;

    // Tokenize query into terms
    std::vector<std::string> tokenize(const std::string& query) const;
};
