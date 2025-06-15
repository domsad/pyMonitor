import psutil, cpuinfo, platform, time, socket, GPUtil, subprocess


class Monitor:

    def cpu_stat(self):
        # Pobiera z biblioteki cpuinfo informacje o cpu
        cpu_stats = cpuinfo.get_cpu_info()
        
        return {
            "model": cpu_stats.get("brand_raw"),
            "architektura": cpu_stats.get("arch"),
            "bity": cpu_stats.get("bits"),
            "częstotliwość (Hz)": cpu_stats.get("hz_actual_friendly"),
            "rdzenie": psutil.cpu_count(logical=False),
            "wątki": psutil.cpu_count(logical=True),
            "użycie CPU (%)": psutil.cpu_percent(interval=1),
            "5 najczęstszych instrukcji": cpu_stats.get("flags")[:5]
        }
    
    def gpu_stat(self):
        gpu_stats = GPUtil.getGPUs()
        
        gpu_info = []

        for gpu in gpu_stats:
            gpu_name = gpu.name.upper().strip()
            
            if "NVIDIA" in gpu_name:
                gpu_type = "NVIDIA"
            elif "AMD" in gpu_type:
                gpu_type = "AMD"
            else:
                gpu_type = "Inny"

            gpu_info.append({
                "typ": gpu_type,
                "nazwa": gpu.name,
                "temperatura (°C)": gpu.temperature,
                "obciążenie (%)": round(gpu.load * 100, 2),
                "pamięć wykorzystywana (MB)": gpu.memoryUsed,
                "pamięć całkowita (MB)": gpu.memoryTotal,
            })
        return gpu_info

    def ram_stat(self):
        ram_stats = psutil.virtual_memory()

        return {
            "całkowita pamięć (GB)": ram_stats.total // (1024**3),
            "używana pamięć (GB)": ram_stats.used // (1024**3),
            "wolna pamięć (GB)": ram_stats.available // (1024**3),
            "procent użycia (%)": ram_stats.percent
        }
    
    def disk_stat(self):
        partitions_info = []

        partitionsList = psutil.disk_partitions()

        for partition in partitionsList:
            try:
                usage = psutil.disk_usage(partition.mountpoint)

                partitions_info.append({
                    "urządzenie": partition.device,
                    "punkt montowania": partition.mountpoint,
                    "system plików": partition.fstype,
                    "pojemność (GB)": usage.total // (1024**3),
                    "użyte miejsce (GB)": usage.used // (1024**3),
                    "wolne miejsce (GB)": usage.free // (1024**3),
                    "procent użycia (%)": usage.percent
                })
            except Exception as error:
            # Pomijamy partycje, do których nie mamy dostępu
                with open('error.log', 'w') as log:
                    log.write('Błąd przy odczytywaniu partycji:', error)
                continue

        return partitions_info

    def network_stat(self):
        net_io = psutil.net_io_counters()
        addrs = psutil.net_if_addrs()

        networkInterfaces = {}

        for interface in addrs:
            ip_list = []

            for addr in addrs[interface]:
                ip_list.append(addr.address) 

            networkInterfaces[interface] = ip_list

        return {
            "wysłane bajty": net_io.bytes_sent,
            "odebrane bajty": net_io.bytes_recv,
            "karty sieciowe": networkInterfaces       
        }

    def system_stat(self):
        uptime = time.time() - psutil.boot_time()
        hours, rem = divmod(uptime, 3600)
        mins, sec = divmod(rem, 60)

        return {
            "system": platform.system(),
            "nazwa hosta": platform.node(),
            "wydanie": platform.release(),
            "sekundy od system boot": round(uptime,2),
            "czas działania systemu": f"{int(hours)}h {int(mins)}m {int(sec)}s"
        }

    def get_all(self):
        return {
            "cpu": self.cpu_stat(),
            "gpu": self.gpu_stat(),
            "ram": self.ram_stat(),
            "dysk": self.disk_stat(),
            "sieć": self.network_stat(),
            "system": self.system_stat(),
        }
