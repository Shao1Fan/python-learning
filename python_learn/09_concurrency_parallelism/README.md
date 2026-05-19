# 09 | 并发与并行

## 面试常见问题

- GIL 是什么？为什么有 GIL？
- GIL 对多线程和多进程各有什么影响？
- 什么时候用 threading，什么时候用 multiprocessing，什么时候用 asyncio？
- 线程安全与锁机制（Lock、RLock、Semaphore、Condition）？
- 进程间通信方式（Queue、Pipe、shared_memory）？
- concurrent.futures 的两种 Executor 的区别？

## 选择决策树

```
任务类型？
├── IO 密集型（网络、文件、数据库）
│   ├── 需要大量并发连接 → asyncio
│   └── 普通的阻塞 IO   → threading / concurrent.futures.ThreadPoolExecutor
│
├── CPU 密集型（计算、图像处理）
│   └── multiprocessing / concurrent.futures.ProcessPoolExecutor
│
└── 混合型
    └── 多进程 + asyncio（每个进程运行事件循环）
```

## 核心概念

| 概念 | threading | multiprocessing | asyncio |
|------|-----------|-----------------|---------|
| 执行单位 | 线程 | 进程 | 协程 |
| 内存共享 | 共享 | 独立 | 共享（单线程） |
| GIL 影响 | 有 | 无 | 无 |
| CPU 并行 | ❌ | ✅ | ❌ |
| IO 并行 | ✅ | ✅ | ✅ |
| 切换开销 | 中 | 高 | 极低 |
