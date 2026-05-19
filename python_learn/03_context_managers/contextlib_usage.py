"""
contextlib 模块高级用法
运行: python python_learn/03_context_managers/contextlib_usage.py
"""

from contextlib import contextmanager, closing, suppress, ExitStack, redirect_stdout, redirect_stderr
import io
import os


# ============================================================
# 1. @contextmanager 装饰器
# ============================================================

@contextmanager
def timer():
    """用装饰器实现计时上下文管理器"""
    start = time.perf_counter()
    try:
        yield  # 此处是 with 块的内容
    finally:
        end = time.perf_counter()
        print(f"耗时: {(end - start) * 1000:.2f}ms")


@contextmanager
def change_dir(path):
    """临时切换工作目录"""
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


@contextmanager
def open_file(filename, mode='r'):
    """自定义文件打开上下文（演示用，生产用内置 open）"""
    print(f"打开文件: {filename}")
    f = open(filename, mode)
    try:
        yield f
    finally:
        print(f"关闭文件: {filename}")
        f.close()


# ============================================================
# 2. contextlib.closing
# ============================================================

class MyResource:
    def __init__(self, name):
        self.name = name

    def close(self):
        print(f"[closing] 关闭: {self.name}")


# ============================================================
# 3. contextlib.suppress — 忽略特定异常
# ============================================================

def demo_suppress():
    """suppress 等效于 try/except pass，但更清晰"""
    with suppress(FileNotFoundError):
        os.remove("不存在的文件.txt")
    print("  [suppress] FileNotFoundError 被安静地忽略")

    with suppress(ValueError, TypeError):
        int("不是数字")
    print("  [suppress] ValueError 也被忽略")


# ============================================================
# 4. contextlib.ExitStack — 动态管理多个上下文
# ============================================================

def demo_exitstack():
    """ExitStack 允许在运行时动态添加/移除上下文管理器"""
    files = []
    stack = ExitStack()

    # 打开多个文件
    for name in ["a.txt", "b.txt", "c.txt"]:
        try:
            f = open(f"/tmp/{name}", "w")
            stack.enter_context(closing(f))
            files.append(f)
        except FileNotFoundError:
            print(f"  文件 {name} 打开失败")

    # 写入内容
    for f in files:
        f.write("Hello\n")

    # 一次性清理所有
    stack.close()
    print("  [ExitStack] 所有文件已关闭")


# ============================================================
# 5. contextlib.redirect_stdout / redirect_stderr
# ============================================================

def demo_redirect():
    """临时重定向标准输出"""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print("这行输出被捕获")
        print("这行也是")
    output = buffer.getvalue()
    print(f"[捕获的输出]: {output!r}")


# ============================================================
# 6. 实现可重入上下文 (contextlib.ContextDecorator)
# ============================================================

from contextlib import ContextDecorator

class LogTask(ContextDecorator):
    """同时可用作装饰器和上下文管理器"""
    def __init__(self, task_name=None):
        self.task_name = task_name

    def __enter__(self):
        self.start = time.perf_counter()
        print(f"[开始] {self.task_name}")
        return self

    def __exit__(self, *args):
        elapsed = (time.perf_counter() - self.start) * 1000
        print(f"[结束] {self.task_name} ({elapsed:.2f}ms)")
        return False


@LogTask(task_name="heavy_compute")
def heavy_compute():
    time.sleep(0.1)


import time

# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. @contextmanager 装饰器")
    with timer():
        time.sleep(0.05)

    print("\n2. contextlib.closing")
    with closing(MyResource("test.txt")) as res:
        print(f"  使用资源: {res.name}")

    print("\n3. contextlib.suppress")
    demo_suppress()

    print("\n4. contextlib.ExitStack")
    demo_exitstack()

    print("\n5. redirect_stdout")
    demo_redirect()

    print("\n6. ContextDecorator")
    heavy_compute()
