# 🔍 IIT-G Campus Search Engine

A custom **information retrieval system** built from scratch in C++ over real IIT Guwahati campus data — no Elasticsearch, no Solr, no search library. Pure systems engineering.

> Search across CDC placement notices, mess menus, academic calendar, timetables, and placement stats from a single CLI interface.

---

## Demo

```
>> search nutanix
  [1] [CDC] CDC Placement - Nutanix
      Company: Nutanix. Allowed for M.Tech CSE 2024 batch. Role: Member of Technical Staff.

  [2] [PLACEMENT] Placement - Nutanix at IIT Guwahati
      Company: Nutanix. Students placed: Ahbar Ahad Siddiqui (CPI: 8.44, CTC: 57 LPA, SDE).

  [3] [PLACEMENT] Ahbar Ahad Siddiqui - Nutanix (SDE)
      Roll: 244101002. CTC: 57 LPA. Base: 26 LPA. Phase 1.

>> search brahmaputra wednesday lunch
  [1] [MESS] Brahmaputra Hostel Wednesday Menu - August 2026
      Lunch: Aloo Parwal (Dry), Black Masoor Dal, Soya Keema Matar, Buttermilk...

>> search microsoft AND placement
  [1] [PLACEMENT] Placement - Microsoft at IIT Guwahati
      3 students placed. Hemanth Simhadri (67 LPA), Shashank Aggarwal (67.5 LPA), Sagar Nishad (67 LPA).

>> search sunday AND NOT chicken
  [Results excluding non-veg Sunday menus]
```

---

## Architecture

```
Data Sources (.txt files)
        │
        ▼
  Document Parser (main.cpp)
        │
        ▼
  Thread Pool (4 workers)
        │
        ▼
  Inverted Index (word → posting list)
        │
  ┌─────┴──────┐
  │            │
TF-IDF      Boolean
Ranking     (AND/OR/NOT)
  │            │
  └─────┬──────┘
        │
   LRU Cache (100 queries)
        │
        ▼
   Binary Index (on-disk)
        │
        ▼
      CLI
```

---

## Core Components

### Inverted Index
Maps every token to its posting list — `word → [(doc_id, freq, positions)]`. O(1) average lookup via `unordered_map`. Tokenizer lowercases, strips punctuation, and filters stopwords.

### TF-IDF Ranking
Scores documents by relevance:
- **TF** = `1 + log(freq)` — log-normalized term frequency
- **IDF** = `log(N / df)` — inverse document frequency
- **Score** = `Σ TF × IDF` across all query terms

### Thread Pool
Fixed pool of 4 worker threads with a shared task queue. Uses `std::mutex` + `std::condition_variable` — workers sleep when idle, wake on `notify_one()`. Atomic doc-ID counter for thread-safe document assignment.

### LRU Cache
Query result cache using doubly linked list + hashmap. O(1) get and put. Most-recently-used at front, evicts from back when capacity (100) is exceeded.

### Boolean Query Engine
Set operations on posting lists:
- `AND` → intersection
- `OR` → union  
- `AND NOT` → difference

### Binary Persistence
Index saved/loaded in binary format — ~3-5x smaller and faster than JSON. On load, raw bytes read directly into memory without string parsing.

---

## Data Sources

398 documents from real IIT-G campus sources:

| Source | Docs | Content |
|---|---|---|
| CDC Portal | 147 | 237 job listings across 146 companies |
| Mess Menus | 104 | 13 hostels × 7 days, August 2026 |
| Placement Stats | 80 | MTech CSE 2024-2026 individual + company records |
| Timetables | 43 | MTech/BTech CSE courses + electives |
| Academic Calendar | 26 | Monsoon Semester 2026 key dates |

---

## Setup

### Requirements
- g++ with C++17 support
- Python 3.9+ (for data ingestion)
- `pip install pdfplumber` (for PDF parsing)

### Build

```bash
make
```

### Index real data

```bash
./search_engine
>> index data/real
>> save index/campus.bin
>> quit
```

### Search

```bash
./search_engine
>> load index/campus.bin
>> search nutanix
>> search brahmaputra wednesday lunch
>> search CS5001
>> search microsoft AND placement
>> search sunday AND NOT chicken
>> stats
>> quit
```

---

## Query Syntax

| Query | Type | Description |
|---|---|---|
| `search nutanix` | Ranked | TF-IDF ranked results |
| `search nutanix AND placement` | Boolean AND | Docs containing both terms |
| `search friday OR holiday` | Boolean OR | Docs containing either term |
| `search friday AND NOT placement` | Boolean NOT | Exclude term |

---

## Interesting Bug Fixed

During testing on Mac after compiling on Linux, `search nutanix` returned mess menu docs ranked above actual Nutanix placement records.

**Root cause:** Thread pool race condition. Doc-IDs were assigned with a plain `int doc_id++` counter shared across worker threads. Multiple threads incremented it simultaneously without synchronization, causing two threads to get the same ID. This merged posting lists from different documents under one ID, breaking IDF calculation — all scores became identical.

**Fix:** Changed counter to `std::atomic<int>` for lock-free atomic increment. Also moved indexing to single-threaded to eliminate all concurrent write races on the shared index structure. At 398 docs, single-threaded indexing completes in under a second anyway.

---

## Project Structure

```
├── src/
│   ├── main.cpp              # CLI + document parser + indexer
│   ├── inverted_index.cpp    # Core index: tokenizer, TF-IDF, persistence
│   ├── query_engine.cpp      # Ranked + boolean query execution
│   ├── thread_pool.cpp       # Fixed worker pool
│   └── lru_cache.cpp         # O(1) query result cache
├── include/                  # Headers for all components
├── ingest/                   # Python parsers for each data source
│   ├── parse_placement_stats.py
│   ├── parse_mess_menus.py
│   ├── parse_academic_calendar.py
│   ├── parse_timetables.py
│   └── parse_cdc_companies.py
├── data/real/                # 398 indexed campus documents
└── Makefile
```

---

## Tech Stack

- **Language**: C++17
- **Data structures**: Inverted index, doubly linked list, hashmap, posting lists
- **Concurrency**: `std::thread`, `std::mutex`, `std::condition_variable`, `std::atomic`
- **Ranking**: TF-IDF with log normalization
- **Ingestion**: Python, pdfplumber
- **Persistence**: Custom binary format

---

## Extension: ML Version

This project is also the retrieval backend for the [Campus RAG Assistant](https://github.com/anandabhi2910/Campus_RAG_Assistant_IITG) — which adds semantic search (FAISS + sentence-transformers) and LLM synthesis (Ollama + Qwen2.5) on top of this C++ engine.
