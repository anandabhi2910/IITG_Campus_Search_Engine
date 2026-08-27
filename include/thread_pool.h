#pragma once
#include <vector>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <atomic>

class ThreadPool {
public:
    explicit ThreadPool(size_t num_threads);
    ~ThreadPool();

    // Enqueue a task (any callable)
    void enqueue(std::function<void()> task);

    // Block until all tasks are done
    void wait_all();

private:
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> task_queue_;

    std::mutex queue_mutex_;
    std::condition_variable cv_;
    std::atomic<bool> stop_;
    std::atomic<int> active_tasks_;   // tasks currently running
    std::condition_variable done_cv_; // signals when active_tasks_ hits 0
    std::mutex done_mutex_;

    void worker_loop();
};
