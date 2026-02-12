@echo off
echo Pushing project to GitHub...
git push -u origin main
if %errorlevel% neq 0 (
    echo.
    echo Something went wrong! You might need to authenticate.
    echo Please make sure you are logged in to GitHub.
    pause
) else (
    echo.
    echo Success! Project pushed to GitHub.
    pause
)
