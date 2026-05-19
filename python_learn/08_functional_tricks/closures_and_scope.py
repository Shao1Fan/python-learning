"""
闭包、作用域与非局部变量
运行: python python_learn/08_functional_tricks/closures_and_scope.py
"""


# ============================================================
# 1. LEGB 作用域规则
# ============================================================

x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(f"  inner: x = {x}")      # local

    inner()
    print(f"  outer: x = {x}")          # enclosing

print(f"  global: x = {x}")             # global


# ============================================================
# 2. 闭包 (Closure)
# ============================================================

def make_counter():
    """闭包: 维持独立状态"""
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


def make_multiplier(n):
    """闭包: 记住外部参数 n"""
    def multiplier(x):
        return x * n
    return multiplier


# ============================================================
# 3. 闭包陷阱: 延迟绑定 (Late Binding)
# ============================================================

def create_functions_bad():
    """错误示范: 所有函数都返回 9 (最后一个 i 的值)"""
    funcs = []
    for i in range(10):
        funcs.append(lambda: i * i)
    return funcs


def create_functions_good():
    """正确: 用默认参数立即绑定当前 i 的值"""
    funcs = []
    for i in range(10):
        funcs.append(lambda x=i: x * x)
    return funcs


def create_functions_good2():
    """正确: 用闭包捕获当前值"""
    def make_func(i):
        return lambda: i * i
    return [make_func(i) for i in range(10)]


# ============================================================
# 4. nonlocal vs global
# ============================================================

counter_global = 0

def increment_global():
    global counter_global
    counter_global += 1


def make_increment():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment


# ============================================================
# 5. 闭包的实际应用
# ============================================================

def make_averager():
    """计算运行平均值（用闭包维持状态）"""
    series = []

    def averager(value):
        series.append(value)
        return sum(series) / len(series)

    return averager


def make_averager_optimized():
    """优化版: 不存储所有历史值"""
    total = 0.0
    count = 0

    def averager(value):
        nonlocal total, count
        total += value
        count += 1
        return total / count

    return averager


# ============================================================
# 6. 检查闭包
# ============================================================

def examine_closure():
    x = 10
    y = 20

    def inner(z):
        return x + y + z

    return inner


# ============================================================
# 7. 闭包实现装饰器
# ============================================================

def make_logger(prefix):
    """利用闭包实现的日志装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[{prefix}] 调用 {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@make_logger("API")
def api_call(endpoint):
    print(f"  请求: {endpoint}")


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. LEGB 作用域")
    outer()

    print("\n2. 闭包")
    counter1 = make_counter()
    counter2 = make_counter()
    print(f"  counter1: {counter1()}, {counter1()}, {counter1()}")
    print(f"  counter2: {counter2()}, {counter2()} (独立的)")

    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"  double(5) = {double(5)}")
    print(f"  triple(5) = {triple(5)}")

    print("\n3. 闭包陷阱")
    bad_funcs = create_functions_bad()
    good_funcs = create_functions_good()
    print(f"  [错误] bad_funcs[3]() = {bad_funcs[3]()} (期望9, 但都是81)")
    print(f"  [正确] good_funcs[3]() = {good_funcs[3]()}")

    print("\n4. nonlocal vs global")
    inc = make_increment()
    print(f"  nonlocal: {inc()}, {inc()}, {inc()}")
    increment_global()
    print(f"  global: counter_global = {counter_global}")

    print("\n5. 闭包作为有状态函数")
    avg = make_averager_optimized()
    print(f"  avg(10) = {avg(10)}")
    print(f"  avg(20) = {avg(20)}")
    print(f"  avg(30) = {avg(30)}")

    print("\n6. 检查闭包")
    fn = examine_closure()
    print(f"  自由变量: {fn.__code__.co_freevars}")
    print(f"  闭包值: {[c.cell_contents for c in fn.__closure__]}")

    print("\n7. 闭包实现装饰器")
    api_call("/users")
    api_call("/products")
