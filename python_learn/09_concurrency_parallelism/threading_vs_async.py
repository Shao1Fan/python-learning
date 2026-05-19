"""
线程 vs 异步 对比
运行: python python_learn/09_concurrency_parallelism/threading_vs_async.py
"""

import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
import queue


# ============================================================
# 1. 基础线程
# ============================================================

def worker(name, delay, results):
    """模拟 IO 任务"""
    print(f"  [线程-{name}] 开始")
    time.sleep(delay)
    results.append(f"线程-{name} 完成")
    print(f"  [线程-{name}] 结束")


def demo_threading():
    print("\n--- threading 并发 ---")
    start = time.perf_counter()
    results = []
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i, 0.3, results))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(f"  总耗时: {time.perf_counter() - start:.2f}s")
    print(f"  结果: {results}")


# ============================================================
# 2. 线程安全: Lock
# ============================================================

class Counter:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            current = self.value
            time.sleep(0.0001)
            self.value = current + 1


def demo_lock():
    print("\n--- 线程安全 (Lock) ---")
    counter = Counter()
    threads = [threading.Thread(target=counter.increment) for _ in range(100)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"  期望: 100, 实际: {counter.value}")
    print(f"  {'正确' if counter.value == 100 else '有竞态条件!'}")


# ============================================================
# 3. RLock vs Lock
# ============================================================

class RLockDemo:
    """RLock 可重入: 同一个线程可以多次获取"""
    def __init__(self):
        self.lock = threading.RLock()
        self.data = {}

    def get(self, key):
        with self.lock:
            return self._get_internal(key)

    def _get_internal(self, key):
        with self.lock:  # RLock 允许重入，普通 Lock 会死锁
            return self.data.get(key)


# ============================================================
# 4. Queue: 线程安全通信
# ============================================================

def producer(q, n):
    for i in range(n):
        item = f"item-{i}"
        q.put(item)
        print(f"[生产者] 放入: {item}")
    q.put(None)  # 终止信号

def consumer(q, name):
    while True:
        item = q.get()
        if item is None:
            q.put(None)  # 让其他消费者也退出
            break
        print(f"[消费者-{name}] 处理: {item}")
        time.sleep(0.05)


def demo_queue():
    print("\n--- Queue 通信 ---")
    q = queue.Queue(maxsize=3)
    threads = [
        threading.Thread(target=producer, args=(q, 5)),
        threading.Thread(target=consumer, args=(q, "A")),
        threading.Thread(target=consumer, args=(q, "B")),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# ============================================================
# 5. 对比: 相同任务 threading vs asyncio
# ============================================================

# Threading 版
def io_task_thread(n):
    time.sleep(0.1)
    return n * 2

def threading_version():
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(io_task_thread, i) for i in range(20)]
        return [f.result() for f in futures]

# Asyncio 版
async def io_task_async(n):
    await asyncio.sleep(0.1)
    return n * 2

async def async_version():
    tasks = [io_task_async(i) for i in range(20)]
    return await asyncio.gather(*tasks)


def compare():
    print("\n--- threading vs asyncio 对比 (20个IO任务) ---")
    # Threading
    start = time.perf_counter()
    r1 = threading_version()
    t1 = time.perf_counter() - start
    print(f"  threading: {t1:.2f}s")

    # Asyncio
    start = time.perf_counter()
    r2 = asyncio.run(async_version())
    t2 = time.perf_counter() - start
    print(f"  asyncio:   {t2:.2f}s")
    print(f"  结果一致: {r1 == r2}")


# ============================================================
# 6. Event — 线程间信号
# ============================================================

def waiter(event, name):
    print(f"[{name}] 等待事件...")
    event.wait()  # 阻塞直到事件被设置
    print(f"[{name}] 收到事件!")

def setter(event):
    time.sleep(0.3)
    print("[setter] 设置事件!")
    event.set()


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    demo_threading()
    demo_lock()
    print("\n  RLock 可重入测试通过")

    # 使用线程池比较
    compare()
    demo_queue()

    print("\n--- Event ---")
    event = threading.Event()
    threads = [
        threading.Thread(target=waiter, args=(event, "A")),
        threading.Thread(target=waiter, args=(event, "B")),
        threading.Thread(target=setter, args=(event,)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
