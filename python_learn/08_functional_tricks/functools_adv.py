"""
functools 模块高级用法
运行: python python_learn/08_functional_tricks/functools_adv.py
"""

import functools
import time


# ============================================================
# 1. @lru_cache / @cache
# ============================================================

@functools.lru_cache(maxsize=128)
def fib(n):
    """缓存版斐波那契"""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


@functools.cache  # Python 3.9+，无大小限制
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


# ============================================================
# 2. @cached_property (Python 3.8+)
# ============================================================

class DataPipeline:
    def __init__(self, data):
        self.data = data

    @functools.cached_property
    def cleaned(self):
        """只执行一次的数据清洗"""
        print("  执行数据清洗...")
        time.sleep(0.2)
        return [x for x in self.data if x is not None]

    @functools.cached_property
    def statistics(self):
        print("  计算统计数据...")
        values = self.cleaned
        return {
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
        }


# ============================================================
# 3. functools.partial
# ============================================================

def power(base, exp):
    return base ** exp


# 固定参数
square = functools.partial(power, exp=2)
cube = functools.partial(power, exp=3)

# 实际应用: 创建多个相似函数
def connect(host, port, protocol, timeout):
    return f"连接 {protocol}://{host}:{port} (超时={timeout}s)"

connect_http = functools.partial(connect, protocol="http", timeout=30)
connect_https = functools.partial(connect, protocol="https", timeout=30)


# ============================================================
# 4. @singledispatch — 单分派泛型
# ============================================================

@functools.singledispatch
def serialize(obj):
    """序列化函数（默认实现）"""
    raise TypeError(f"不支持的类型: {type(obj)}")


@serialize.register(str)
def _(obj):
    return f"字符串: '{obj}'"


@serialize.register(int)
@serialize.register(float)
def _(obj):
    return f"数字: {obj}"


@serialize.register(list)
def _(obj):
    items = ", ".join(serialize(x) for x in obj)
    return f"[{items}]"


@serialize.register(dict)
def _(obj):
    pairs = ", ".join(f"{k}: {serialize(v)}" for k, v in obj.items())
    return f"{{{pairs}}}"


# 也可以注册自定义类型
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


@serialize.register(Person)
def _(obj):
    return f"Person(name={obj.name!r}, age={obj.age})"


# ============================================================
# 5. functools.reduce
# ============================================================

# reduce 的应用
sum_all = lambda *a: functools.reduce(lambda x, y: x + y, a)

# 替代 for 循环的经典模式
def compose(*funcs):
    """函数组合: compose(f, g)(x) = f(g(x))"""
    return functools.reduce(lambda f, g: lambda x: f(g(x)), funcs)


def pipe(*funcs):
    """管道: pipe(f, g)(x) = g(f(x))"""
    return functools.reduce(lambda f, g: lambda x: g(f(x)), funcs)


# ============================================================
# 6. @wraps 深入
# ============================================================

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper 文档"""
        return func(*args, **kwargs)
    return wrapper


@my_decorator
def original_func():
    """original_func 文档"""
    pass


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. @lru_cache & @cache")
    print(f"  fib(50) = {fib(50)}")
    print(f"  缓存信息: {fib.cache_info()}")
    print(f"  factorial(100) = {factorial(100)}")

    print("\n2. @cached_property")
    dp = DataPipeline([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"  stats = {dp.statistics}")
    print(f"  再次访问 (使用缓存): {dp.statistics}")

    print("\n3. partial 固定参数")
    print(f"  square(5) = {square(5)}")
    print(f"  cube(3) = {cube(3)}")
    print(f"  {connect_http('localhost', 8080)}")
    print(f"  {connect_https('api.example.com', 443)}")

    print("\n4. singledispatch")
    print(f"  {serialize('hello')}")
    print(f"  {serialize(42)}")
    print(f"  {serialize([1, 'a', 3.14])}")
    print(f"  {serialize({'name': 'Alice', 'age': 30})}")
    print(f"  {serialize(Person('Bob', 25))}")

    print("\n5. reduce")
    print(f"  sum_all(1,2,3,4,5) = {sum_all(1,2,3,4,5)}")
    # 函数组合
    add1 = lambda x: x + 1
    double = lambda x: x * 2
    compose_add1_then_double = compose(double, add1)
    pipe_add1_then_double = pipe(add1, double)
    print(f"  compose(double, add1)(5) = {compose_add1_then_double(5)}")  # double(add1(5)) = 12
    print(f"  pipe(add1, double)(5) = {pipe_add1_then_double(5)}")        # double(add1(5)) = 12

    print("\n6. @wraps")
    print(f"  func.__name__ = {original_func.__name__}")
    print(f"  func.__doc__  = {original_func.__doc__}")
