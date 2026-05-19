"""
生成器与迭代器深度解析
运行: python python_learn/02_generators_iterators/yield_and_generator.py
"""

import sys


# ============================================================
# 1. 手写迭代器 vs 生成器
# ============================================================

class SquaresIterator:
    """手写迭代器: 实现 __iter__ 和 __next__"""
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        result = self.i ** 2
        self.i += 1
        return result


def squares_generator(n):
    """生成器: 用 yield 实现同样功能"""
    for i in range(n):
        yield i ** 2


# ============================================================
# 2. 生成器特性: 惰性求值 & 内存节省
# ============================================================

def lazy_range(n):
    """手写 range 生成器"""
    i = 0
    while i < n:
        yield i
        i += 1


# ============================================================
# 3. yield 高级用法: send / throw / close
# ============================================================

def echo():
    """双向通信生成器: send() 发送值给 yield"""
    print("生成器启动...")
    try:
        while True:
            received = yield
            print(f"生成器收到: {received}")
    except GeneratorExit:
        print("生成器被关闭")


def running_average():
    """维持状态的生成器: 计算运行平均值"""
    total = 0.0
    count = 0
    average = None
    while True:
        value = yield average
        if value is None:
            continue
        total += value
        count += 1
        average = total / count


# ============================================================
# 4. yield from — 委托给子生成器
# ============================================================

def sub_gen():
    """子生成器"""
    yield "来自子生成器 A"
    yield "来自子生成器 B"


def main_gen():
    """主生成器: 用 yield from 委托"""
    yield "来自主生成器"
    yield from sub_gen()
    yield "回到主生成器"


# ============================================================
# 5. yield from 进阶: 嵌套展平
# ============================================================

def flatten(nested):
    """递归展平嵌套可迭代对象"""
    try:
        for item in nested:
            try:
                # 尝试展平子元素
                yield from flatten(item)
            except TypeError:
                # 不可迭代则直接 yield
                yield item
    except TypeError:
        yield nested


# ============================================================
# 6. 生成器表达式 vs 列表推导式
# ============================================================

def compare_memory():
    list_comp = [x * x for x in range(100000)]
    gen_expr = (x * x for x in range(100000))
    print(f"列表推导式内存: {sys.getsizeof(list_comp):,} 字节")
    print(f"生成器表达式内存: {sys.getsizeof(gen_expr):,} 字节")


# ============================================================
# 7. 生成器的实际应用: 流式读取大文件
# ============================================================

def read_file_in_chunks(file_path, chunk_size=1024):
    """逐块读取文件，避免全部载入内存"""
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


# ============================================================
# 8. 无限序列 + take
# ============================================================

def fibonacci():
    """无限斐波那契数列生成器"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def take(n, iterable):
    """取前 n 个元素"""
    for i, value in enumerate(iterable):
        if i >= n:
            break
        yield value


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. 手写迭代器 vs 生成器")
    for v in SquaresIterator(5):
        print(f"  SquaresIterator: {v}")
    for v in squares_generator(5):
        print(f"  squares_generator: {v}")

    print("\n2. 惰性求值")
    for i in lazy_range(5):
        print(f"  lazy_range: {i}")

    print("\n3. send() 双向通信")
    gen = echo()
    next(gen)  # 启动生成器
    gen.send("Hello")
    gen.send("World")
    gen.close()

    print("\n4. running_average() - 维持状态")
    avg = running_average()
    next(avg)  # 启动
    print(f"  avg.send(10) = {avg.send(10)}")
    print(f"  avg.send(20) = {avg.send(20)}")
    print(f"  avg.send(30) = {avg.send(30)}")

    print("\n5. yield from 委托")
    for msg in main_gen():
        print(f"  {msg}")

    print("\n6. 递归展平")
    nested = [1, [2, [3, 4], 5], 6]
    print(f"  原始: {nested}")
    print(f"  展平: {list(flatten(nested))}")

    print("\n7. 内存对比")
    compare_memory()

    print("\n8. 无限序列")
    print(f"  前10个斐波那契数: {list(take(10, fibonacci()))}")
