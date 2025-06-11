# pyMonitor

Po pobraniu projektu wykonaj:

Na windows:

python -m venv .venv
.\.venv\Scripts\activate

pip install psutil py-cpuinfo flask

Linux:
python3 -m venv .venv
source .venv/bin/activate

pip install psutil py-cpuinfo flask

Tutaj masz api - wszystkie staty
http://127.0.0.1:5000/api/stats

http://127.0.0.1:5000/api/cpu
http://127.0.0.1:5000/api/ram
http://127.0.0.1:5000/api/disk
http://127.0.0.1:5000/api/system
