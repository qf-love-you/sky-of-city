@echo off

@ rem if "%1" == "h" goto begin
@ rem mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin

python main.py
pause