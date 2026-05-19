"""
可调用对象、比较与哈希
运行: python python_learn/07_magic_methods/callable_and_compare.py
"""


# ============================================================
# 1. __call__: 让对象可调用
# ============================================================

class Adder:
    def __init__(self, n):
        self.n = n

    def __call__(self, x):
        return self.n + x


class Partial:
    """简化版 functools.partial"""
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        all_args = self.args + args
        all_kwargs = {**self.kwargs, **kwargs}
        return self.func(*all_args, **all_kwargs)


# ============================================================
# 2. __eq__ 和 __hash__ 的关系
# ============================================================

class Point:
    """正确实现 __eq__ 和 __hash__"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class PointWithoutHash:
    """没有 __hash__: 不能放进 set / 作为 dict key"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # 没有定义 __hash__，Python 会自动设为 None


# ============================================================
# 3. __lt__, __gt__ 实现排序
# ============================================================

from functools import total_ordering

@total_ordering
class Student:
    """只需实现 __eq__ 和一个比较方法，其余自动生成"""
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __eq__(self, other):
        return self.score == other.score

    def __lt__(self, other):
        return self.score < other.score

    def __repr__(self):
        return f"Student('{self.name}', {self.score})"


# ============================================================
# 4. __bool__ 自定义真值判断
# ============================================================

class CustomBool:
    def __init__(self, value):
        self.value = value

    def __bool__(self):
        print(f"[__bool__] 判断真值: {self.value}")
        return bool(self.value)


# ============================================================
# 5. __repr__ vs __str__
# ============================================================

class ReprStrDemo:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        """开发者友好: 通常是重构对象的表达式"""
        return f"ReprStrDemo('{self.name}', {self.age})"

    def __str__(self):
        """用户友好: 可读性强"""
        return f"{self.name}({self.age}岁)"


# ============================================================
# 6. 数值运算
# ============================================================

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """向量数乘: v * 3"""
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        """反向乘法: 3 * v"""
        return self.__mul__(scalar)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __neg__(self):
        return Vector(-self.x, -self.y)


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. __call__")
    add5 = Adder(5)
    print(f"  add5(3) = {add5(3)}")

    add10 = Partial(Adder(0).__call__, 10)
    # 更实用的例子:
    def power(base, exp):
        return base ** exp
    square = Partial(power, exp=2)
    cube = Partial(power, exp=3)
    print(f"  square(4) = {square(4)}")
    print(f"  cube(3) = {cube(3)}")

    print("\n2. __eq__ 和 __hash__")
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(3, 4)
    print(f"  p1 == p2: {p1 == p2}")
    print(f"  p1 == p3: {p1 == p3}")
    point_set = {p1, p2, p3}
    print(f"  set长度: {len(point_set)}（p1,p2 相等，所以只有2个）")

    print("\n3. @total_ordering 自动补全比较")
    students = [
        Student("张三", 88),
        Student("李四", 95),
        Student("王五", 72),
    ]
    students.sort()
    print(f"  排序后: {students}")
    print(f"  张三 > 王五: {students[0] > students[1]}")

    print("\n4. __bool__")
    if CustomBool(True):
        print("  真值判断通过")

    print("\n5. __repr__ vs __str__")
    r = ReprStrDemo("Alice", 25)
    print(f"  repr: {r!r}")
    print(f"  str:  {r!s}")

    print("\n6. 向量运算")
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print(f"  {v1} + {v2} = {v1 + v2}")
    print(f"  {v1} * 3 = {v1 * 3}")
    print(f"  3 * {v1} = {3 * v1}")
    print(f"  |{v1}| = {abs(v1)}")
