"""
异步编程实战案例
运行: python python_learn/04_async_programming/real_world.py

某些示例需要安装: pip install aiohttp httpx
"""

import asyncio
import time


# ============================================================
# 案例1: 异步 Web 爬虫（模拟）
# ============================================================

class AsyncWebCrawler:
    """模拟异步爬虫"""
    def __init__(self, max_concurrent=5):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch(self, url: str) -> dict:
        async with self.semaphore:
            print(f"  [爬取] {url}")
            # 模拟网络 IO
            await asyncio.sleep(0.3 + hash(url) % 3 * 0.1)
            return {"url": url, "status": 200, "size": 1024}

    async def crawl_many(self, urls: list[str]) -> list[dict]:
        tasks = [self.fetch(url) for url in urls]
        return await asyncio.gather(*tasks)


# ============================================================
# 案例2: 超时与重试
# ============================================================

class AsyncRetry:
    """异步重试包装器"""
    async def execute(self, url: str, max_retries=3, timeout=2.0):
        for attempt in range(1, max_retries + 1):
            try:
                async with asyncio.timeout(timeout):
                    print(f"  [尝试 {attempt}/{max_retries}] {url}")
                    await asyncio.sleep(0.5 * attempt)
                    if attempt < 2:  # 模拟前几次失败
                        raise ConnectionError("网络异常")
                    return f"结果: {url}"
            except (TimeoutError, ConnectionError) as e:
                print(f"  [失败] {e}")
                if attempt == max_retries:
                    raise
        return None


# ============================================================
# 案例3: 异步文件处理（aiofiles 模拟）
# ============================================================

class AsyncFileProcessor:
    """模拟异步文件处理 (asyncio.to_thread 包装阻塞 IO)"""
    async def read_large_file(self, path: str) -> str:
        # 用 to_thread 避免阻塞事件循环
        def _read():
            with open(path, 'r') as f:
                return f.read()
        return await asyncio.to_thread(_read)

    async def process_many(self, paths: list[str]):
        tasks = [self.read_large_file(p) for p in paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for path, result in zip(paths, results):
            if isinstance(result, Exception):
                print(f"  [错误] {path}: {result}")
            else:
                print(f"  [完成] {path}: {len(result)} 字符")


# ============================================================
# 案例4: 异步限流器 (Rate Limiter)
# ============================================================

class RateLimiter:
    """令牌桶算法实现限流"""
    def __init__(self, rate: float, burst: int):
        self.rate = rate          # 每秒添加令牌数
        self.burst = burst        # 最大令牌数
        self.tokens = burst
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            self._refill()
            if self.tokens < 1:
                wait_time = (1 - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
                self._refill()
            self.tokens -= 1

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
        self.last_refill = now


async def rate_limited_task(limiter: RateLimiter, task_id: int):
    await limiter.acquire()
    print(f"  [任务 {task_id}] 执行 (tokens={limiter.tokens:.1f})")


# ============================================================
# 案例5: 协程间通信 — 广播模式
# ============================================================

class AsyncBroadcast:
    """一对多广播"""
    def __init__(self):
        self._subscribers = []

    def subscribe(self, queue: asyncio.Queue):
        self._subscribers.append(queue)

    async def publish(self, message):
        for q in self._subscribers:
            await q.put(message)

    async def close(self):
        for q in self._subscribers:
            await q.put(None)


async def subscriber(name: str, queue: asyncio.Queue):
    while True:
        msg = await queue.get()
        if msg is None:
            break
        print(f"  [{name}] 收到: {msg}")
    print(f"  [{name}] 退出")


# ============================================================
# 运行演示
# ============================================================

async def main():
    print("=" * 60)
    print("案例1: 异步爬虫")
    crawler = AsyncWebCrawler(max_concurrent=3)
    urls = [f"https://api.example.com/page/{i}" for i in range(6)]
    results = await crawler.crawl_many(urls)
    print(f"  爬取完成: {len(results)} 个页面")

    print("\n案例2: 超时重试")
    retrier = AsyncRetry()
    try:
        result = await retrier.execute("https://api.unstable.com")
        print(f"  {result}")
    except Exception as e:
        print(f"  最终失败: {e}")

    print("\n案例3: 异步文件处理")
    processor = AsyncFileProcessor()
    await processor.process_many(["/tmp/test1.txt", "/tmp/test2.txt"])

    print("\n案例4: 限流器")
    limiter = RateLimiter(rate=5, burst=3)  # 每秒5个，突发3个
    tasks = [rate_limited_task(limiter, i) for i in range(8)]
    await asyncio.gather(*tasks)

    print("\n案例5: 广播模式")
    broadcast = AsyncBroadcast()
    q1 = asyncio.Queue()
    q2 = asyncio.Queue()
    broadcast.subscribe(q1)
    broadcast.subscribe(q2)
    async with asyncio.TaskGroup() as tg:
        tg.create_task(subscriber("订阅者A", q1))
        tg.create_task(subscriber("订阅者B", q2))
        for i in range(3):
            await broadcast.publish(f"消息 #{i}")
            await asyncio.sleep(0.1)
        await broadcast.close()


if __name__ == "__main__":
    asyncio.run(main())
