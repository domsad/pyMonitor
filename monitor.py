import psutil, cpuinfo, platform, time

class Monitor:
    # Można popatrzeć co oferują jeszcze ciekawego te biblioteki i dodać
    # Albo dodać jakąś inną bibliotekę
    # Doku cpuinfo - https://github.com/workhorsy/py-cpuinfo
    # Potężna dokumentacja psutil - https://psutil.readthedocs.io/en/latest/#

    def cpu_stat(self):
        # Pobiera z biblioteki cpuinfo informacje o cpu
        # Doku - https://github.com/workhorsy/py-cpuinfo
        cpu_stats = cpuinfo.get_cpu_info()
        return {
            "model": cpu_stats.get("bits"),
            "architektura": cpu_stats.get("arch"),
            "bity": cpu_stats.get("bits"),
            "częstotliwość (Hz)": cpu_stats.get("hz_actual_friendly"),
            "rdzenie": psutil.cpu_count(logical=False),
            "wątki": psutil.cpu_count(logical=True),
            "użycie CPU (%)": psutil.cpu_percent(interval=1), # w procentach
            "użycie CPU dla wątków (%)": psutil.cpu_percent(percpu=True, interval=1),
            # nwm czy użyteczne ale można coś powiedzieć ogólnie o instrukcjach procesora przy prezentowaniu projektu
            "10 najczęstszych instrukcji": cpu_stats.get("flags", [])[:10]
        }
    def ram_stat(self):
        ram = psutil.virtual_memory()
        return {
            # można to zaokrąglić z round()
            "całkowita pamięć (GB)": ram.total // (1024**3),
            "używana pamięć (GB)": ram.used // (1024**3),
            "wolna pamięć (GB)": ram.available // (1024**3),
            "procent użycia (%)": ram.percent
        }
    def disk_stat(self):
        disk = psutil.disk_usage('/')
        return {
            "pojemność dysku (GB)": disk.total // (1024**3),
            "użyte miejsce (GB)": disk.used // (1024**3),
            "wolne miejsce (GB)": disk.free // (1024**3),
            "procent użycia (%)": disk.percent
        }
    def system_stat(self):
        return {
            "system": platform.system(),
            "nazwa hosta": platform.node(),
            "wydanie": platform.release(),
        }
    def uptime(self):
        uptime = time.time() - psutil.boot_time()
        hours, rem = divmod(uptime, 3600)
        mins, sec = divmod(rem, 60)
        return {
            "sekundy od system boot": round(uptime,2),
            "czas działania systemu sformatowany": f"{int(hours)}h {int(mins)}m {int(sec)}s"
        }
    def get_all(self):
        return {
            "cpu": self.cpu_stat(),
            "ram": self.ram_stat(),
            "dysk": self.disk_stat(),
            "system": self.system_stat(),
            "czas działania systemu": self.uptime()
        }
