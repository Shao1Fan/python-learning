"""
collections 模块深度解析
运行: python python_learn/14_advanced_collections/collections_deep.py
"""

from collections import (
    defaultdict, Counter, deque, OrderedDict,
    ChainMap, namedtuple, UserDict, UserList,
)
import json


# ============================================================
# 1. defaultdict — 缺失 key 自动初始化
# ============================================================

def demo_defaultdict():
    print("--- defaultdict ---")

    # 普通 dict
    groups = {}
    for name in ["A", "B", "A", "C", "B", "A"]:
        if name not in groups:
            groups[name] = []
        groups[name].append(name)

    # defaultdict
    groups2 = defaultdict(list)
    for name in ["A", "B", "A", "C", "B", "A"]:
        groups2[name].append(name)

    print(f"  dict: {dict(groups2)}")

    # 嵌套 defaultdict
    nested = defaultdict(lambda: defaultdict(int))
    nested["Alice"]["login"] += 1
    nested["Bob"]["login"] += 1
    nested["Alice"]["login"] += 1
    print(f"  嵌套: {json.dumps(nested, ensure_ascii=False)}")


# ============================================================
# 2. Counter — 计数利器
# ============================================================

def demo_counter():
    print("\n--- Counter ---")
    words = ["apple", "banana", "apple", "orange", "banana", "apple"]
    counter = Counter(words)

    print(f"  计数: {counter}")
    print(f"  最常⻅的2个: {counter.most_common(2)}")
    print(f"  apple 数量: {counter['apple']}")

    # 数学运算
    counter2 = Counter(["apple", "grape", "grape"])
    print(f"  相加: {counter + counter2}")
    print(f"  相减: {counter - counter2}")
    print(f"  交集: {counter & counter2}")
    print(f"  并集: {counter | counter2}")

    # 其他方法
    elements = list(counter.elements())
    print(f"  elements (展开): {sorted(elements)}")
    counter.update(["grape", "grape"])  # 批量增加
    counter.subtract(["apple", "apple"])  # 批量减少
    print(f"  增减后: {counter}")


# ============================================================
# 3. deque — 双端队列
# ============================================================

def demo_deque():
    print("\n--- deque ---")
    dq = deque(maxlen=5)

    # 从右侧添加
    for i in range(6):
        dq.append(i)
        print(f"  添加 {i}: {list(dq)} (超过 maxlen 自动移除最左)")

    # 左侧操作
    dq.appendleft(-1)
    print(f"  左侧添加 -1: {list(dq)}")

    # 旋转
    dq2 = deque([1, 2, 3, 4, 5])
    dq2.rotate(2)  # 右移2
    print(f"  rotate(2): {list(dq2)}")
    dq2.rotate(-2)  # 左移2
    print(f"  rotate(-2): {list(dq2)}")

    # deque 作为队列
    queue = deque()
    queue.append("任务1")
    queue.append("任务2")
    queue.append("任务3")
    print(f"  队列: {list(queue)}")
    print(f"  出队: {queue.popleft()}")
    print(f"  出队: {queue.popleft()}")

    # deque 作为栈
    stack = deque()
    stack.append("页面1")
    stack.append("页面2")
    stack.append("页面3")
    print(f"  栈: {list(stack)}")
    print(f"  出栈: {stack.pop()}")
    print(f"  出栈: {stack.pop()}")


# ============================================================
# 4. OrderedDict — 有序字典
# ============================================================

def demo_ordereddict():
    print("\n--- OrderedDict ---")
    # Python 3.7+ dict 已经保持插入顺序
    # OrderedDict 的特殊功能: popitem(last=) 和 move_to_end()

    od = OrderedDict()
    od["z"] = 1
    od["y"] = 2
    od["x"] = 3
    print(f"  原始: {list(od.items())}")

    # 移到末尾
    od.move_to_end("z")
    print(f"  move_to_end('z'): {list(od.items())}")

    # 移到开头
    od.move_to_end("x", last=False)
    print(f"  move_to_end('x', last=False): {list(od.items())}")

    # 弹出首/尾
    first = od.popitem(last=False)
    last = od.popitem(last=True)
    print(f"  弹出首个: {first}")
    print(f"  弹出末个: {last}")


# ============================================================
# 5. ChainMap — 字典链（作用域链）
# ============================================================

def demo_chainmap():
    print("\n--- ChainMap ---")

    defaults = {"host": "localhost", "port": 8080, "debug": False}
    config = {"port": 9000, "debug": True}
    overrides = {"host": "prod.example.com"}

    # 优先级: overrides > config > defaults
    cm = ChainMap(overrides, config, defaults)
    print(f"  host: {cm['host']}")  # overrides
    print(f"  port: {cm['port']}")  # config
    print(f"  debug: {cm['debug']}")  # config

    # 修改只会影响第一个 map
    cm["timeout"] = 30
    print(f"  overrides: {overrides}")

    # new_child — 创建新链
    cm2 = cm.new_child({"host": "test.server"})
    print(f"  new_child host: {cm2['host']}")


# ============================================================
# 6. namedtuple — 命名元组
# ============================================================

def demo_namedtuple():
    print("\n--- namedtuple ---")
    Point = namedtuple("Point", ["x", "y", "z"])
    pt = Point(1, 2, 3)

    print(f"  pt: {pt}")
    print(f"  pt.x = {pt.x}, pt[0] = {pt[0]}")
    print(f"  解包: x={pt.x}, y={pt.y}, z={pt.z}")

    # _asdict / _replace / _make
    print(f"  asdict: {pt._asdict()}")
    pt2 = pt._replace(x=100)
    print(f"  replace: {pt2}")
    pt3 = Point._make([4, 5, 6])
    print(f"  make: {pt3}")

    # 适合做简单的 DTO
    from typing import NamedTuple

    class Employee(NamedTuple):
        name: str
        age: int
        salary: float

    emp = Employee("Alice", 30, 50000.0)
    print(f"  Employee: {emp}, name={emp.name}")


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    demo_defaultdict()
    demo_counter()
    demo_deque()
    demo_ordereddict()
    demo_chainmap()
    demo_namedtuple()
