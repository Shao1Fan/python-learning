# Python 面试 100 题

> 按频率排列，🔥 越多越常考

---

## 一、语言基础（🔥🔥🔥🔥🔥）

### 1. `is` 和 `==` 的区别？
- `is` 比较内存地址（`id()`）
- `==` 比较值（`__eq__`）
- 小整数缓存池 `[-5, 256]` 会导致 `is` 意外为 `True`

### 2. 可变对象 vs 不可变对象
```python
# 不可变: int, str, tuple, frozenset
# 可变: list, dict, set
a = [1, 2]
b = [1, 2]
a is b  # False
a == b  # True
```

### 3. 默认参数陷阱
```python
def bad(item, items=[]):  # items 是函数属性，所有调用共享
    items.append(item)
    return items

bad(1)  # [1]
bad(2)  # [1, 2] ← 不是 [2]！

# 正确:
def good(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 4. `*args` 和 `**kwargs`
- `*args` 接收位置参数 → tuple
- `**kwargs` 接收关键字参数 → dict
- 解包: `func(*list, **dict)`

### 5. 浅拷贝 vs 深拷贝
```python
import copy
a = [[1, 2], [3, 4]]
b = copy.copy(a)          # 浅: 外层新对象，内层仍引用
c = copy.deepcopy(a)      # 深: 完全独立
```

### 6. `@staticmethod` vs `@classmethod` vs 实例方法
- 实例方法: 第一个参数 `self`
- `@classmethod`: 第一个参数 `cls`，可被子类继承/重写
- `@staticmethod`: 无特殊参数，纯粹放在类命名空间的函数

### 7. 列表推导式 vs 生成器表达式
```python
[x * x for x in range(10)]      # 列表 → 立即求值
(x * x for x in range(10))      # 生成器 → 惰性求值
```

### 8. `for` 循环的 `else` 子句
```python
for x in range(10):
    if x > 5:
        break
else:
    # 循环没有被 break 时执行
    pass
```

### 9. `try/except/else/finally` 执行顺序
- `try` → 无异常 → `else` → `finally`
- `try` → 有异常 → `except` → `finally`

### 10. `__new__` vs `__init__`
- `__new__` 创建对象（返回实例）
- `__init__` 初始化对象
- `__new__` 先于 `__init__` 执行

---

## 二、装饰器（🔥🔥🔥🔥🔥）

### 11. 装饰器本质是什么？
函数是"一等公民"，装饰器是一个接受函数并返回新函数的可调用对象。

### 12. `@functools.wraps` 的作用？
保留原函数的 `__name__`、`__doc__`、`__module__` 等元信息。

### 13. 多个装饰器的执行顺序？
```python
@A
@B
def f(): pass
# f = A(B(f))
# 执行: 先进入 A 的 wrapper，再进入 B 的 wrapper，再执行原函数
```

### 14. 带参数的装饰器怎么实现？
再包一层工厂函数：
```python
def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator
```

### 15. 类装饰器和函数装饰器的区别？
类装饰器通过 `__call__` 实现，可以更自然地维护状态。

### 16. 写一个缓存装饰器
```python
def cache(func):
    memo = {}
    @wraps(func)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        result = func(*args)
        memo[args] = result
        return result
    return wrapper
```

### 17. 装饰器在工程中的实际用途？
日志、权限校验、重试、缓存、计时、单例、注册表、事务管理。

---

## 三、生成器与迭代器（🔥🔥🔥🔥🔥）

### 18. 迭代器 vs 可迭代对象？
- 可迭代对象: 实现了 `__iter__` 或 `__getitem__`
- 迭代器: 实现了 `__iter__` + `__next__`，会抛出 `StopIteration`

### 19. 生成器怎么节省内存？
惰性求值，一次只生成一个值，不把全部数据加载到内存。

### 20. `yield` 和 `yield from` 的区别？
- `yield` 返回一个值，暂停执行
- `yield from` 委托给子生成器，简化嵌套生成器的迭代

### 21. `send()`、`throw()`、`close()` 的用途？
- `send(value)`: 向生成器发送值（从 yield 表达式返回）
- `throw(exc)`: 在 yield 处抛出异常
- `close()`: 在 yield 处抛 `GeneratorExit`

### 22. 手写一个 `range()` 生成器？
```python
def my_range(n):
    i = 0
    while i < n:
        yield i
        i += 1
```

### 23. itertools 高频用法？
- `chain` 串联迭代器
- `groupby` 分组（需先排序）
- `product` 笛卡尔积
- `combinations` / `permutations` 排列组合
- `cycle` 无限循环

---

## 四、上下文管理器（🔥🔥🔥🔥）

### 24. `with` 语句的原理？
```python
with EXPR as VAR:
    BLOCK
# 等效于:
VAR = EXPR.__enter__()
try:
    BLOCK
finally:
    VAR.__exit__(...)
```

### 25. `__exit__` 返回 `True` 的作用？
吞掉异常，`with` 块后的代码继续执行。

### 26. `@contextmanager` 怎么用？
```python
from contextlib import contextmanager
@contextmanager
def my_context():
    print("enter")
    try:
        yield
    finally:
        print("exit")
```

### 27. `contextlib.suppress` 的作用？
```python
with suppress(FileNotFoundError):
    os.remove("file.txt")  # 文件不存在也不报错
```

### 28. `ExitStack` 的应用？
动态管理多个上下文管理器，比如打开不确定数量的文件。

---

## 五、异步编程（🔥🔥🔥🔥🔥）

### 29. async/await 原理？
- `async def` 定义协程，调用返回协程对象
- `await` 挂起当前协程，让出控制权给事件循环
- 事件循环调度所有协程，实现并发

### 30. `await` 后面可以跟什么？
- 协程 (`coroutine`)
- `asyncio.Task`
- `asyncio.Future`
- 实现了 `__await__` 的对象

### 31. `gather` vs `create_task`？
- `gather` 并发等待多个协程，返回结果列表
- `create_task` 在后台调度协程，返回 Task 对象

### 32. 协程、线程、进程的选择？

| 维度 | 协程 | 线程 | 进程 |
|------|------|------|------|
| IO 密集型 | ✅✅ | ✅ | ⚠️ |
| CPU 密集型 | ❌ | ❌ (GIL) | ✅ |
| 切换开销 | 极低 | 中 | 高 |

### 33. GIL 是什么？
全局解释器锁 (Global Interpreter Lock)，保证同一时刻只有一个线程执行 Python 字节码。

### 34. 如何绕开 GIL？
- 多进程
- C 扩展
- `asyncio`（本身就是单线程）
- `numpy` 等底层用 C 实现的库

### 35. async 上下文管理器怎么写？
```python
class AsyncResource:
    async def __aenter__(self): ...
    async def __aexit__(self, *args): ...
```

### 36. async 迭代器怎么写？
```python
class AsyncRange:
    def __aiter__(self): return self
    async def __anext__(self): ...
```

---

## 六、元类（🔥🔥🔥）

### 37. 什么是元类？
元类是"类的类"。`type` 是所有类的元类。元类拦截类的创建过程。

### 38. 元类的应用场景？
- 单例模式
- ORM（如 SQLAlchemy）
- 自动注册子类
- API 校验框架

### 39. `__init_subclass__` 和元类的关系？
`__init_subclass__` 是 Python 3.6 引入的"元类轻量替代"，在父类被继承时触发。

### 40. `__new__` 和 `__init__` 在元类中的区别？
- `__new__`: 创建类对象（返回 class）
- `__init__`: 初始化类对象

---

## 七、描述符与 Property（🔥🔥🔥🔥）

### 41. 描述符协议是什么？
```python
__get__(self, obj, objtype)
__set__(self, obj, value)
__delete__(self, obj)
```

### 42. 数据描述符 vs 非数据描述符？
- 数据描述符: 实现了 `__get__` + `__set__`/`__delete__`
- 非数据描述符: 只实现了 `__get__`
- 数据描述符优先级高于实例 `__dict__`

### 43. `@property` 原理？
`property` 是一个数据描述符，把方法调用变成属性访问。

### 44. 属性查找顺序？
1. 数据描述符（类字典）
2. 实例 `__dict__`
3. 非数据描述符
4. `__getattr__`

### 45. `__slots__` 的作用？
- 节省内存（去掉 `__dict__`）
- 限制动态添加属性
- 属性访问速度略有提升

---

## 八、魔术方法（🔥🔥🔥）

### 46. `__call__` 的用途？
让对象可调用，适合做有状态的函数/装饰器/工厂。

### 47. `__eq__` 和 `__hash__` 的关系？
- 定义了 `__eq__` 的类，`__hash__` 会被自动设为 `None`
- 需要同时实现两者才能放进 set / 作为 dict key
- 哈希值基于 `__eq__` 的字段计算

### 48. `__repr__` vs `__str__`？
- `__repr__`: 开发者友好，应能重建对象
- `__str__`: 用户友好，可读性强

### 49. `__getattr__` vs `__getattribute__`？
- `__getattribute__`: 所有属性访问都会调
- `__getattr__`: 属性不存在时才调

### 50. `__del__` 的陷阱？
- 调用时机不确定
- 循环引用 + `__del__` 会导致对象无法被 GC 回收

---

## 九、函数式技巧（🔥🔥🔥🔥）

### 51. `functools.partial` 的作用？
固定函数的部分参数，返回新函数。

### 52. `lru_cache` 和 `cached_property` 的区别？
- `lru_cache`: 缓存函数返回值，可设置 maxsize
- `cached_property`: 缓存属性值（类级别），只计算一次

### 53. `singledispatch` 是什么？
单分派泛型函数，根据第一个参数的类型调用不同实现。

### 54. 闭包 (Closure) 是什么？
内层函数持有外层函数作用域引用的组合。可用于维持状态、装饰器、回调。

### 55. 闭包陷阱（延迟绑定）？
```python
funcs = [lambda: i * i for i in range(10)]
funcs[3]()  # 81，不是 9
# 修正: 用默认参数绑定当前值
```

### 56. `nonlocal` 和 `global` 的区别？
- `global`: 声明变量是全局作用域
- `nonlocal`: 声明变量是外层闭包作用域

---

## 十、并发与并行（🔥🔥🔥🔥🔥）

### 57. 进程和线程的区别？
- 进程: 独立内存空间，切换开销大
- 线程: 共享内存，切换开销小，有 GIL

### 58. `Lock` vs `RLock` vs `Semaphore`？
- `Lock`: 互斥锁，不可重入
- `RLock`: 可重入锁，同一线程可多次 acquire
- `Semaphore`: 允许多少个线程同时访问

### 59. 死锁的四个条件？
互斥、持有并等待、不可剥夺、循环等待。

### 60. `Queue` 在线程间通信？
`queue.Queue` 是线程安全的，内部使用 `Condition` + `Lock`。

### 61. `concurrent.futures` 的两种 Executor？
- `ThreadPoolExecutor`: 线程池（IO 密集型）
- `ProcessPoolExecutor`: 进程池（CPU 密集型）

### 62. 进程间通信方式？
`Queue`、`Pipe`、`shared_memory`、`Manager`、`Value`/`Array`。

---

## 十一、类型注解（🔥🔥🔥）

### 63. `Optional[X]` 和 `Union[X, None]` 的关系？
两者等价，`Optional[X]` 是 `Union[X, None]` 的简写。

### 64. `Protocol` 的用途？
结构子类型（鸭子类型），定义接口而不需要显式继承。

### 65. `TypeVar` 和 `Generic` 的用途？
- `TypeVar`: 类型变量，创建泛型函数
- `Generic`: 创建泛型类

### 66. `TypedDict` 和普通 dict 的区别？
`TypedDict` 指定了键和值的类型（只在类型检查时生效）。

### 67. `@overload` 的作用？
为同一个函数声明多个类型签名。

### 68. `Literal` 和 `Final` 的作用？
- `Literal`: 限制为具体的字面量值
- `Final`: 标记为常量，禁止重新赋值

---

## 十二、DataClass 与模式匹配（🔥🔥🔥🔥）

### 69. `@dataclass` 自动生成了什么？
`__init__`、`__repr__`、`__eq__`，条件：`__hash__`、`__lt__` 等。

### 70. `field()` 常用参数？
- `default` / `default_factory`: 默认值
- `init`: 是否参与 `__init__`
- `repr`: 是否在 `__repr__` 中显示
- `compare`: 是否参与比较
- `hash`: 是否参与哈希

### 71. `frozen=True` 的效果？
生成不可变对象，`__setattr__` 和 `__delattr__` 会抛异常。

### 72. `__post_init__` 的用途？
初始化后的钩子，用于校验或派生字段。

### 73. `match/case` (Python 3.10+) 支持匹配什么？
字面值、序列、字典、dataclass、类型 + `if` 守卫、OR 模式。

---

## 十三、内存管理（🔥🔥🔥）

### 74. Python 的垃圾回收机制？
- 主要: 引用计数
- 辅助: 分代回收（处理循环引用）

### 75. 循环引用怎么处理？
GC 的分代回收算法会遍历对象图，标记不可达的循环引用对象。

### 76. 分代回收的阈值？
默认 `(700, 10, 10)`，即第0代触发700次后执行第0代GC，等。

### 77. `weakref` 的用途？
建立弱引用，不增加引用计数，不影响对象生命周期。适用于缓存、回调、避免循环引用。

### 78. 如何检测内存泄漏？
- `gc.get_objects()`
- `objgraph` 库
- `tracemalloc` 模块

---

## 十四、异常与日志（🔥🔥🔥）

### 79. `raise from` 的作用？
保留异常链信息，`__cause__` 属性记录原始异常。

### 80. 自定义异常的最佳实践？
```python
class AppError(Exception):
    def __init__(self, message, code=500):
        self.code = code
        super().__init__(message)
```

### 81. logging 的日志级别？
DEBUG < INFO < WARNING < ERROR < CRITICAL

### 82. Logger 的传播机制？
子 Logger 默认向父 Logger 传播日志，可通过 `propagate = False` 关闭。

### 83. logging 和 print 的选择？
生产环境必须用 logging，因为它支持日志级别、格式控制、输出重定向、轮转等。

---

## 十五、高级集合（🔥🔥🔥）

### 84. `defaultdict` 的工作原理？
缺失 key 时调用 `default_factory` 创建默认值。

### 85. `Counter` 的 `most_common` 原理？
使用 `heapq.nlargest` 获取频率最高的 N 个元素。

### 86. `deque` 为什么比 list 适合做队列？
`deque` 两端插入/删除都是 O(1)，list 头部操作是 O(n)。

### 87. `ChainMap` 适合什么场景？
作用域链、配置合并（多个 dict 优先级叠加）。

### 88. `namedtuple` 和 dataclass 怎么选？
- `namedtuple`: 轻量、不可变、占用小
- `dataclass`: 功能丰富、可变、支持继承

### 89. `heapq` 是大顶堆还是小顶堆？
Python 的 heapq 是小顶堆。要实现大顶堆，可以存储负值。

---

## 十六、综合与开放题（🔥🔥🔥🔥🔥）

### 90. 什么是 Python 的"一等公民"？
函数、类、对象都是"值"，可以赋值给变量、作为参数传递、作为返回值。

### 91. 解释 `__name__ == '__main__'`？
当前模块作为脚本直接运行时 `__name__` 为 `__main__`，被导入时为模块名。

### 92. Python 的 `with` 语句除了文件还有哪些用途？
数据库事务、计时器、锁、临时环境变量、打印缩进。

### 93. `pickle` 和 `json` 的区别？
- `pickle`: Python 专属，支持任意对象
- `json`: 跨语言，只支持基本类型，安全

### 94. 深拷贝、浅拷贝、赋值三者的区别？
- 赋值: 引用同一对象
- 浅拷贝: 新容器，但元素是引用
- 深拷贝: 完全独立

### 95. GIL 会被移除吗？
目前没有计划彻底移除，但 `free-threaded Python`（3.13t）已在实验阶段。

### 96. WSGI 和 ASGI 的区别？
- WSGI: 同步 Web 接口标准
- ASGI: 异步 Web 接口标准（支持 WebSocket）

### 97. Python 中如何实现单例？
- 元类
- 装饰器
- `__new__`
- 模块（模块是天然单例）

### 98. 接口/抽象类的实现方式？
- ABC（`abc.ABC` + `@abstractmethod`）
- `Protocol`（结构子类型）

### 99. 配置文件处理方式？
- `configparser` (ini)
- `json`
- `yaml`
- `pydantic-settings` (环境变量)

### 100. Python 中如何处理大文件？
- 逐行读取 (`for line in file`)
- 分块读取 (`file.read(chunk_size)`)
- 使用生成器
- 使用 `mmap`
