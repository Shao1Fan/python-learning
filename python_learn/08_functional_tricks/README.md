# 08 | 函数式技巧

## 面试常见问题

- `functools.partial` 的作用？
- `lru_cache` 和 `cached_property` 的区别？
- `singledispatch` 怎么实现函数重载？
- 闭包的陷阱：延迟绑定问题？
- `nonlocal` 关键字的用途？
- `operator` 模块有什么用？

## 核心函数

| 函数 | 作用 | 场景 |
|------|------|------|
| `partial` | 固定部分参数 | API 封装、回调 |
| `lru_cache` | 缓存函数返回值 | 递归优化、耗时计算 |
| `cached_property` | 缓存属性 | 计算密集型属性（只算一次） |
| `singledispatch` | 单分派泛型 | 替代 if/elif type |
| `wraps` | 保留元数据 | 装饰器必备 |
| `reduce` | 累积运算 | 函数式折叠 |
