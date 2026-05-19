"""
弱引用（weakref）深入
运行: python python_learn/11_memory_and_gc/weakref_and_slots.py
"""

import weakref
import gc


# ============================================================
# 1. ref — 基础弱引用
# ============================================================

class Person:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Person({self.name!r})"


def ref_basic():
    print("--- weakref.ref 基础 ---")
    p = Person("Alice")
    r = weakref.ref(p)

    print(f"  原始对象: {p}")
    print(f"  弱引用: {r}")
    print(f"  通过弱引用访问: {r()}")

    del p
    print(f"  删除对象后: {r()}")  # None


# ============================================================
# 2. proxy — 代理访问
# ============================================================

def proxy_demo():
    print("\n--- weakref.proxy ---")
    class Data:
        def __init__(self):
            self.value = 42
    data = Data()
    proxy = weakref.proxy(data)

    print(f"  proxy.value = {proxy.value}")

    del data
    try:
        _ = proxy.value
    except ReferenceError as e:
        print(f"  原对象被删除后访问报错: {e}")


# ============================================================
# 3. WeakKeyDictionary / WeakValueDictionary
# ============================================================

def weak_dict_demo():
    print("\n--- WeakValueDictionary ---")
    # 当 value 的对象被回收时，自动删除条目
    cache = weakref.WeakValueDictionary()

    p1 = Person("Alice")
    p2 = Person("Bob")
    cache["user1"] = p1
    cache["user2"] = p2

    print(f"  cache 长度: {len(cache)}")

    del p1
    gc.collect()
    print(f"  删除 Alice 后 cache 长度: {len(cache)}")
    print(f"  cache keys: {list(cache.keys())}")


# ============================================================
# 4. finalize — 清理回调
# ============================================================

def finalize_demo():
    print("\n--- weakref.finalize ---")
    class Database:
        def __init__(self, name):
            self.name = name

        def close(self):
            print(f"  [清理] 关闭数据库连接: {self.name}")

    db = Database("mydb")
    finalizer = weakref.finalize(db, db.close)

    # 当对象被回收时自动调用 close()
    del db
    gc.collect()
    print("  (对象已被回收，cleanup 已自动执行)")


# ============================================================
# 5. 缓存系统: 不阻止对象被回收
# ============================================================

class CachedInstance:
    """实例缓存，但不阻止回收"""
    _cache = weakref.WeakValueDictionary()

    def __new__(cls, instance_id, *args, **kwargs):
        if instance_id in cls._cache:
            print(f"  [缓存命中] {instance_id}")
            return cls._cache[instance_id]

        instance = super().__new__(cls)
        instance.instance_id = instance_id
        cls._cache[instance_id] = instance
        print(f"  [创建新实例] {instance_id}")
        return instance


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    ref_basic()
    proxy_demo()
    weak_dict_demo()
    finalize_demo()

    print("\n--- 缓存系统 ---")
    c1 = CachedInstance("id-1")
    c2 = CachedInstance("id-2")
    c3 = CachedInstance("id-1")  # 缓存命中
    print(f"  c1 is c3: {c1 is c3}")

    # 删除引用后缓存自动清理
    del c1, c3
    gc.collect()
    c4 = CachedInstance("id-1")  # 重新创建
    print(f"  c4 is not c2: {c4 is not c2}")
