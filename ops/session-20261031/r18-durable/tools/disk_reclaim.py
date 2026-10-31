"""Measure and optionally reclaim regenerable caches/dumps on a full disk.

Nothing governed is touched: only OS/app cache and crash-dump directories, plus
package-manager caches. The deletion list is printed before and after so the round
report can disclose exactly what was removed.
"""
import os
import shutil
import sys

LA = os.environ.get("LOCALAPPDATA", r"C:\Users\user\AppData\Local")
CANDIDATES = [
    os.path.join(LA, "CrashDumps"),
    os.path.join(LA, "D3DSCache"),
    os.path.join(LA, "calibre-cache"),
    os.path.join(LA, "Temp"),
    os.path.join(LA, "npm-cache"),
]


def size(p):
    total = 0
    count = 0
    for root, dirs, files in os.walk(p, onerror=lambda e: None):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
                count += 1
            except OSError:
                pass
    return total, count


def free():
    import ctypes
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
        ctypes.c_wchar_p("C:\\"), None, None, ctypes.byref(free_bytes))
    return free_bytes.value


mode = sys.argv[1] if len(sys.argv) > 1 else "measure"
print("free_before=%.1f MB" % (free() / 1e6))
for p in CANDIDATES:
    if not os.path.isdir(p):
        print("ABSENT   %s" % p)
        continue
    b, n = size(p)
    print("%-8s %9.1f MB %6d files  %s" % ("PRESENT", b / 1e6, n, p))

if mode == "reclaim":
    for p in CANDIDATES:
        if not os.path.isdir(p):
            continue
        removed = 0
        errors = 0
        for entry in os.listdir(p):
            full = os.path.join(p, entry)
            try:
                if os.path.isdir(full) and not os.path.islink(full):
                    shutil.rmtree(full, ignore_errors=True)
                else:
                    os.remove(full)
                removed += 1
            except OSError:
                errors += 1
        print("RECLAIM  %-50s removed=%d errors=%d" % (p, removed, errors))
    print("free_after=%.1f MB" % (free() / 1e6))
