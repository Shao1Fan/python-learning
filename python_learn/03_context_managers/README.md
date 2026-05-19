# 03 | 上下文管理器 (Context Managers)

## 面试常见问题

- `with` 语句的原理？
- `__enter__` 和 `__exit__` 返回值的作用？
- `contextmanager` 装饰器怎么用？
- 如何写一个支持 `with` 的数据库连接？
- `contextlib.suppress` 和 `contextlib.ExitStack` 是什么？
- 上下文管理器在什么场景下比 try/finally 更优雅？

## 关键要点

```python
with open("file.txt") as f:
    ...

# 等价于：
f = open("file.txt")
try:
    ...
finally:
    f.close()
```

| 方法 | 作用 | 返回值 |
|------|------|--------|
| `__enter__` | 进入 with 块时调用 | 赋值给 as 后面的变量 |
| `__exit__` | 离开 with 块时调用（无论是否异常） | True 表示吞掉异常 |
