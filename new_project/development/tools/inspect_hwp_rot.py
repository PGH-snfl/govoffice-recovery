from __future__ import annotations

import pythoncom
import win32com.client


def safe(call):
    try:
        return call()
    except Exception as exc:
        return f"ERROR:{type(exc).__name__}:{exc}"


context = pythoncom.CreateBindCtx(0)
running = pythoncom.GetRunningObjectTable()
for moniker in running.EnumRunning():
    name = safe(lambda: moniker.GetDisplayName(context, None))
    if not isinstance(name, str) or not name.startswith("!HwpObject"):
        continue
    raw = running.GetObject(moniker)
    hwp = win32com.client.Dispatch(raw.QueryInterface(pythoncom.IID_IDispatch))
    print(
        {
            "moniker": name,
            "path": safe(lambda: hwp.Path),
            "windows": safe(lambda: hwp.XHwpWindows.Count),
            "documents": safe(lambda: hwp.XHwpDocuments.Count),
            "visible": safe(lambda: hwp.XHwpWindows.Item(0).Visible),
        },
        flush=True,
    )
