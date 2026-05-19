"""
装饰器实战案例
运行: python python_learn/01_decorators/examples.py
"""

import functools
import time
import logging
from typing import Callable, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


# ============================================================
# 案例1: 权限校验装饰器
# ============================================================

class User:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role


def require_role(role: str):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(user: User, *args, **kwargs):
            if user.role != role:
                raise PermissionError(f"用户 {user.name} 没有 {role} 权限")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator


@require_role("admin")
def delete_database(user: User):
    print(f"[危险操作] {user.name} 删除了数据库！")


# ============================================================
# 案例2: 日志装饰器（带参数支持）
# ============================================================

def log(level: str = "INFO"):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.log(getattr(logging, level), f"调用 {func.__name__}，参数: {args} {kwargs}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@log("INFO")
def process_order(order_id: str):
    print(f"处理订单 {order_id}")


# ============================================================
# 案例3: 单例模式装饰器
# ============================================================

def singleton(cls):
    instances = {}
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class Database:
    def __init__(self):
        self.connected = False
        print("创建 Database 实例（仅一次）")

    def connect(self):
        self.connected = True
        print("数据库已连接")


# ============================================================
# 案例4: 超时控制装饰器
# ============================================================

import signal

class TimeoutError_(Exception):
    pass

def timeout(seconds: int):
    def decorator(func: Callable) -> Callable:
        def handler(signum, frame):
            raise TimeoutError_(f"函数 {func.__name__} 执行超时 ({seconds}s)")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if hasattr(signal, "SIGALRM"):
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(seconds)
                try:
                    return func(*args, **kwargs)
                finally:
                    signal.alarm(0)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator


@timeout(2)
def long_running_task():
    print("开始耗时任务...")
    time.sleep(10)
    return "完成"


# ============================================================
# 案例5: 注册表模式（插件系统）
# ============================================================

PLUGINS = {}

def register(func: Callable) -> Callable:
    PLUGINS[func.__name__] = func
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@register
def format_json(data):
    return {"type": "json", "data": data}

@register
def format_xml(data):
    return {"type": "xml", "data": data}

def run_plugin(name: str, data: Any):
    if name not in PLUGINS:
        raise KeyError(f"未知插件: {name}")
    return PLUGINS[name](data)


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("案例1: 权限校验")
    admin = User("Alice", "admin")
    user = User("Bob", "user")
    delete_database(admin)
    # delete_database(user)  # 会抛 PermissionError

    print("\n案例2: 日志装饰器")
    process_order("ORD-2024-001")

    print("\n案例3: 单例装饰器")
    db1 = Database()
    db2 = Database()
    print(f"db1 is db2: {db1 is db2}")

    print("\n案例4: 超时控制（仅 Linux/Mac 有效）")
    # try:
    #     long_running_task()
    # except TimeoutError_ as e:
    #     print(e)

    print("\n案例5: 插件注册表")
    print(run_plugin("format_json", {"key": "value"}))
    print("已注册的插件:", list(PLUGINS.keys()))
