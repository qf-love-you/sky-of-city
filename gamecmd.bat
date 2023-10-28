@echo off

echo game commands:
echo\
echo exit: exit the process
echo\

:loop

set /p command=input game command:

if "%command%" == "exit" (
    exit
)

if "%command%" == "debug" (

)
goto loop
