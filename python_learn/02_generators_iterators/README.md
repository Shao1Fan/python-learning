# 02 | 生成器与迭代器 (Generators & Iterators)

## 面试常见问题

- `__iter__` 和 `__next__` 的区别？
- 生成器 vs 迭代器 vs 可迭代对象？
- `yield` 和 `yield from` 的区别？
- `send()`、`throw()`、`close()` 的用法？
- 生成器为什么能节省内存？
- 手写一个 `range()` 生成器？

## 核心关系

```
可迭代对象 (Iterable)
  ├── __iter__() → 返回迭代器
  │
  └── 例如: list, dict, str, tuple
  
迭代器 (Iterator)
  ├── __iter__() → return self
  ├── __next__() → 返回下一个元素 / 抛 StopIteration
  │
  └── 例如: 生成器, file对象

生成器 (Generator)
  ├── 用 yield 定义
  ├── 是简化版的迭代器
  ├── 惰性求值、节省内存
  ├── 可双向通信: send() / throw() / close()
  └── yield from: 委托给子生成器
```

## 内存对比

```python
# 列表: 全部载入内存
squares_list = [x * x for x in range(1000000)]   # ~28MB

# 生成器: 惰性求值
squares_gen  = (x * x for x in range(1000000))    # ~56B
```
