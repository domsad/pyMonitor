import psutil, cpuinfo, platform, time, socket, GPUtil
if platform.system() == "Windows":
    import subprocess
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
            "model": cpu_stats.get("brand_raw"),
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
    def gpu_stat(self):
        system = platform.system()
        gpus = GPUtil.getGPUs()
        
        if not gpus:
            # brak GPU wykrytego przez GPUtil - spróbuj wykryć AMD na Windowsie inaczej
            if system == "Windows":
                try:
                    output = subprocess.check_output(
                        ["wmic", "path", "win32_VideoController", "get", "Name"],
                        encoding="utf-8"
                    )
                    lines = [line.strip() for line in output.split("\n") if line.strip()]
                    amd_gpus = [line for line in lines[1:] if "AMD" in line.upper() or "RADEON" in line.upper()]
                    if amd_gpus:
                        return {
                            "typ": "AMD",
                            "karty": amd_gpus,
                            "info": "Brak szczegółowych danych (temperatura, obciążenie) bez dodatkowych narzędzi"
                        }
                    else:
                        return {"info": "Nie wykryto GPU NVIDIA ani AMD"}
                except Exception as e:
                    return {"error": f"Błąd wykrywania GPU AMD: {e}"}
            else:
                return {"info": "Brak wykrywalnych GPU lub brak wsparcia dla tego systemu"}
        
        # jeśli są GPU wykryte przez GPUtil
        gpu_infos = []
        for gpu in gpus:
            vendor = gpu.name.upper()
            # prosta heurystyka po nazwie:
            if "NVIDIA" in vendor or "GEFORCE" in vendor:
                typ = "NVIDIA"
            elif "AMD" in vendor or "RADEON" in vendor:
                typ = "AMD"
            else:
                typ = "Inny"

            gpu_infos.append({
                "typ": typ,
                "nazwa": gpu.name,
                "temperatura (°C)": gpu.temperature,
                "obciążenie (%)": gpu.load * 100,
                "pamięć wykorzystywana (MB)": gpu.memoryUsed,
                "pamięć całkowita (MB)": gpu.memoryTotal,
                "UUID": gpu.uuid,
            })

        return gpu_infos

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
        total_capacity = 0
        total_used = 0
        total_free = 0
        partitions_info = []
        for p in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(p.mountpoint)
                partitions_info.append({
                    "urządzenie": p.device,
                    "punkt montowania": p.mountpoint,
                    "system plików": p.fstype,
                    "pojemność (GB)": usage.total // (1024**3),
                    "użyte miejsce (GB)": usage.used // (1024**3),
                    "wolne miejsce (GB)": usage.free // (1024**3),
                    "procent użycia (%)": usage.percent
                })
                total_capacity += usage.total
                total_used += usage.used
                total_free += usage.free
            except PermissionError:
                # Niektóre partycje mogą być niedostępne do odczytu np. CD-ROMy
                partitions_info.append({
                    "urządzenie": p.device,
                    "punkt montowania": p.mountpoint,
                    "system plików": p.fstype,
                    "info": "brak dostępu"
                })
        total_capacity_gb = total_capacity / (1024**3)
        total_used_gb = total_used / (1024**3)
        total_free_gb = total_free / (1024**3)

        # Obliczamy procent użycia całkowitego dysku (z sumy)
        total_used_percent = (total_used / total_capacity) * 100 if total_capacity else 0
        total_free_percent = (total_free / total_capacity) * 100 if total_capacity else 0

        partitions_info.append({
            "----- Podsumowanie -----": "",
            "łączna pojemność (GB)": round(total_capacity_gb, 2),
            "łączne zajęte miejsce (GB)": round(total_used_gb, 2),
            "łączne wolne miejsce (GB)": round(total_free_gb, 2),
            "łączne zajęte miejsce (%)": round(total_used_percent, 2),
            "łączne wolne miejsce (%)": round(total_free_percent, 2)
        })

        return partitions_info
    def network_stat(self):
        net_io = psutil.net_io_counters()
        addrs = psutil.net_if_addrs()
        return {
            "bytes_wysłane": net_io.bytes_sent,
            "bytes_odebrane": net_io.bytes_recv,
            "adresy_IP": {iface: [addr.address for addr in addrs[iface] if addr.family == socket.AF_INET] for iface in addrs}
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
            "gpu": self.gpu_stat(),
            "ram": self.ram_stat(),
            "dysk": self.disk_stat(),
            "sieć": self.network_stat(),
            "system": self.system_stat(),
            "czas działania systemu": self.uptime()
        }
