# 12 | DataClass 与模式匹配

## 面试常见问题

- `@dataclass` 自动生成了什么方法？
- `field()` 函数的参数？`default_factory` 的作用？
- `frozen=True` 的效果？
- `__post_init__` 的用途？
- `dataclasses.field(init=False, repr=False)` 场景？
- Python 3.10 的 match/case 语法？
- `@dataclass(slots=True)` （Python 3.10+）？

## 核心对比

| 特性 | 普通类 | dataclass | NamedTuple |
|------|--------|-----------|------------|
| 可变 | ✅ | ✅(可frozen) | ❌ |
| __init__ | 手动 | 自动 | 自动 |
| __repr__ | 手动 | 自动 | 自动 |
| __eq__ | 手动 | 自动 | 自动 |
| __hash__ | 手动 | 自动 | 自动 |
| 继承 | ✅ | ✅ | ❌ |
| 性能 | - | - | 略优 |
