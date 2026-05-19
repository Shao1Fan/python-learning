"""
多进程编程
运行: python python_learn/09_concurrency_parallelism/multiprocess_demo.py
"""

import multiprocessing as mp
import time
import os
import sys
sys.set_int_max_str_digits(0)


# ============================================================
# 1. 基础进程
# ============================================================

def cpu_heavy(n):
    """CPU 密集型任务"""
    print(f"  进程 {os.getpid()}: 计算 fib({n})")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def demo_basic():
    print("\n--- 基础多进程 ---")
    start = time.perf_counter()

    with mp.Pool(processes=4) as pool:
        results = pool.map(cpu_heavy, [1000000, 1000000, 1000000, 1000000])

    print(f"  耗时: {time.perf_counter() - start:.2f}s")
    print(f"  结果: {[str(r)[:10] for r in results]}")


# ============================================================
# 2. Process 类
# ============================================================

class CustomProcess(mp.Process):
    def __init__(self, name, n):
        super().__init__()
        self.name = name
        self.n = n

    def run(self):
        print(f"  [{self.name}] PID={os.getpid()}, 父PID={os.getppid()}")
        result = cpu_heavy(self.n)
        self.result = result


def demo_process_class():
    print("\n--- 自定义 Process ---")
    procs = [CustomProcess(f"Worker-{i}", 500000) for i in range(3)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()


# ============================================================
# 3. 进程间通信 — Queue
# ============================================================

def worker_producer(q, n):
    for i in range(n):
        q.put(f"来自进程 {os.getpid()}: 消息 {i}")
    q.put(None)


def worker_consumer(q, results):
    count = 0
    while True:
        item = q.get()
        if item is None:
            break
        results.append(item)
        count += 1
    print(f"  消费者收到 {count} 条消息")


def demo_queue():
    print("\n--- 进程间 Queue ---")
    q = mp.Queue()
    manager = mp.Manager()
    results = manager.list()

    p1 = mp.Process(target=worker_producer, args=(q, 5))
    p2 = mp.Process(target=worker_consumer, args=(q, results))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # 如果 consumer 由 worker_producer 的 None 关闭，需要再 put 一个 None
    # 简化起见直接用 manager


# ============================================================
# 4. 共享内存
# ============================================================

def shared_memory_demo():
    print("\n--- 共享内存 ---")
    # Value
    counter = mp.Value('i', 0)

    def increment(c):
        for _ in range(1000):
            with c.get_lock():
                c.value += 1

    procs = [mp.Process(target=increment, args=(counter,)) for _ in range(10)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print(f"  共享 counter: {counter.value} (期望 10000)")

    # Array
    arr = mp.Array('d', [0.0, 0.0, 0.0])

    def set_values(a):
        for i in range(len(a)):
            a[i] = os.getpid() * (i + 1)

    procs = [mp.Process(target=set_values, args=(arr,)) for _ in range(3)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print(f"  共享 array: {list(arr)}")


# ============================================================
# 5. concurrent.futures 方式
# ============================================================

from concurrent.futures import ProcessPoolExecutor

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def demo_futures():
    print("\n--- ProcessPoolExecutor ---")
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(fibonacci, 800000) for _ in range(4)]
        results = [f.result() for f in futures]
    print(f"  耗时: {time.perf_counter() - start:.2f}s")
    print(f"  并行加速比: 约 {4}x (4核)")


# ============================================================
# 6. 进程池 vs 线程池 对比
# ============================================================

from concurrent.futures import ThreadPoolExecutor

def cpu_task(n):
    start = time.perf_counter()
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return time.perf_counter() - start


def compare_pool():
    print("\n--- 线程池 vs 进程池 (CPU任务) ---")
    n = 500000

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as ex:
        list(ex.map(cpu_task, [n] * 4))
    t_thread = time.perf_counter() - start
    print(f"  线程池: {t_thread:.2f}s (受 GIL 限制)")

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as ex:
        list(ex.map(cpu_task, [n] * 4))
    t_process = time.perf_counter() - start
    print(f"  进程池: {t_process:.2f}s (真正的并行)")


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    # macOS 需要此设置
    mp.set_start_method('fork', force=True)

    print("=" * 60)
    demo_basic()
    demo_process_class()
    demo_queue()
    shared_memory_demo()
    demo_futures()
    compare_pool()
