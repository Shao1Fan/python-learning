# 07 | 魔术方法 (Magic Methods)

## 面试常见问题

- `__call__` 的作用？让对象可调用
- `__eq__` 和 `__hash__` 的关系？
- `__getattr__` vs `__getattribute__` 的区别？
- `__enter__` / `__exit__` 实现上下文管理器
- `__new__` vs `__init__` 的执行顺序？
- `__repr__` vs `__str__` 的区别？

## 魔术方法分类

| 类别 | 方法 |
|------|------|
| 创建/销毁 | `__new__`, `__init__`, `__del__` |
| 字符串表示 | `__repr__`, `__str__`, `__format__` |
| 容器协议 | `__len__`, `__getitem__`, `__setitem__`, `__delitem__`, `__iter__`, `__contains__` |
| 属性访问 | `__getattr__`, `__getattribute__`, `__setattr__`, `__delattr__` |
| 可调用 | `__call__` |
| 比较 | `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`, `__hash__` |
| 数值运算 | `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__floordiv__`, `__mod__`, `__pow__` |
| 类型转换 | `__int__`, `__float__`, `__bool__`, `__bytes__` |
