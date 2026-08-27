#pragma once
#include "types.h"
#include <unordered_map>
#include <vector>
#include <string>
#include <mutex>

class InvertedIndex {
public:
    // Add a document to the index
    void add_document(const Document& doc);

    // Get posting list for a term
    const std::vector<PostingEntry>* get_postings(const std::string& term) const;

    // TF-IDF score for a term in a document
    float tfidf_score(const std::string& term, int doc_id) const;

    // Save index to binary file
    void save(const std::string& path) const;

    // Load index from binary file
    void load(const std::string& path);

    int total_docs() const { return documents_.size(); }
    const Document* get_document(int doc_id) const;
    const std::unordered_map<std::string, std::vector<PostingEntry>>& get_index() const { return index_; }

private:
    // word → posting list
    std::unordered_map<std::string, std::vector<PostingEntry>> index_;

    // doc_id → Document
    std::vector<Document> documents_;

    // term → number of docs containing that term (for IDF)
    std::unordered_map<std::string, int> doc_frequency_;

    // Protects index_ during concurrent writes from thread pool
    mutable std::mutex mutex_;

    // Tokenize text into lowercase terms, strip punctuation
    std::vector<std::string> tokenize(const std::string& text) const;

    // Common English stopwords to skip during indexing
    bool is_stopword(const std::string& word) const;
};
