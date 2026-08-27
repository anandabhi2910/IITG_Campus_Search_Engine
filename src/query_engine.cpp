#include "query_engine.h"
#include <algorithm>
#include <cctype>
#include <sstream>
#include <unordered_map>
#include <unordered_set>

QueryEngine::QueryEngine(InvertedIndex& index, LRUCache& cache)
    : index_(index), cache_(cache) {}

// ── Tokenizer (same logic as indexer) ────────────────────────────────────────
std::vector<std::string> QueryEngine::tokenize(const std::string& query) const {
    std::vector<std::string> tokens;
    std::string token;
    for (char c : query) {
        if (std::isalnum(c)) token += std::tolower(c);
        else {
            if (!token.empty()) { tokens.push_back(token); token.clear(); }
        }
    }
    if (!token.empty()) tokens.push_back(token);
    return tokens;
}

// ── Snippet builder ───────────────────────────────────────────────────────────
std::string QueryEngine::make_snippet(const std::string& body, int max_len) const {
    if ((int)body.size() <= max_len) return body;
    return body.substr(0, max_len) + "...";
}

// ── Detect boolean query ──────────────────────────────────────────────────────
bool QueryEngine::is_boolean_query(const std::string& query) const {
    return query.find(" AND ") != std::string::npos ||
           query.find(" OR ")  != std::string::npos ||
           query.find(" NOT ") != std::string::npos;
}

// ── Ranked TF-IDF search ─────────────────────────────────────────────────────
std::vector<SearchResult> QueryEngine::ranked_search(
        const std::vector<std::string>& terms, int top_k) {

    // Accumulate TF-IDF scores per doc across all query terms
    std::unordered_map<int, float> scores;

    for (const auto& term : terms) {
        const auto* postings = index_.get_postings(term);
        if (!postings) continue;
        for (const auto& p : *postings) {
            scores[p.doc_id] += index_.tfidf_score(term, p.doc_id);
        }
    }

    // Sort by score descending
    std::vector<std::pair<int, float>> ranked(scores.begin(), scores.end());
    std::sort(ranked.begin(), ranked.end(),
              [](const auto& a, const auto& b) { return a.second > b.second; });

    // Build results
    std::vector<SearchResult> results;
    for (int i = 0; i < std::min((int)ranked.size(), top_k); ++i) {
        const Document* doc = index_.get_document(ranked[i].first);
        if (!doc) continue;
        SearchResult r;
        r.doc_id  = doc->id;
        r.score   = ranked[i].second;
        r.source  = doc->source;
        r.date    = doc->date;
        r.title   = doc->title;
        r.snippet = make_snippet(doc->body);
        results.push_back(r);
    }
    return results;
}

// ── Boolean AND ──────────────────────────────────────────────────────────────
// Returns docs that contain ALL terms (set intersection on posting lists)
std::vector<SearchResult> QueryEngine::boolean_and(const std::vector<std::string>& terms) {
    if (terms.empty()) return {};

    // Start with doc set from first term
    std::unordered_set<int> result_set;
    const auto* first = index_.get_postings(terms[0]);
    if (!first) return {};
    for (const auto& p : *first) result_set.insert(p.doc_id);

    // Intersect with each subsequent term
    for (size_t i = 1; i < terms.size(); ++i) {
        const auto* postings = index_.get_postings(terms[i]);
        if (!postings) return {};
        std::unordered_set<int> term_docs;
        for (const auto& p : *postings) term_docs.insert(p.doc_id);
        // Keep only docs in both sets
        for (auto it = result_set.begin(); it != result_set.end(); ) {
            if (!term_docs.count(*it)) it = result_set.erase(it);
            else ++it;
        }
    }

    std::vector<SearchResult> results;
    for (int doc_id : result_set) {
        const Document* doc = index_.get_document(doc_id);
        if (!doc) continue;
        SearchResult r;
        r.doc_id  = doc->id;
        r.score   = 1.0f;
        r.source  = doc->source;
        r.date    = doc->date;
        r.title   = doc->title;
        r.snippet = make_snippet(doc->body);
        results.push_back(r);
    }
    return results;
}

// ── Boolean OR ───────────────────────────────────────────────────────────────
// Returns docs containing ANY term (set union)
std::vector<SearchResult> QueryEngine::boolean_or(const std::vector<std::string>& terms) {
    std::unordered_set<int> seen;
    std::vector<SearchResult> results;

    for (const auto& term : terms) {
        const auto* postings = index_.get_postings(term);
        if (!postings) continue;
        for (const auto& p : *postings) {
            if (seen.insert(p.doc_id).second) {
                const Document* doc = index_.get_document(p.doc_id);
                if (!doc) continue;
                SearchResult r;
                r.doc_id  = doc->id;
                r.score   = index_.tfidf_score(term, p.doc_id);
                r.source  = doc->source;
                r.date    = doc->date;
                r.title   = doc->title;
                r.snippet = make_snippet(doc->body);
                results.push_back(r);
            }
        }
    }
    return results;
}

// ── Boolean query parser ──────────────────────────────────────────────────────
// Supports: "term1 AND term2", "term1 OR term2", "term1 AND NOT term2"
std::vector<SearchResult> QueryEngine::execute_boolean(const std::string& query) {
    // Simple parser: detect operator, split terms
    if (query.find(" AND NOT ") != std::string::npos) {
        auto pos = query.find(" AND NOT ");
        std::string left  = query.substr(0, pos);
        std::string right = query.substr(pos + 9);

        // Get AND results, then exclude NOT results
        auto and_results = boolean_and(tokenize(left));
        const auto* not_postings = index_.get_postings(right);
        if (!not_postings) return and_results;

        std::unordered_set<int> excluded;
        for (const auto& p : *not_postings) excluded.insert(p.doc_id);

        std::vector<SearchResult> filtered;
        for (const auto& r : and_results)
            if (!excluded.count(r.doc_id)) filtered.push_back(r);
        return filtered;
    }

    if (query.find(" AND ") != std::string::npos) {
        std::vector<std::string> terms;
        std::stringstream ss(query);
        std::string part;
        while (std::getline(ss, part, ' ')) {
            if (part != "AND") terms.push_back(part);
        }
        return boolean_and(terms);
    }

    if (query.find(" OR ") != std::string::npos) {
        std::vector<std::string> terms;
        std::stringstream ss(query);
        std::string part;
        while (std::getline(ss, part, ' ')) {
            if (part != "OR") terms.push_back(part);
        }
        return boolean_or(terms);
    }

    return {};
}

// ── Main search entry point ───────────────────────────────────────────────────
std::vector<SearchResult> QueryEngine::search(const std::string& query, int top_k) {
    // Check LRU cache first
    auto cached = cache_.get(query);
    if (cached.has_value()) return cached.value();

    std::vector<SearchResult> results;

    if (is_boolean_query(query)) {
        results = execute_boolean(query);
    } else {
        auto terms = tokenize(query);
        results = ranked_search(terms, top_k);
    }

    // Store in cache for next time
    cache_.put(query, results);
    return results;
}
