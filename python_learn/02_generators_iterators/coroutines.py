"""
基于生成器的协程（async/await 的前身）
运行: python python_learn/02_generators_iterators/coroutines.py
"""


# ============================================================
# 1. 协程基础: 用 yield 实现消费者-生产者
# ============================================================

def consumer():
    """消费者协程"""
    print("[消费者] 启动，等待数据...")
    total = 0
    count = 0
    while True:
        value = yield      # 接收生产者发送的数据
        if value is None:  # 终止信号
            break
        count += 1
        total += value
        print(f"[消费者] 收到 #{count}: {value}")
    return total, count


def producer():
    """生产者: 驱动消费者协程"""
    c = consumer()
    next(c)  # 启动消费者（执行到第一个 yield）

    for i in range(1, 6):
        print(f"[生产者] 发送 #{i}: {i * 10}")
        c.send(i * 10)

    try:
        c.send(None)  # 发送终止信号
    except StopIteration as e:
        total, count = e.value
        print(f"[统计] 共处理 {count} 个值，总和={total}")


# ============================================================
# 2. 协程管道: 多个协程串联
# ============================================================

def coroutine(func):
    """装饰器: 自动调用 next() 启动协程"""
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return start


@coroutine
def filter_even(target):
    """过滤偶数"""
    while True:
        value = yield
        if value % 2 == 0:
            target.send(value)


@coroutine
def printer(prefix=""):
    """打印接收到的值"""
    while True:
        value = yield
        print(f"{prefix}{value}")


# ============================================================
# 3. 协程实现简单状态机
# ============================================================

@coroutine
def state_machine():
    """状态机: 管理一个实体的状态流转"""
    state = "初始化"
    print(f"[状态机] 初始状态: {state}")
    while True:
        event = yield
        if state == "初始化" and event == "启动":
            state = "运行中"
            print(f"[状态机] 事件={event} → 状态={state}")
        elif state == "运行中" and event == "暂停":
            state = "已暂停"
            print(f"[状态机] 事件={event} → 状态={state}")
        elif state == "运行中" and event == "停止":
            state = "已停止"
            print(f"[状态机] 事件={event} → 状态={state}")
            break
        elif state == "已暂停" and event == "恢复":
            state = "运行中"
            print(f"[状态机] 事件={event} → 状态={state}")
        else:
            print(f"[状态机] 非法转换: 状态={state}, 事件={event}")


# ============================================================
# 4. 模拟 async/await 的简化版事件循环
# ============================================================

from collections import deque

class SimpleEventLoop:
    """极简事件循环（基于生成器协程）"""
    def __init__(self):
        self.tasks = deque()

    def add_task(self, coro):
        self.tasks.append(coro)

    def run(self):
        while self.tasks:
            coro = self.tasks.popleft()
            try:
                next(coro)
                self.tasks.append(coro)  # 放回队列继续运行
            except StopIteration:
                pass  # 协程完成


def task_hello(name):
    """协程任务"""
    for i in range(3):
        print(f"[{name}] 运行第 {i+1} 步")
        yield  # 主动让出控制权


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. 生产-消费者协程")
    producer()

    print("\n2. 协程管道: 过滤偶数")
    p = printer("  结果: ")
    f = filter_even(p)
    for n in [1, 2, 3, 4, 5, 6]:
        f.send(n)

    print("\n3. 状态机协程")
    sm = state_machine()
    sm.send("启动")
    sm.send("暂停")
    sm.send("恢复")
    try:
        sm.send("停止")
    except StopIteration:
        pass

    print("\n4. 简化版事件循环")
    loop = SimpleEventLoop()
    loop.add_task(task_hello("任务A"))
    loop.add_task(task_hello("任务B"))
    loop.add_task(task_hello("任务C"))
    loop.run()
