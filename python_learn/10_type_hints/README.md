# 10 | 类型注解 (Type Hints)

## 面试常见问题

- `TypeVar` 和 `Generic` 怎么用？
- `Protocol` 的鸭子类型？什么是结构子类型？
- `TypedDict` 和普通 dict 的区别？
- `Optional` / `Union` / `Any` / `Literal` / `Final` 各有什么用？
- `overload` 装饰器干什么用？
- 类型注解是运行时检查还是静态检查？

## 核心概念

```python
# 基础
name: str = "Alice"
age: int

# 函数注解
def greet(name: str, age: int = 18) -> str:
    return f"你好，{name}"

# 泛型
from typing import List, Dict, Optional, Union
nums: List[int] = [1, 2, 3]
config: Dict[str, Union[str, int]] = {"host": "localhost", "port": 8080}
maybe: Optional[str] = None  # Optional[X] == Union[X, None]
```
