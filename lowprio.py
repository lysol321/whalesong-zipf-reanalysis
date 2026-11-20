"""Set this process to Windows IDLE priority (properly typed ctypes; the untyped call silently failed)."""
import ctypes
from ctypes import wintypes

IDLE_PRIORITY_CLASS = 0x00000040


def set_idle():
    try:
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.GetCurrentProcess.restype = wintypes.HANDLE
        k32.SetPriorityClass.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        k32.SetPriorityClass.restype = wintypes.BOOL
        k32.GetPriorityClass.argtypes = [wintypes.HANDLE]
        k32.GetPriorityClass.restype = wintypes.DWORD
        h = k32.GetCurrentProcess()
        k32.SetPriorityClass(h, IDLE_PRIORITY_CLASS)
        return k32.GetPriorityClass(h)
    except Exception:
        return None


if __name__ == "__main__":
    print("priority class: 0x%x" % set_idle())
