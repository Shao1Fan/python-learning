# 04 | 异步编程 (Async Programming)

## 面试常见问题

- `async def` 和 `def` 的区别？什么是协程？
- `await` 在等待什么？await 后面可以跟什么？
- 事件循环 (event loop) 的工作原理？
- `asyncio.gather` vs `asyncio.create_task`?
- 协程、线程、进程的区别与选择？
- GIL 和 asyncio 的关系？
- async 上下文管理器 / async 迭代器怎么写？
- 什么时候用 async 什么时候用 threading？

## 核心概念

```
协程 (Coroutine)         ← async def 定义的函数调用返回
  └── await 表达式       ← 等待另一个协程完成，让出控制权

事件循环 (Event Loop)    ← 调度所有协程的核心引擎
  ├── 注册协程
  ├── 调度执行
  └── 处理 IO 就绪事件

Task                     ← 协程的"包装"，用于并发调度
  └── asyncio.create_task()

Future                   ← 异步结果的"占位符"
  └── 低层接口，Task 是 Future 的子类
```

## 关键对比

| 特性 | threading | multiprocessing | asyncio |
|------|-----------|-----------------|---------|
| 并行 | ❌ (GIL) | ✅ | ❌ (单线程) |
| 并发 | ✅ | ✅ | ✅ |
| IO 密集型 | ✅ | ⚠️  | ✅✅ |
| CPU 密集型 | ❌ | ✅ | ❌ |
| 开销 | 中 | 高 | 低 |
| 共享数据 | 需锁 | 需 IPC | 天然安全 |
