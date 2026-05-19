# 14 | 高级集合类型

## 面试常见问题

- `defaultdict` 和普通 dict 的区别？
- `Counter` 的常用方法？
- `deque` 为什么比 list 适合做队列？
- `ChainMap` 的用途？
- `OrderedDict` 和 Python 3.7+ dict 的区别？
- `namedtuple` 和 dataclass 的选择？
- `heapq` 的堆操作？

## 核心对比

| 类型 | 特点 | 适用场景 |
|------|------|----------|
| `defaultdict` | 缺失 key 自动创建默认值 | 分组计数 |
| `Counter` | 计数 + 数学运算 | 频次统计 |
| `deque` | 双端 O(1) 插入/删除 | 队列/栈 |
| `OrderedDict` | 保持插入顺序 | 有序字典（3.7前） |
| `ChainMap` | 多个字典合并视图 | 作用域链 |
| `namedtuple` | 轻量不可变数据 | 简单 DTO |
