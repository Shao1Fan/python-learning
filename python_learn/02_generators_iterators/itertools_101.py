"""
itertools 模块深度应用
运行: python python_learn/02_generators_iterators/itertools_101.py
"""

import itertools
import operator


# ============================================================
# 1. 无限迭代器
# ============================================================

def demo_count():
    """count(start=0, step=1)"""
    for i in itertools.count(10, 2):
        if i > 20:
            break
        print(f"  {i}", end="")


def demo_cycle():
    """cycle(iterable) — 无限循环"""
    colors = itertools.cycle(["红", "绿", "蓝"])
    for _ in range(6):
        print(f"  {next(colors)}", end=" ")


def demo_repeat():
    """repeat(object, times=None)"""
    for item in itertools.repeat("🔔", 3):
        print(f"  {item}")


# ============================================================
# 2. 有限迭代器
# ============================================================

def demo_accumulate():
    """accumulate — 累积运算"""
    nums = [1, 2, 3, 4, 5]
    print(f"  原始: {nums}")
    print(f"  累积和: {list(itertools.accumulate(nums))}")
    print(f"  累积乘: {list(itertools.accumulate(nums, operator.mul))}")


def demo_chain():
    """chain — 串联多个可迭代对象"""
    result = list(itertools.chain([1, 2], [3, 4], "ab"))
    print(f"  chain: {result}")
    # 等价: itertools.chain.from_iterable([[1,2], [3,4]])


def demo_compress():
    """compress — 用选择器过滤"""
    data = ["A", "B", "C", "D"]
    selectors = [1, 0, 1, 1]
    print(f"  compress: {list(itertools.compress(data, selectors))}")


def demo_dropwhile_takewhile():
    """dropwhile / takewhile"""
    nums = [1, 4, 6, 4, 1]
    print(f"  dropwhile(<5): {list(itertools.dropwhile(lambda x: x < 5, nums))}")
    print(f"  takewhile(<5): {list(itertools.takewhile(lambda x: x < 5, nums))}")


def demo_filterfalse():
    """filterfalse — 保留不符合条件的"""
    nums = [1, 2, 3, 4, 5, 6]
    print(f"  filterfalse(偶数): {list(itertools.filterfalse(lambda x: x % 2 == 0, nums))}")


def demo_islice():
    """islice — 可迭代对象切片"""
    nums = range(10)
    print(f"  islice(2, 7, 2): {list(itertools.islice(nums, 2, 7, 2))}")


def demo_starmap():
    """starmap — 解包参数后 map"""
    pairs = [(2, 3), (4, 5), (6, 7)]
    print(f"  starmap(pow): {list(itertools.starmap(pow, pairs))}")


def demo_zip_longest():
    """zip_longest — 以最长的为准"""
    a = [1, 2, 3]
    b = [10, 20]
    print(f"  zip_longest: {list(itertools.zip_longest(a, b, fillvalue=0))}")


# ============================================================
# 3. 排列组合
# ============================================================

def demo_combinations():
    """combinations — 组合（不放回，顺序无关）"""
    items = [1, 2, 3, 4]
    print(f"  combinations(2): {list(itertools.combinations(items, 2))}")


def demo_permutations():
    """permutations — 排列（不放回，顺序有关）"""
    items = [1, 2, 3]
    print(f"  permutations(2): {list(itertools.permutations(items, 2))}")


def demo_product():
    """product — 笛卡尔积（放回，顺序有关）"""
    items = [1, 2]
    print(f"  product(2): {list(itertools.product(items, repeat=2))}")


def demo_combinations_with_replacement():
    """combinations_with_replacement — 组合（放回，顺序无关）"""
    items = [1, 2, 3]
    print(f"  combinations_with_replacement(2): {list(itertools.combinations_with_replacement(items, 2))}")


# ============================================================
# 4. 分组
# ============================================================

def demo_groupby():
    """groupby — 按键分组（必须先排序）"""
    data = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)]
    data.sort(key=lambda x: x[0])  # 必须先排序！
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        print(f"  {key}: {list(group)}")


# ============================================================
# 5. 实用案例
# ============================================================

def chunked(iterable, n):
    """将可迭代对象分成大小为 n 的块"""
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, n))
        if not chunk:
            break
        yield chunk


def ncycles(iterable, n):
    """将序列重复 n 次"""
    return itertools.chain.from_iterable(itertools.repeat(tuple(iterable), n))


def unique_everseen(iterable, key=None):
    """去除连续重复元素，但保留首次出现（与 dedup 不同）"""
    seen = set()
    for element in iterable:
        k = key(element) if key else element
        if k not in seen:
            seen.add(k)
            yield element


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. 无限迭代器")
    print("\n  count:", end=""); demo_count()
    print("\n  cycle:", end=""); demo_cycle()
    print("\n  repeat:", end=""); demo_repeat()

    print("\n\n2. 有限迭代器")
    print("\n  accumulate:"); demo_accumulate()
    print("  chain:"); demo_chain()
    print("  compress:"); demo_compress()
    print("  dropwhile/takewhile:"); demo_dropwhile_takewhile()
    print("  filterfalse:"); demo_filterfalse()
    print("  islice:"); demo_islice()
    print("  starmap:"); demo_starmap()
    print("  zip_longest:"); demo_zip_longest()

    print("\n3. 排列组合")
    demo_combinations()
    demo_permutations()
    demo_product()
    demo_combinations_with_replacement()

    print("\n4. groupby 分组")
    demo_groupby()

    print("\n5. 实用案例")
    print(f"  chunked(range(10), 3): {list(chunked(range(10), 3))}")
    print(f"  ncycles([1,2,3], 3): {list(ncycles([1,2,3], 3))}")
    data = [1, 1, 2, 2, 3, 3, 4, 5]
    # 注意这里是演示 batch 的去重功能
    print(f"  unique_everseen: {list(unique_everseen(data))}")
