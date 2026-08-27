CXX      = g++
CXXFLAGS = -std=c++17 -O2 -Wall -Iinclude
LDFLAGS  = -lpthread

SRC = src/main.cpp src/inverted_index.cpp src/thread_pool.cpp \
      src/lru_cache.cpp src/query_engine.cpp

TARGET = search_engine

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET) $(LDFLAGS)

clean:
	rm -f $(TARGET) index/*.bin

.PHONY: all clean
