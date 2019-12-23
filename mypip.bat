echo off

call D:\DEV\python3\python --version

call D:\DEV\python3\Scripts\pip --version
call D:\DEV\python3\python -m pip install --upgrade pip
call D:\DEV\python3\Scripts\pip --version

rem set arg1=%1
rem call D:\DEV\python3\python -m pip install %arg1% -U
rem call C:\DEV\python362\Scripts\pip install %arg1% -U

rem call D:\DEV\python3\Scripts\pip install %arg1%

call D:\DEV\python3\Scripts\pip install --upgrade setuptools
call D:\DEV\python3\Scripts\pip install --upgrade requests
call D:\DEV\python3\Scripts\pip install --upgrade simpleJson
call D:\DEV\python3\Scripts\pip install --upgrade pytz
call D:\DEV\python3\Scripts\pip install --upgrade pyparsing
call D:\DEV\python3\Scripts\pip install --upgrade cmd2
call D:\DEV\python3\python -m pip install --upgrade PyMySQL
call D:\DEV\python3\Scripts\pip install pymongo
call D:\DEV\python3\Scripts\pip install --upgrade pylint
call D:\DEV\python3\Scripts\pip install --upgrade click

call D:\DEV\python3\Scripts\pip install --upgrade BeautifulSoup4
call D:\DEV\python3\Scripts\pip install --upgrade pandas
call D:\DEV\python3\Scripts\pip install --upgrade xlsxwriter

call D:\DEV\python3\Scripts\pip install --upgrade flask
call D:\DEV\python3\Scripts\pip install --upgrade Flask-RESTful
call D:\DEV\python3\Scripts\pip install --upgrade Flask-Cors
call D:\DEV\python3\Scripts\pip install --upgrade urllib3


call D:\DEV\python3\Scripts\pip list 

