"""Secure Python code execution sandbox.

Constraints:
- Timeout: 5 seconds
- Memory: 50MB
- No file system (except /tmp)
- No network access
- Standard library only
- Returns: {stdout, stderr, success, error_type}
"""
import io
import logging
import multiprocessing
import os
import resource
import signal
import sys
import tempfile
import time
import traceback
from typing import Any

logger = logging.getLogger("sandbox")

# Blocked modules that students should not access
BLOCKED_MODULES = frozenset({
    "subprocess", "os.system", "shutil", "socket", "http",
    "urllib", "requests", "ftplib", "smtplib", "telnetlib",
    "xmlrpc", "ctypes", "importlib", "code", "codeop",
    "compile", "compileall", "py_compile", "zipimport",
    "pkgutil", "ensurepip", "pip", "venv", "webbrowser",
    "antigravity", "turtle", "tkinter", "multiprocessing",
    "threading", "signal", "pathlib",
})

BLOCKED_BUILTINS = frozenset({
    "exec", "eval", "compile", "__import__", "open",
    "breakpoint", "exit", "quit",
})


def _create_safe_builtins() -> dict:
    """Create a restricted builtins dict."""
    import builtins
    safe = {}
    for name in dir(builtins):
        if name.startswith("_") and name != "__name__":
            continue
        if name.lower() in BLOCKED_BUILTINS:
            continue
        safe[name] = getattr(builtins, name)

    # Allow open only for /tmp
    original_open = builtins.open

    def safe_open(file, mode="r", *args, **kwargs):
        filepath = str(file)
        if not filepath.startswith("/tmp") and not filepath.startswith(tempfile.gettempdir()):
            raise PermissionError(f"File access denied: only /tmp is allowed")
        if "w" in mode or "a" in mode:
            # Limit file size
            pass
        return original_open(file, mode, *args, **kwargs)

    safe["open"] = safe_open
    safe["__name__"] = "__main__"
    safe["__builtins__"] = safe
    return safe


def _execute_code(code: str, result_queue: multiprocessing.Queue, timeout: int, memory_mb: int):
    """Execute code in a restricted subprocess."""
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    start_time = time.time()

    try:
        # Set resource limits (Unix only)
        if hasattr(resource, "setrlimit"):
            # Memory limit
            mem_bytes = memory_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
            # CPU time limit
            resource.setrlimit(resource.RLIMIT_CPU, (timeout + 1, timeout + 2))
            # No new processes
            resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))

        # Set alarm for timeout
        def timeout_handler(signum, frame):
            raise TimeoutError("Code execution timed out")

        if hasattr(signal, "SIGALRM"):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)

        # Redirect stdout/stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture

        try:
            # Create safe globals
            safe_globals = _create_safe_builtins()
            safe_globals["__builtins__"] = safe_globals

            # Block dangerous imports
            original_import = __builtins__.__import__ if hasattr(__builtins__, "__import__") else __import__

            def safe_import(name, *args, **kwargs):
                if name in BLOCKED_MODULES or any(name.startswith(m + ".") for m in BLOCKED_MODULES):
                    raise ImportError(f"Module '{name}' is not allowed in the sandbox")
                return original_import(name, *args, **kwargs)

            safe_globals["__import__"] = safe_import

            # Compile and execute
            compiled = compile(code, "<student_code>", "exec")
            exec(compiled, safe_globals)

            execution_time = int((time.time() - start_time) * 1000)

            result_queue.put({
                "stdout": stdout_capture.getvalue(),
                "stderr": stderr_capture.getvalue(),
                "success": True,
                "error_type": None,
                "execution_time_ms": execution_time,
            })

        except SyntaxError as e:
            result_queue.put({
                "stdout": stdout_capture.getvalue(),
                "stderr": f"SyntaxError: {e.msg} (line {e.lineno})",
                "success": False,
                "error_type": "syntax",
                "execution_time_ms": int((time.time() - start_time) * 1000),
            })
        except TimeoutError:
            result_queue.put({
                "stdout": stdout_capture.getvalue(),
                "stderr": f"TimeoutError: Code exceeded {timeout} second time limit",
                "success": False,
                "error_type": "timeout",
                "execution_time_ms": timeout * 1000,
            })
        except MemoryError:
            result_queue.put({
                "stdout": stdout_capture.getvalue(),
                "stderr": f"MemoryError: Code exceeded {memory_mb}MB memory limit",
                "success": False,
                "error_type": "memory",
                "execution_time_ms": int((time.time() - start_time) * 1000),
            })
        except Exception as e:
            error_tb = traceback.format_exc()
            error_type = "runtime"
            result_queue.put({
                "stdout": stdout_capture.getvalue(),
                "stderr": error_tb,
                "success": False,
                "error_type": error_type,
                "execution_time_ms": int((time.time() - start_time) * 1000),
            })
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            if hasattr(signal, "SIGALRM"):
                signal.alarm(0)

    except Exception as e:
        result_queue.put({
            "stdout": "",
            "stderr": str(e),
            "success": False,
            "error_type": "runtime",
            "execution_time_ms": int((time.time() - start_time) * 1000),
        })


def execute_sandboxed(code: str, timeout: int = 5, memory_mb: int = 50) -> dict[str, Any]:
    """Execute Python code in a sandboxed subprocess.

    Args:
        code: Python source code to execute
        timeout: Maximum execution time in seconds (default 5)
        memory_mb: Maximum memory in MB (default 50)

    Returns:
        Dict with stdout, stderr, success, error_type, execution_time_ms
    """
    result_queue = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=_execute_code,
        args=(code, result_queue, timeout, memory_mb),
    )
    process.start()
    process.join(timeout=timeout + 2)  # Extra buffer for process startup

    if process.is_alive():
        process.kill()
        process.join(timeout=2)
        return {
            "stdout": "",
            "stderr": f"TimeoutError: Code exceeded {timeout} second time limit",
            "success": False,
            "error_type": "timeout",
            "execution_time_ms": timeout * 1000,
        }

    if not result_queue.empty():
        return result_queue.get()

    return {
        "stdout": "",
        "stderr": "Execution failed: no result returned",
        "success": False,
        "error_type": "runtime",
        "execution_time_ms": 0,
    }
