"""
logging 模块深入使用
运行: python python_learn/13_exceptions_and_logging/logging_101.py
"""

import logging
import logging.handlers
import sys
import tempfile
import os


# ============================================================
# 1. 基础配置
# ============================================================

def basic_config():
    print("--- 基础日志配置 ---")
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )

    logger = logging.getLogger("demo.basic")
    logger.debug("这是 DEBUG 信息")
    logger.info("这是 INFO 信息")
    logger.warning("这是 WARNING 信息")
    logger.error("这是 ERROR 信息")


# ============================================================
# 2. Logger 层级关系
# ============================================================

def logger_hierarchy():
    print("\n--- Logger 层级 ---")
    parent = logging.getLogger("app")
    child = logging.getLogger("app.service")
    grandchild = logging.getLogger("app.service.db")

    # 子 logger 默认传播给父 logger
    parent.setLevel(logging.WARNING)

    print(f"  parent: {parent.name}, level={parent.level}")
    print(f"  child: {child.name}, effective_level={child.getEffectiveLevel()}")
    print(f"  grandchild: {grandchild.name}, effective_level={grandchild.getEffectiveLevel()}")


# ============================================================
# 3. 自定义 Handler 和 Formatter
# ============================================================

def custom_handlers():
    print("\n--- 自定义 Handler ---")
    logger = logging.getLogger("demo.custom")
    logger.setLevel(logging.DEBUG)

    # 清空已有 handler
    logger.handlers.clear()

    # 控制台 Handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(
        "[%(levelname)s] %(message)s"
    ))
    logger.addHandler(console)

    # 文件 Handler
    log_file = os.path.join(tempfile.gettempdir(), "demo_app.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(name)s | %(message)s"
    ))
    logger.addHandler(file_handler)

    logger.debug("这条只在控制台显示")
    logger.info("这条在控制台和文件都显示")
    logger.error("错误信息也双向显示")

    print(f"  日志文件: {log_file}")
    with open(log_file, 'r') as f:
        print(f"  文件内容:\n    {f.read().strip()}")
    os.unlink(log_file)


# ============================================================
# 4. RotatingFileHandler — 日志轮转
# ============================================================

def rotating_handler():
    print("\n--- RotatingFileHandler ---")
    logger = logging.getLogger("demo.rotating")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    log_file = os.path.join(tempfile.gettempdir(), "rotating.log")
    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=100, backupCount=3, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)

    # 写入超过 maxBytes 的数据，触发轮转
    for i in range(20):
        logger.info(f"日志行 {i} - " + "x" * 20)

    files = [f for f in os.listdir(tempfile.gettempdir()) if f.startswith("rotating")]
    print(f"  轮转后的文件: {files}")
    for f in files:
        os.unlink(os.path.join(tempfile.gettempdir(), f))


# ============================================================
# 5. 日志过滤器
# ============================================================

class SensitiveDataFilter(logging.Filter):
    """过滤敏感数据"""
    def filter(self, record):
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            record.msg = record.msg.replace("password=", "password=***")
        return True


def log_filter_demo():
    print("\n--- 日志过滤器 ---")
    logger = logging.getLogger("demo.filter")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    handler.addFilter(SensitiveDataFilter())
    logger.addHandler(handler)

    logger.info("用户登录: username=admin, password=secret123")
    logger.info("正常信息: 操作成功")


# ============================================================
# 6. 结构化日志 (JSON)
# ============================================================

import json

class JSONFormatter(logging.Formatter):
    """输出 JSON 格式日志"""
    def format(self, record):
        log_entry = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, ensure_ascii=False)


def json_logging():
    print("\n--- JSON 结构化日志 ---")
    logger = logging.getLogger("demo.json")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

    logger.info("用户操作", extra={"user_id": 42, "action": "login"})


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    basic_config()
    logger_hierarchy()
    custom_handlers()
    rotating_handler()
    log_filter_demo()
    json_logging()
