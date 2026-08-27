#include "inverted_index.h"
#include "thread_pool.h"
#include "lru_cache.h"
#include "query_engine.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <filesystem>
#include <string>
#include <atomic>

namespace fs = std::filesystem;

// ── Document parser ───────────────────────────────────────────────────────────
// Reads plain text files in this format:
//   SOURCE: CDC
//   DATE: 2026-08-20
//   TITLE: Nutanix Placement Drive
//   BODY: Full text of the notice...
Document parse_doc_file(const std::string& filepath, int doc_id) {
    Document doc;
    doc.id = doc_id;
    doc.filepath = filepath;

    std::ifstream file(filepath);
    if (!file) throw std::runtime_error("Cannot open: " + filepath);

    std::string line;
    bool in_body = false;
    std::ostringstream body_stream;

    while (std::getline(file, line)) {
        if (in_body) {
            body_stream << line << "\n";
        } else if (line.substr(0, 7) == "SOURCE:") {
            doc.source = line.substr(8);
        } else if (line.substr(0, 5) == "DATE:") {
            doc.date = line.substr(6);
        } else if (line.substr(0, 6) == "TITLE:") {
            doc.title = line.substr(7);
        } else if (line.substr(0, 5) == "BODY:") {
            in_body = true;
            body_stream << line.substr(6) << "\n";
        }
    }
    doc.body = body_stream.str();
    return doc;
}

// ── Indexer ───────────────────────────────────────────────────────────────────
void index_data_dir(const std::string& data_dir, InvertedIndex& index) {
    ThreadPool pool(4);  // 4 worker threads
    // int doc_id = 0;
    std::atomic<int> doc_id{0};

    std::cout << "[Indexer] Scanning: " << data_dir << "\n";

    for (const auto& entry : fs::recursive_directory_iterator(data_dir)) {
        if (entry.path().extension() != ".txt") continue;

        int id = doc_id++;
        std::string path = entry.path().string();

        // Enqueue indexing task — runs in parallel across 4 threads
        // pool.enqueue([&index, path, id]() {
            try {
                Document doc = parse_doc_file(path, id);
                index.add_document(doc);
                std::cout << "  [+] " << doc.source << " | " << doc.title << "\n";
            } catch (const std::exception& e) {
                std::cerr << "  [!] Error indexing " << path << ": " << e.what() << "\n";
            }
        // });
    }

    // pool.wait_all();
    std::cout << "[Indexer] Done. " << index.total_docs() << " documents indexed.\n";
}

// ── CLI ───────────────────────────────────────────────────────────────────────
void print_results(const std::vector<SearchResult>& results) {
    if (results.empty()) {
        std::cout << "  No results found.\n";
        return;
    }
    for (int i = 0; i < (int)results.size(); ++i) {
        const auto& r = results[i];
        std::cout << "\n  [" << i+1 << "] [" << r.source << "] [" << r.date << "] "
                  << r.title << "\n"
                  << "      Score: " << r.score << "\n"
                  << "      " << r.snippet << "\n";
    }
}

void print_help() {
    std::cout << "\nCommands:\n"
              << "  index <data_dir>     Index all .txt docs in a directory\n"
              << "  save  <index_file>   Save index to binary file\n"
              << "  load  <index_file>   Load index from binary file\n"
              << "  search <query>       Ranked TF-IDF search\n"
              << "  search nutanix AND placement   Boolean AND\n"
              << "  search friday OR holiday       Boolean OR\n"
              << "  search friday AND NOT placement Boolean AND NOT\n"
              << "  stats                Show index statistics\n"
              << "  help                 Show this message\n"
              << "  quit                 Exit\n\n";
}

int main() {
    InvertedIndex index;
    LRUCache cache(100);          // cache last 100 query results
    QueryEngine engine(index, cache);

    std::cout << "╔══════════════════════════════════════╗\n"
              << "║   IIT-G Campus Search Engine v1.0   ║\n"
              << "╚══════════════════════════════════════╝\n";
    print_help();

    std::string line;
    while (true) {
        std::cout << ">> ";
        if (!std::getline(std::cin, line)) break;
        if (line.empty()) continue;

        // Parse command
        std::string cmd, arg;
        auto space = line.find(' ');
        if (space != std::string::npos) {
            cmd = line.substr(0, space);
            arg = line.substr(space + 1);
        } else {
            cmd = line;
        }

        if (cmd == "quit" || cmd == "exit" || cmd == "q") {
            std::cout << "Goodbye.\n";
            break;

        } else if (cmd == "index") {
            if (arg.empty()) { std::cout << "Usage: index <data_dir>\n"; continue; }
            index_data_dir(arg, index);

        } else if (cmd == "save") {
            if (arg.empty()) { std::cout << "Usage: save <file>\n"; continue; }
            index.save(arg);
            std::cout << "Index saved to: " << arg << "\n";

        } else if (cmd == "load") {
            if (arg.empty()) { std::cout << "Usage: load <file>\n"; continue; }
            index.load(arg);
            std::cout << "Index loaded. " << index.total_docs() << " docs.\n";

        } else if (cmd == "search") {
            if (arg.empty()) { std::cout << "Usage: search <query>\n"; continue; }
            auto results = engine.search(arg);
            print_results(results);

        } else if (cmd == "stats") {
            std::cout << "  Documents indexed: " << index.total_docs() << "\n"
                      << "  Cache size: " << cache.size() << "/100\n";

        } else if (cmd == "help") {
            print_help();

        } else {
            std::cout << "Unknown command. Type 'help'.\n";
        }
    }
    return 0;
}
