#pragma once
#include <string>
#include <vector>

// One entry in a posting list: which doc, how often, where
struct PostingEntry {
    int doc_id;
    int frequency;
    std::vector<int> positions;
};

// A document in the corpus
struct Document {
    int id;
    std::string source;   // "CDC", "NOTICE", "MESS", "TIMETABLE"
    std::string date;
    std::string title;
    std::string body;
    std::string filepath; // original file path
};

// A query result returned to the user
struct SearchResult {
    int doc_id;
    float score;
    std::string source;
    std::string date;
    std::string title;
    std::string snippet;  // first 150 chars of body
};
