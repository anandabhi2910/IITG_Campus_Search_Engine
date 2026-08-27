#include "thread_pool.h"

ThreadPool::ThreadPool(size_t num_threads) : stop_(false), active_tasks_(0) {
    for (size_t i = 0; i < num_threads; ++i)
        workers_.emplace_back(&ThreadPool::worker_loop, this);
}

ThreadPool::~ThreadPool() {
    stop_ = true;
    cv_.notify_all();       // wake all sleeping workers so they can exit
    for (auto& t : workers_)
        if (t.joinable()) t.join();
}

void ThreadPool::enqueue(std::function<void()> task) {
    {
        std::lock_guard<std::mutex> lock(queue_mutex_);
        task_queue_.push(std::move(task));
    }
    cv_.notify_one();       // wake one sleeping worker
}

void ThreadPool::wait_all() {
    std::unique_lock<std::mutex> lock(done_mutex_);
    // Sleep until: queue empty AND no active tasks
    done_cv_.wait(lock, [this] {
        std::lock_guard<std::mutex> q(queue_mutex_);
        return task_queue_.empty() && active_tasks_ == 0;
    });
}

void ThreadPool::worker_loop() {
    while (true) {
        std::function<void()> task;
        {
            std::unique_lock<std::mutex> lock(queue_mutex_);
            // Sleep here (no CPU burned) until there's work or we're stopping
            cv_.wait(lock, [this] {
                return !task_queue_.empty() || stop_.load();
            });

            if (stop_ && task_queue_.empty()) return;

            task = std::move(task_queue_.front());
            task_queue_.pop();
            active_tasks_++;
        }

        task();   // do the actual work (outside the lock)

        active_tasks_--;
        done_cv_.notify_all();  // signal wait_all() if it's waiting
    }
}
