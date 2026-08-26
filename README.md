# Mini Redis

A lightweight in-memory Redis-style server implemented in C++.

## Features

- TCP server
- Non-blocking I/O
- Event-driven server loop
- In-memory hash table
- `GET`, `SET`, and `DEL`
- Key expiration with TTL
- Heap-based expiration management
- AVL tree
- Sorted sets
- Background thread pool
- Binary request/response protocol

## Project Structure

| File | Purpose |
|------|---------|
| `server.cpp` | Server, networking, event loop, command handling |
| `hashtable.cpp/h` | Hash table implementation |
| `avl.cpp/h` | AVL tree implementation |
| `zset.cpp/h` | Sorted-set implementation |
| `heap.cpp/h` | Expiration timer heap |
| `thread_pool.cpp/h` | Background worker pool |
| `list.h` | Doubly-linked list utilities |
| `common.h` | Shared utilities |
| `redis_test.py` | Integration test client |

## Requirements

- Linux or WSL
- `g++`
- Python 3

## Build

```bash
g++ -std=c++11 -pthread -o redis_server \
    server.cpp \
    avl.cpp \
    hashtable.cpp \
    heap.cpp \
    thread_pool.cpp \
    zset.cpp
