"""
垃圾回收与内存泄漏排查
运行: python python_learn/11_memory_and_gc/gc_and_leak.py
"""

import gc
import sys
import weakref


# ============================================================
# 1. 引用计数
# ============================================================

def refcount_demo():
    print("--- 引用计数 ---")
    x = [1, 2, 3]
    print(f"  初始: sys.getrefcount(x) = {sys.getrefcount(x)}")
    y = x
    print(f"  赋值后: sys.getrefcount(x) = {sys.getrefcount(x)}")
    del y
    print(f"  del y 后: sys.getrefcount(x) = {sys.getrefcount(x)}")


# ============================================================
# 2. 循环引用
# ============================================================

class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []

    def __repr__(self):
        return f"Node({self.name})"


def circular_ref_demo():
    print("\n--- 循环引用 ---")
    gc.collect()  # 先回收干净

    a = Node("A")
    b = Node("B")
    a.children.append(b)
    b.parent = a

    print(f"  a -> b 的引用: a.children[0] is b = {a.children[0] is b}")
    print(f"  b -> a 的引用: b.parent is a = {b.parent is a}")

    # 循环引用导致引用计数永远不为 0
    # 但 gc 模块可以回收
    print(f"  gc.garbage: {gc.garbage}")


# ============================================================
# 3. gc 模块 — 手动控制
# ============================================================

def gc_demo():
    print("\n--- gc 模块 ---")
    print(f"  是否启用: {gc.isenabled()}")
    print(f"  各代阈值: {gc.get_threshold()}")  # (700, 10, 10)
    print(f"  各代计数: {gc.get_count()}")

    # 创建并丢弃对象，观察 GC
    for _ in range(1000):
        _ = [1] * 1000

    print(f"  GC 统计: {gc.get_stats()}")

    # 手动触发
    collected = gc.collect()
    print(f"  手动 GC 回收了 {collected} 个对象")


# ============================================================
# 4. __del__ 陷阱
# ============================================================

class Resource:
    def __init__(self, name):
        self.name = name

    def __del__(self):
        print(f"  [__del__] 释放资源: {self.name}")
        # 注意: __del__ 中不要访问全局变量，不要依赖其调用时机


class CircularDel:
    """__del__ + 循环引用 = 无法回收"""
    def __init__(self, name):
        self.name = name
        self.other = None

    def __del__(self):
        print(f"  [__del__] {self.name}")


def del_trap_demo():
    print("\n--- __del__ 陷阱 ---")
    a = CircularDel("A")
    b = CircularDel("B")
    a.other = b
    b.other = a

    del a, b
    # 因为 __del__ 的存在，gc 无法回收循环引用对象
    # Python 会将它们放入 gc.garbage
    if hasattr(gc, 'garbage'):
        pass  # Python 3.4+ 改为自动回收


# ============================================================
# 5. 利用 weakref 避免循环引用
# ============================================================

class WeakNode:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []

    def __repr__(self):
        return f"WeakNode({self.name})"


def weakref_demo():
    print("\n--- weakref 避免循环引用 ---")
    a = WeakNode("A")
    b = WeakNode("B")

    # 用弱引用替代强引用
    a.children.append(weakref.ref(b))
    b.parent = weakref.ref(a)

    # 访问弱引用
    b_ref = a.children[0]
    print(f"  弱引用: {b_ref}")
    print(f"  通过弱引用访问: {b_ref()}")

    # 删除 b 后，弱引用失效
    del b
    print(f"  删除后: {b_ref()}")  # None


# ============================================================
# 6. 内存泄漏排查 (使用 objgraph)
# ============================================================

def leak_simulation():
    print("\n--- 内存泄漏排查 ---")
    cache = []

    def leak():
        """模拟回调泄漏"""
        class Leaky:
            def __init__(self, name):
                self.name = name

        obj = Leaky(f"obj-{id(Leaky)}")
        # 闭包持有 Leaky 引用，变成了泄漏
        def callback():
            return obj.name
        cache.append(callback)

    # 泄漏模拟
    for _ in range(10):
        leak()

    print(f"  cache 长度: {len(cache)} (泄漏了 {len(cache)} 个闭包)")
    print("  用 objgraph 可查看引用链: pip install objgraph")


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    refcount_demo()
    circular_ref_demo()
    gc_demo()
    del_trap_demo()
    weakref_demo()
    leak_simulation()
