"""
__slots__ 内存优化与性能
运行: python python_learn/06_descriptors_and_properties/__slots__.py
"""

import sys


# ============================================================
# 1. __slots__ 基础
# ============================================================

class WithoutSlots:
    """普通类: 使用 __dict__ 存储属性"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


class WithSlots:
    """使用 __slots__: 固定属性，省去 __dict__"""
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


# ============================================================
# 2. 内存对比
# ============================================================

def compare_memory():
    objs_no_slots = [WithoutSlots(i, i * 2) for i in range(1000)]
    objs_with_slots = [WithSlots(i, i * 2) for i in range(1000)]

    mem_no_slots = sys.getsizeof(objs_no_slots[0]) + sys.getsizeof(objs_no_slots[0].__dict__)
    mem_with_slots = sys.getsizeof(objs_with_slots[0])

    print(f"  无 __slots__: {mem_no_slots} 字节/对象")
    print(f"  有 __slots__: {mem_with_slots} 字节/对象")


# ============================================================
# 3. __slots__ 的限制与继承
# ============================================================

class BaseWithSlots:
    __slots__ = ("a",)

class ChildWithSlots(BaseWithSlots):
    __slots__ = ("b",)  # 子类也必须定义 __slots__

    def __init__(self, a, b):
        self.a = a
        self.b = b


# ============================================================
# 4. __slots__ 中使用 __dict__（兼容动态属性）
# ============================================================

class FlexibleSlots:
    """允许部分动态属性"""
    __slots__ = ("fixed", "__dict__")  # 保留 __dict__

    def __init__(self, fixed):
        self.fixed = fixed


# ============================================================
# 5. __slots__ 与描述符
# ============================================================

class Descriptor:
    """描述符可以和 __slots__ 配合"""
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj._value

    def __set__(self, obj, value):
        obj._value = value


class WithDescriptor:
    __slots__ = ("_value",)
    attr = Descriptor()


# ============================================================
# 6. 性能对比
# ============================================================

import time

def benchmark():
    N = 1_000_000
    print(f"\n  创建 {N:,} 个对象并访问属性...")

    start = time.perf_counter()
    objs1 = [WithoutSlots(i, i * 2) for i in range(N)]
    t1 = sum(o.x + o.y for o in objs1)
    t_create_no_slots = time.perf_counter() - start

    start = time.perf_counter()
    objs2 = [WithSlots(i, i * 2) for i in range(N)]
    t2 = sum(o.x + o.y for o in objs2)
    t_create_with_slots = time.perf_counter() - start

    print(f"  无 __slots__: 创建+访问 {t_create_no_slots:.2f}s")
    print(f"  有 __slots__: 创建+访问 {t_create_with_slots:.2f}s")
    print(f"  __slots__ 主要优势是内存节省，属性访问差异取决于 Python 版本和访问模式")


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)

    # 常规对象
    obj1 = WithoutSlots(1, 2)
    obj2 = WithSlots(1, 2)

    print(f"  无 __slots__ 有 __dict__: {hasattr(obj1, '__dict__')}")
    print(f"  有 __slots__ 无 __dict__: {hasattr(obj2, '__dict__')}")

    # 无法动态添加属性
    try:
        obj2.z = 3
    except AttributeError as e:
        print(f"  __slots__ 禁止动态添加: {e}")

    print()
    compare_memory()

    # 性能和内存的基准测试（默认只在小样本测试）
    print(f"\n  高性能基准测试 (N=100,000):")
    benchmark()
