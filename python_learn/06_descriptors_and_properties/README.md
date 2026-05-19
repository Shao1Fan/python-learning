# 06 | 描述符与 Property

## 面试常见问题

- 描述符协议是什么？
- `@property` 是怎么实现的？
- 非数据描述符和数据描述符的区别？
- 属性访问优先级：`__getattribute__` 怎么查找？
- `__slots__` 的原理和作用？

## 描述符协议

```python
__get__(self, obj, objtype) → value
__set__(self, obj, value)   → None
__delete__(self, obj)       → None
```

| 类型 | `__get__` | `__set__` | 优先级 |
|------|-----------|-----------|--------|
| 数据描述符 | ✅ | ✅ | 最高 |
| 非数据描述符 | ✅ | ❌ | 次于实例 `__dict__` |

## 属性访问顺序

```python
obj.attr  →  type(obj).__mro__ 中查找数据描述符
          →  obj.__dict__
          →  type(obj).__mro__ 中查找非数据描述符
          →  抛 AttributeError
```
