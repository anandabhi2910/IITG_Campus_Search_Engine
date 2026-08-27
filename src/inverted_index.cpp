#include "inverted_index.h"
#include <algorithm>
#include <cctype>
#include <cmath>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <unordered_set>

// ── Stopwords ────────────────────────────────────────────────────────────────
bool InvertedIndex::is_stopword(const std::string& word) const {
    static const std::unordered_set<std::string> stopwords = {
        "a","an","the","is","it","in","on","at","to","of","and","or","for",
        "with","by","from","as","be","was","are","were","has","have","had",
        "this","that","these","those","will","would","can","could","should",
        "may","might","do","does","did","not","but","so","if","then","than",
        "its","their","our","your","my","his","her","we","they","he","she","i"
    };
    return stopwords.count(word) > 0;
}

// ── Tokenizer ────────────────────────────────────────────────────────────────
std::vector<std::string> InvertedIndex::tokenize(const std::string& text) const {
    std::vector<std::string> tokens;
    std::string token;

    for (char c : text) {
        if (std::isalnum(c)) {
            token += std::tolower(c);
        } else {
            if (!token.empty()) {
                if (token.size() > 1 && !is_stopword(token))
                    tokens.push_back(token);
                token.clear();
            }
        }
    }
    if (!token.empty() && token.size() > 1 && !is_stopword(token))
        tokens.push_back(token);

    return tokens;
}

// ── Add document ─────────────────────────────────────────────────────────────
// Called from thread pool workers — mutex protects shared state
void InvertedIndex::add_document(const Document& doc) {
    // Tokenize outside the lock (CPU work, no shared state touched)
    std::string full_text = doc.title + " " + doc.body;
    auto tokens = tokenize(full_text);

    // Build local freq map and positions — no lock needed yet
    std::unordered_map<std::string, PostingEntry> local;
    for (int pos = 0; pos < (int)tokens.size(); ++pos) {
        const std::string& t = tokens[pos];
        auto& entry = local[t];
        entry.doc_id = doc.id;
        entry.frequency++;
        entry.positions.push_back(pos);
    }

    // Lock only when writing to shared index
    std::lock_guard<std::mutex> lock(mutex_);

    documents_.push_back(doc);

    for (auto& [term, entry] : local) {
        index_[term].push_back(entry);
        doc_frequency_[term]++;
    }
}

// ── Lookup ───────────────────────────────────────────────────────────────────
const std::vector<PostingEntry>* InvertedIndex::get_postings(const std::string& term) const {
    auto it = index_.find(term);
    if (it == index_.end()) return nullptr;
    return &it->second;
}

const Document* InvertedIndex::get_document(int doc_id) const {
    if (doc_id < 0 || doc_id >= (int)documents_.size()) return nullptr;
    return &documents_[doc_id];
}

// ── TF-IDF scoring ───────────────────────────────────────────────────────────
// TF  = freq / total tokens in doc  (normalized term frequency)
// IDF = log(N / df)                 (inverse document frequency)
float InvertedIndex::tfidf_score(const std::string& term, int doc_id) const {
    auto it = index_.find(term);
    if (it == index_.end()) return 0.0f;

    // Find posting for this doc
    const PostingEntry* posting = nullptr;
    for (const auto& p : it->second) {
        if (p.doc_id == doc_id) { posting = &p; break; }
    }
    if (!posting) return 0.0f;

    // TF: raw freq (simple version — good enough at small scale)
    // float tf = static_cast<float>(posting->frequency);
    // float tf = static_cast<float>(posting->frequency) / 
    //        static_cast<float>(posting->positions.size() > 0 ? 
    //        posting->positions.back() + 1 : 1);
    float tf = 1.0f + std::log(static_cast<float>(posting->frequency));

    // IDF: log(total_docs / docs_with_term) — add 1 to avoid div-by-zero
    int df = doc_frequency_.count(term) ? doc_frequency_.at(term) : 1;
    float idf = std::log(static_cast<float>(documents_.size() + 1) /
                         static_cast<float>(df + 1));

    return tf * idf;
}

// ── Persistence: Save ────────────────────────────────────────────────────────
// Binary format: faster load than JSON, ~3x smaller
void InvertedIndex::save(const std::string& path) const {
    std::ofstream out(path, std::ios::binary);
    if (!out) throw std::runtime_error("Cannot open file for writing: " + path);

    // Write documents
    int num_docs = documents_.size();
    out.write(reinterpret_cast<const char*>(&num_docs), sizeof(int));
    for (const auto& doc : documents_) {
        auto write_str = [&](const std::string& s) {
            int len = s.size();
            out.write(reinterpret_cast<const char*>(&len), sizeof(int));
            out.write(s.data(), len);
        };
        out.write(reinterpret_cast<const char*>(&doc.id), sizeof(int));
        write_str(doc.source);
        write_str(doc.date);
        write_str(doc.title);
        write_str(doc.body);
        write_str(doc.filepath);
    }

    // Write index
    int num_terms = index_.size();
    out.write(reinterpret_cast<const char*>(&num_terms), sizeof(int));
    for (const auto& [term, postings] : index_) {
        int tlen = term.size();
        out.write(reinterpret_cast<const char*>(&tlen), sizeof(int));
        out.write(term.data(), tlen);

        int num_postings = postings.size();
        out.write(reinterpret_cast<const char*>(&num_postings), sizeof(int));
        for (const auto& p : postings) {
            out.write(reinterpret_cast<const char*>(&p.doc_id), sizeof(int));
            out.write(reinterpret_cast<const char*>(&p.frequency), sizeof(int));
            int np = p.positions.size();
            out.write(reinterpret_cast<const char*>(&np), sizeof(int));
            out.write(reinterpret_cast<const char*>(p.positions.data()), np * sizeof(int));
        }
    }

    // Write doc_frequency
    int num_df = doc_frequency_.size();
    out.write(reinterpret_cast<const char*>(&num_df), sizeof(int));
    for (const auto& [term, freq] : doc_frequency_) {
        int tlen = term.size();
        out.write(reinterpret_cast<const char*>(&tlen), sizeof(int));
        out.write(term.data(), tlen);
        out.write(reinterpret_cast<const char*>(&freq), sizeof(int));
    }
}

// ── Persistence: Load ────────────────────────────────────────────────────────
void InvertedIndex::load(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    if (!in) throw std::runtime_error("Cannot open index file: " + path);

    auto read_str = [&]() {
        int len; in.read(reinterpret_cast<char*>(&len), sizeof(int));
        std::string s(len, '\0');
        in.read(s.data(), len);
        return s;
    };

    // Read documents
    int num_docs; in.read(reinterpret_cast<char*>(&num_docs), sizeof(int));
    documents_.resize(num_docs);
    for (auto& doc : documents_) {
        in.read(reinterpret_cast<char*>(&doc.id), sizeof(int));
        doc.source   = read_str();
        doc.date     = read_str();
        doc.title    = read_str();
        doc.body     = read_str();
        doc.filepath = read_str();
    }

    // Read index
    int num_terms; in.read(reinterpret_cast<char*>(&num_terms), sizeof(int));
    for (int i = 0; i < num_terms; ++i) {
        std::string term = read_str();
        int num_postings; in.read(reinterpret_cast<char*>(&num_postings), sizeof(int));
        std::vector<PostingEntry> postings(num_postings);
        for (auto& p : postings) {
            in.read(reinterpret_cast<char*>(&p.doc_id), sizeof(int));
            in.read(reinterpret_cast<char*>(&p.frequency), sizeof(int));
            int np; in.read(reinterpret_cast<char*>(&np), sizeof(int));
            p.positions.resize(np);
            in.read(reinterpret_cast<char*>(p.positions.data()), np * sizeof(int));
        }
        index_[term] = std::move(postings);
    }

    // Read doc_frequency
    int num_df; in.read(reinterpret_cast<char*>(&num_df), sizeof(int));
    for (int i = 0; i < num_df; ++i) {
        std::string term = read_str();
        int freq; in.read(reinterpret_cast<char*>(&freq), sizeof(int));
        doc_frequency_[term] = freq;
    }
}
