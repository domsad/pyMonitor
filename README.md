#  pyMonitor – systemowy monitor zasobów

**pyMonitor** to lekka aplikacja napisana w Pythonie, która umożliwia monitorowanie podstawowych zasobów systemu operacyjnego takich jak CPU, RAM, dysk, GPU, sieć oraz czas działania systemu. Dane prezentowane są zarówno w interfejsie webowym, jak i udostępniane przez REST API.

---

##  Instalacja
Po sklonowaniu repozytorium lub pobraniu programu należy włączyć konsole poleceń i wykonać nastepujące komendy:

###  Dla Windows:
```bash
python3 -m venv .venv
.venv\Scripts\activate
pip install psutil py-cpuinfo flask gputil
```

###  Dla Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install psutil py-cpuinfo flask gputil
```

---

##  Uruchomienie
Po zainstalowaniu wymaganych bibliotek uruchom program poleceniem:

```bash
python3 main.py
```

Aplikacja będzie dostępna pod adresem:
```
http://127.0.0.1:5000/
```

---

##  Endpointy API

| Endpoint | Opis |
|---------|------|
| `/api/stats` | Wszystkie statystyki razem |
| `/api/stats/cpu` | Statystyki CPU |
| `/api/stats/ram` | Statystyki pamięci RAM |
| `/api/stats/disk` | Statystyki dysku |
| `/api/stats/gpu` | Statystyki GPU |
| `/api/stats/system` | Informacje o systemie |
| `/api/stats/network` | Statystyki sieciowe |

---

##  Interfejs webowy

Po wejściu na stronę główną (`/`) aplikacja wyświetli dane systemowe w czytelnej formie, które automatycznie odświeżają się co kilka sekund.

---

##  Autorzy
Dominik Sadowski, Kacper Kaczmarek, Maciej Kotas
