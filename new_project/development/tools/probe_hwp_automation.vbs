' Minimal 32-bit COM activation probe. Never opens, edits, saves, or quits a document.
On Error Resume Next
WScript.Echo "before_create"
Set hwp = CreateObject("HWPFrame.HwpObject")
If Err.Number <> 0 Then
    WScript.Echo "create_error=" & Hex(Err.Number) & " " & Err.Description
    WScript.Quit 1
End If
WScript.Echo "created"
WScript.Echo "version=" & hwp.Version
If Err.Number <> 0 Then WScript.Echo "version_error=" & Hex(Err.Number)
Set hwp = Nothing
