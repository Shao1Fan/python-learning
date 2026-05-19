"""
手写上下文管理器
运行: python python_learn/03_context_managers/custom_context.py
"""

import time
from contextlib import contextmanager


# ============================================================
# 1. 类方式: 实现 __enter__ 和 __exit__
# ============================================================

class Timer:
    """计时上下文管理器"""
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        elapsed = (self.end - self.start) * 1000
        print(f"耗时: {elapsed:.2f}ms")
        # 返回 False 表示不吞异常，True 则吞掉
        return False


class DatabaseConnection:
    """模拟数据库连接上下文管理器"""
    def __init__(self, dsn):
        self.dsn = dsn

    def __enter__(self):
        print(f"[连接] 建立连接: {self.dsn}")
        self.connected = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[断开] 关闭连接: {self.dsn}")
        self.connected = False
        if exc_type:
            print(f"[异常] 发生了异常: {exc_val}")
        return False  # 不吞异常

    def query(self, sql):
        if not self.connected:
            raise RuntimeError("连接已关闭")
        return f"[结果] 执行: {sql}"


# ============================================================
# 2. 异常处理: __exit__ 吞掉特定异常
# ============================================================

class IgnoreValueError:
    """忽略 ValueError"""
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print(f"[IgnoreValueError] 忽略: {exc_val}")
            return True
        return False


# ============================================================
# 3. 嵌套上下文管理器
# ============================================================

class Resource:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"[{self.name}] 获取资源")
        return self

    def __exit__(self, *args):
        print(f"[{self.name}] 释放资源")
        return False


# ============================================================
# 4. 异步上下文管理器（预览，详细在 async 章节）
# ============================================================

class AsyncDatabase:
    """异步上下文管理器（示意）"""
    async def __aenter__(self):
        print("[async] 连接数据库...")
        return self

    async def __aexit__(self, *args):
        print("[async] 断开数据库...")


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. Timer 计时上下文")
    with Timer() as t:
        time.sleep(0.05)
        print("  (做了些工作)")

    print("\n2. 数据库连接")
    with DatabaseConnection("mysql://localhost/mydb") as db:
        print(db.query("SELECT 1"))
    print("  (with 块结束，连接已关闭)")

    print("\n3. 吞掉异常")
    with IgnoreValueError():
        raise ValueError("这是一个被忽略的异常")
    print("  (程序继续运行)")

    print("\n4. 嵌套上下文")
    with Resource("A") as a, Resource("B") as b:
        print("  使用 A 和 B")
