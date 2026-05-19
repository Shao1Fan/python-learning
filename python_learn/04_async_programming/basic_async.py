"""
asyncio 入门到进阶
运行: python python_learn/04_async_programming/basic_async.py
"""

import asyncio
import time


# ============================================================
# 1. 基础: 定义和运行协程
# ============================================================

async def hello():
    print("  Hello")
    await asyncio.sleep(0.1)
    print("  World")


# ============================================================
# 2. 并发执行: gather vs create_task
# ============================================================

async def fetch_data(url, delay):
    """模拟网络请求"""
    print(f"[fetch] 开始请求 {url}")
    await asyncio.sleep(delay)
    print(f"[fetch] 完成请求 {url}")
    return f"数据来自 {url}"


async def demo_concurrent():
    """对比顺序 vs 并发"""
    urls = [
        ("http://api1.com", 0.3),
        ("http://api2.com", 0.2),
        ("http://api3.com", 0.1),
    ]

    # 顺序执行
    print("\n--- 顺序执行 ---")
    start = time.perf_counter()
    for url, delay in urls:
        await fetch_data(url, delay)
    print(f"  总耗时: {time.perf_counter() - start:.2f}s")

    # 并发执行 gather
    print("\n--- gather 并发 ---")
    start = time.perf_counter()
    tasks = [fetch_data(url, delay) for url, delay in urls]
    results = await asyncio.gather(*tasks)
    for r in results:
        print(f"  {r}")
    print(f"  总耗时: {time.perf_counter() - start:.2f}s")

    # create_task 方式
    print("\n--- create_task 并发 ---")
    start = time.perf_counter()
    tasks = [asyncio.create_task(fetch_data(url, delay)) for url, delay in urls]
    for t in asyncio.as_completed(tasks):
        result = await t
        print(f"  [完成] {result}")
    print(f"  总耗时: {time.perf_counter() - start:.2f}s")


# ============================================================
# 3. Task 操作: 取消 / 超时 / 等待
# ============================================================

async def slow_operation(name, delay):
    try:
        print(f"[{name}] 开始 (耗时 {delay}s)")
        await asyncio.sleep(delay)
        print(f"[{name}] 完成")
        return f"{name} 结果"
    except asyncio.CancelledError:
        print(f"[{name}] 被取消")
        raise


async def demo_task_control():
    """Task 取消和超时"""
    # 取消任务
    task = asyncio.create_task(slow_operation("任务1", 5))
    await asyncio.sleep(0.5)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("  任务1 取消成功")

    # 超时
    try:
        async with asyncio.timeout(0.5):
            await slow_operation("任务2", 2)
    except TimeoutError:
        print("  任务2 超时")

    # wait_for
    try:
        await asyncio.wait_for(slow_operation("任务3", 3), timeout=1)
    except TimeoutError:
        print("  任务3 超时 (wait_for)")


# ============================================================
# 4. 信号量: 控制并发数
# ============================================================

async def bounded_fetch(semaphore, url, delay):
    async with semaphore:
        return await fetch_data(url, delay)


async def demo_semaphore():
    """限制同时只能有 3 个请求"""
    semaphore = asyncio.Semaphore(3)
    urls = [(f"http://api{i}.com", 0.3) for i in range(10)]
    tasks = [bounded_fetch(semaphore, url, delay) for url, delay in urls]
    results = await asyncio.gather(*tasks)
    print(f"  共完成 {len(results)} 个请求 (最大并发3)")


# ============================================================
# 5. async 上下文管理器
# ============================================================

class AsyncResource:
    async def __aenter__(self):
        print("  [异步] 获取资源")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, *args):
        print("  [异步] 释放资源")
        await asyncio.sleep(0.1)


async def demo_async_context():
    async with AsyncResource() as res:
        print("  使用异步资源中...")


# ============================================================
# 6. async 迭代器 / 异步生成器
# ============================================================

class AsyncRange:
    """异步迭代器"""
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.i >= self.n:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)
        val = self.i
        self.i += 1
        return val


async def async_generator(n):
    """异步生成器（简化写法）"""
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i


async def demo_async_iter():
    print("\n--- AsyncRange (异步迭代器) ---")
    async for i in AsyncRange(5):
        print(f"  {i}")

    print("\n--- 异步生成器 ---")
    async for i in async_generator(5):
        print(f"  {i}")


# ============================================================
# 7. Queue: 生产者-消费者
# ============================================================

async def producer(queue, n, consumers=2):
    for i in range(n):
        item = f"消息-{i}"
        await queue.put(item)
        print(f"[生产者] 放入: {item}")
        await asyncio.sleep(0.1)
    for _ in range(consumers):
        await queue.put(None)
    print("[生产者] 完成")


async def consumer(queue, name):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        print(f"[消费者-{name}] 处理: {item}")
        await asyncio.sleep(0.2)
        queue.task_done()
    print(f"[消费者-{name}] 退出")


# ============================================================
# 8. 主入口
# ============================================================

async def main():
    print("=" * 60)
    print("1. 基础协程")
    await hello()

    print("\n2. 并发执行")
    await demo_concurrent()

    print("\n3. Task 控制")
    await demo_task_control()

    print("\n4. 信号量控制并发")
    await demo_semaphore()

    print("\n5. 异步上下文管理器")
    await demo_async_context()

    print("\n6. 异步迭代器")
    await demo_async_iter()

    print("\n7. 生产者-消费者")
    q = asyncio.Queue()
    await asyncio.gather(
        producer(q, 5),
        consumer(q, "A"),
        consumer(q, "B"),
    )


if __name__ == "__main__":
    asyncio.run(main())
