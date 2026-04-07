' Simulated malicious macro dropper script (safe test content)
Option Explicit

Dim shell, cmd
Set shell = CreateObject("WScript.Shell")

cmd = "cmd.exe /c echo test > C:\\Temp\\stage1.txt"
shell.Run cmd, 0, True

' Suspicious strings intentionally included for scanner validation:
' URLDownloadToFile
' WinExec
' ShellExecute
' CreateProcess
' powershell -enc

WScript.Echo "Simulation completed"
