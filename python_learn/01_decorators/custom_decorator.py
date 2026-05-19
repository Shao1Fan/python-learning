"""
自定义装饰器 —— 从基础到进阶
运行: python python_learn/01_decorators/custom_decorator.py
"""

import functools
import time


# ============================================================
# 1. 最简单的装饰器（无参）
# ============================================================

def timer(func):
    """打印函数执行时间"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[{func.__name__}] 耗时: {(end - start) * 1000:.2f}ms")
        return result
    return wrapper


@timer
def slow_add(a, b):
    time.sleep(0.1)
    return a + b


# ============================================================
# 2. 带参数的装饰器（装饰器工厂）
# ============================================================

def retry(max_attempts=3, delay=0.5):
    """失败重试装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"[{func.__name__}] 第{attempt}次失败: {e}，重试中...")
                    time.sleep(delay)
        return wrapper
    return decorator


@retry(max_attempts=3, delay=0.1)
def unstable_api(x):
    if time.time() % 2 < 1:
        raise ConnectionError("网络波动")
    return x * 2


# ============================================================
# 3. 类装饰器
# ============================================================

class CountCalls:
    """统计函数被调用了多少次"""
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"[{self.func.__name__}] 第 {self.count} 次调用")
        return self.func(*args, **kwargs)


@CountCalls
def greet(name):
    return f"你好，{name}！"


# ============================================================
# 4. 装饰器在类方法上使用（注意 self）
# ============================================================

def method_logger(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"[{self.__class__.__name__}] 调用 {func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper


class Service:
    @method_logger
    def run(self):
        print("Service running...")


# ============================================================
# 5. 装饰器也可以是一个类方法
# ============================================================

class Decorators:
    """将装饰器组织为类的静态方法"""
    @staticmethod
    def log_call(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"调用: {func.__name__}({args}, {kwargs})")
            return func(*args, **kwargs)
        return wrapper


@Decorators.log_call
def square(x):
    return x ** 2


# ============================================================
# 6. 带状态: 缓存装饰器（手写简化版 LRU）
# ============================================================

def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"[缓存命中] {func.__name__}{args}")
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper


@memoize
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


# ============================================================
# 7. 多个装饰器组合
# ============================================================

def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper


@bold
@italic
def formatted_text(text):
    return text


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("1. 计时装饰器")
    print(slow_add(3, 4))

    print("\n2. 重试装饰器")
    try:
        print(unstable_api(10))
    except ConnectionError:
        print("最终仍然失败")

    print("\n3. 类装饰器（统计调用次数）")
    print(greet("Alice"))
    print(greet("Bob"))

    print("\n4. 方法装饰器")
    svc = Service()
    svc.run()

    print("\n5. 类静态方法装饰器")
    print(square(5))

    print("\n6. 缓存装饰器")
    print(f"fib(10) = {fib(10)}")
    print(f"fib(10) = {fib(10)}（第二次，命中缓存）")

    print("\n7. 多个装饰器组合")
    print(formatted_text("Hello 世界"))
    # 注意顺序: bold(italic(func))  →  <b><i>Hello 世界</i></b>
