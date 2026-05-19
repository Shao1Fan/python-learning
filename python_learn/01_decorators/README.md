# 01 | 装饰器 (Decorators)

## 面试常见问题

- 装饰器的本质是什么？
- `@functools.wraps` 有什么用？
- 带参数的装饰器怎么写？
- 类装饰器和函数装饰器有什么区别？
- 多个装饰器的执行顺序？
- 装饰器在工程中有什么实际用途？

## 核心概念

| 概念 | 说明 |
|------|------|
| 闭包 | 内层函数持有外层函数作用域的引用 |
| `@语法糖` | `@dec` 等价于 `func = dec(func)` |
| `functools.wraps` | 保留原函数的 `__name__`、`__doc__` 等属性 |
| 装饰器工厂 | 外层再包一层函数接收参数 |
| 类装饰器 | 通过 `__call__` 使类实例可调用 |

## 执行顺序

```python
@decorator_a
@decorator_b
def func():
    pass

# 等价于：
func = decorator_a(decorator_b(func))
# 执行时：先执行 decorator_b 的包裹逻辑 → 再执行 decorator_a 的包裹逻辑
```
