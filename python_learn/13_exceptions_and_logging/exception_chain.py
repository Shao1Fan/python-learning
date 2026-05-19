"""
异常链与自定义异常
运行: python python_learn/13_exceptions_and_logging/exception_chain.py
"""

import traceback
import sys


# ============================================================
# 1. try/except/else/finally 执行顺序
# ============================================================

def demo_execution_order():
    print("--- 执行顺序 ---")

    def test(value):
        print(f"  try: value={value}")
        try:
            print("    进入 try 块")
            if value == 0:
                raise ValueError("value 为 0")
            result = 10 / value
        except ZeroDivisionError:
            print("    进入 except: ZeroDivisionError")
        except ValueError as e:
            print(f"    进入 except: ValueError - {e}")
        else:
            print(f"    进入 else: 成功，result={result}")
            return result
        finally:
            print("    进入 finally (总是执行)")

        return None

    print("  [测试1] value=2")
    print(f"  返回值: {test(2)}\n")

    print("  [测试2] value=0")
    print(f"  返回值: {test(0)}\n")

    print("  [测试3] value=0.0 (触发 ZeroDivisionError)")
    print(f"  返回值: {test(0.0)}\n")


# ============================================================
# 2. raise from — 异常链
# ============================================================

def db_query(user_id):
    """模拟数据库查询"""
    raise ConnectionError("数据库连接超时")


def get_user_name(user_id):
    try:
        return db_query(user_id)
    except ConnectionError as e:
        # raise from 保留原始异常上下文
        raise RuntimeError("获取用户信息失败") from e


def demo_exception_chain():
    print("\n--- raise from 异常链 ---")
    try:
        get_user_name(42)
    except RuntimeError as e:
        print(f"  异常: {e}")
        print(f"  原始异常: {e.__cause__}")
        print("  完整追踪:")
        traceback.print_exception(type(e), e, e.__traceback__)


# ============================================================
# 3. 自定义异常
# ============================================================

class AppError(Exception):
    """应用基础异常"""
    def __init__(self, message: str, code: int = 500):
        self.code = code
        super().__init__(f"[{code}] {message}")


class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id):
        super().__init__(f"{resource}({resource_id}) 未找到", code=404)


class ValidationError(AppError):
    def __init__(self, field: str, reason: str):
        super().__init__(f"字段 '{field}' 校验失败: {reason}", code=422)


class AuthError(AppError):
    def __init__(self, message: str = "未授权访问"):
        super().__init__(message, code=401)


def find_user(user_id):
    if user_id != 1:
        raise NotFoundError("用户", user_id)
    return {"id": 1, "name": "Alice"}


# ============================================================
# 4. 异常抑制与上下文重置
# ============================================================

def demo_suppress_and_context():
    print("\n--- raise ... from None ---")

    def internal():
        try:
            return int("不是数字")
        except ValueError:
            # suppress=True: 不暴露内部异常细节
            raise RuntimeError("解析失败") from None

    try:
        internal()
    except RuntimeError as e:
        print(f"  异常: {e}")
        print(f"  __cause__: {e.__cause__}")
        print(f"  __suppress_context__: {e.__suppress_context__}")


# ============================================================
# 5. sys.exc_info — 获取当前异常信息
# ============================================================

def demo_exc_info():
    print("\n--- sys.exc_info() ---")
    try:
        raise ValueError("测试异常")
    except ValueError:
        exc_type, exc_val, exc_tb = sys.exc_info()
        print(f"  类型: {exc_type.__name__}")
        print(f"  值: {exc_val}")
        print(f"  跟踪: {exc_tb.tb_frame.f_code.co_name}")

        # 重要: 避免循环引用，处理完后清理
        del exc_tb


# ============================================================
# 6. 异常处理模式: 重试 / 降级
# ============================================================

import time

class RetryableError(Exception):
    """可重试的异常"""
    pass

class FatalError(Exception):
    """不可重试的异常"""
    pass


def unstable_operation(attempt):
    if attempt < 2:
        raise RetryableError("暂时失败")
    if attempt == 2:
        raise FatalError("不可恢复")
    return "成功"


def with_retry(func, max_retries=3, delay=0.1):
    for attempt in range(1, max_retries + 1):
        try:
            return func(attempt)
        except RetryableError as e:
            print(f"  第{attempt}次重试: {e}")
            if attempt == max_retries:
                raise
            time.sleep(delay)
        except FatalError:
            raise  # 不重试


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    demo_execution_order()
    demo_exception_chain()
    demo_suppress_and_context()
    demo_exc_info()

    print("\n--- 自定义异常 ---")
    try:
        find_user(999)
    except AppError as e:
        print(f"  捕获: {e} (code={e.code})")

    try:
        raise ValidationError("email", "格式不正确")
    except AppError as e:
        print(f"  捕获: {e}")

    print("\n--- 重试模式 ---")
    try:
        result = with_retry(unstable_operation)
        print(f"  最终结果: {result}")
    except FatalError:
        print("  遇到致命错误，停止重试")
