# pyMonitor

### TODO:
- kod w index.html wypada rozdzielić na css js i html
- można zrobić dla requestów api tzw Swagger UI (https://swagger.io/tools/swagger-ui/) chodzi o krótką dokumentację dla api requestów
- prezentacja i readme // ewentualnie po prostu można spróbować zaprezentować w readme program jak w innych projektach na githubie
- poszukać jakiś bugów ale chyba i tak będziemy prezentować na czyimś lapku więc tylko na nim może działać xd
- można rozbudować ten projekt jak jakiś pomysł masz


### Zmienić vvv sformatować

Po pobraniu projektu wykonaj:

Na windows:

python -m venv .venv
.\.venv\Scripts\activate

pip install psutil py-cpuinfo flask gputil

Linux:
python3 -m venv .venv
source .venv/bin/activate

pip install psutil py-cpuinfo flask gputil


Wszystkie statystyki razem:
http://127.0.0.1:5000/api/stats

CPU:
http://127.0.0.1:5000/api/cpu

RAM:
http://127.0.0.1:5000/api/ram

Dysk:
http://127.0.0.1:5000/api/disk

System:
http://127.0.0.1:5000/api/system

Sieć:
http://127.0.0.1:5000/api/network

GPU:
http://127.0.0.1:5000/api/gpu
