"""
heapq (堆) 与 array (数组)
运行: python python_learn/14_advanced_collections/heapq_and_array.py
"""

import heapq
import array
import random


# ============================================================
# 1. heapq — 堆排序基础
# ============================================================

def demo_heapq_basic():
    print("--- heapify / heappush / heappop ---")
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    heap = []

    for v in data:
        heapq.heappush(heap, v)
    print(f"  堆 (小顶堆): {heap}")

    # 弹出最小元素
    smallest = heapq.heappop(heap)
    print(f"  弹出最小: {smallest}")
    print(f"  剩余: {heap}")

    # heapify: 原地建堆
    data2 = [3, 1, 4, 1, 5, 9, 2, 6]
    heapq.heapify(data2)
    print(f"  heapify 后: {data2}")


# ============================================================
# 2. nlargest / nsmallest
# ============================================================

def demo_nlargest():
    print("\n--- nlargest / nsmallest ---")
    data = random.sample(range(1, 100), 20)
    print(f"  数据: {data}")
    print(f"  最大的3个: {heapq.nlargest(3, data)}")
    print(f"  最小的3个: {heapq.nsmallest(3, data)}")

    # 按 key 排序
    students = [
        {"name": "Alice", "score": 88},
        {"name": "Bob", "score": 95},
        {"name": "Charlie", "score": 72},
        {"name": "David", "score": 91},
    ]
    top2 = heapq.nlargest(2, students, key=lambda s: s["score"])
    print(f"  分数最高的2个: {[s['name'] for s in top2]}")


# ============================================================
# 3. 堆实现优先队列
# ============================================================

class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._counter = 0

    def push(self, item, priority=0):
        """优先级越小越先出"""
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def pop(self):
        return heapq.heappop(self._heap)[-1]

    def __bool__(self):
        return bool(self._heap)

    def __len__(self):
        return len(self._heap)


def demo_priority_queue():
    print("\n--- 优先队列 ---")
    pq = PriorityQueue()
    pq.push("普通任务", 5)
    pq.push("紧急任务", 1)
    pq.push("次要任务", 10)
    pq.push("加急任务", 2)

    print("  执行顺序:")
    while pq:
        print(f"    {pq.pop()}")


# ============================================================
# 4. 合并有序序列
# ============================================================

def demo_merge():
    print("\n--- merge 合并有序序列 ---")
    list1 = [1, 3, 5, 7]
    list2 = [2, 4, 6, 8]
    list3 = [0, 9, 10]

    merged = list(heapq.merge(list1, list2, sorted(list3)))
    print(f"  合并结果: {merged}")


# ============================================================
# 5. 堆应用: 最大值/最小值维护
# ============================================================

class RunningMedian:
    """流式数据中位数"""
    def __init__(self):
        self._small = []  # 最大堆 (存负数)
        self._large = []  # 最小堆

    def add(self, value):
        if not self._small or value <= -self._small[0]:
            heapq.heappush(self._small, -value)
        else:
            heapq.heappush(self._large, value)

        # 平衡两个堆
        if len(self._small) > len(self._large) + 1:
            heapq.heappush(self._large, -heapq.heappop(self._small))
        elif len(self._large) > len(self._small):
            heapq.heappush(self._small, -heapq.heappop(self._large))

    def median(self):
        if len(self._small) == len(self._large):
            return (-self._small[0] + self._large[0]) / 2
        return -self._small[0]


def demo_median():
    print("\n--- 流式中位数 ---")
    rm = RunningMedian()
    for v in [5, 3, 8, 1, 9, 2, 7]:
        rm.add(v)
        print(f"  添加 {v}, 中位数: {rm.median()}")


# ============================================================
# 6. array — 类型化数组
# ============================================================

def demo_array():
    print("\n--- array ---")
    # 'i' = signed int, 'f' = float, 'd' = double
    arr = array.array('i', [1, 2, 3, 4, 5])
    print(f"  array('i'): {arr}")
    print(f"  类型: {arr.typecode}")
    print(f"  字节大小: {arr.itemsize} bytes/item")

    arr.append(6)
    arr.extend([7, 8])
    print(f"  扩展后: {list(arr)}")

    # 与 list 内存对比
    import sys
    list_data = list(range(1000))
    arr_data = array.array('i', range(1000))
    print(f"  1000 个元素:")
    print(f"    list 内存: {sys.getsizeof(list_data):,} 字节 (+元素本身)")
    print(f"    array 内存: {sys.getsizeof(arr_data):,} 字节 (内联存储)")


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    demo_heapq_basic()
    demo_nlargest()
    demo_priority_queue()
    demo_merge()
    demo_median()
    demo_array()
