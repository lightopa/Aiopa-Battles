DEL /S /Q build
"C:\Python34\python.exe" setupExe.py build
cd "build"
rmdir /S /Q "Aiopa Battles"
rmdir /S /Q "Aiopa Battles"
rename "exe.win-amd64-3.4" "Aiopa Battles"
"C:\Program Files\7-Zip\7z.exe" a -r -tzip "Aiopa-Battles-vX.X.X-alpha.zip" "Aiopa Battles/*.*"
pause