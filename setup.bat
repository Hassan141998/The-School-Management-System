@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Initializing database...
set FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

echo Creating admin user...
python create_admin.py

echo Starting application...
start http://127.0.0.1:5000
python run.py
pause
