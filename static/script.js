// Odświeżanie danych co sekunde
setInterval(fetchStats, 1000);
window.onload = fetchStats;

// Pobiera dane z API i aktualizuje interfejs
function fetchStats() {
    fetch("/api/stats")
        .then(res => res.json())
        .then(data => {
            // CPU
            document.getElementById("cpu").innerText = formatObject(data.cpu);

            // GPU
            document.getElementById("gpu").innerText = formatObject(data.gpu);

            // RAM
            document.getElementById("ram").innerText = formatObject(data.ram);

            // Dysk
            document.getElementById("dysk").innerText = formatObject(data.dysk);

            // Sieć
            document.getElementById("network").innerText = formatObject(data.sieć);

            // System
            document.getElementById("system").innerText = formatObject(data.system);
        });
}

// Formatowanie danych do czytelnego tekstu
function formatObject(obj) {
    if (!obj) return "Brak danych";

    if (Array.isArray(obj)) {
        return obj.map((item, i) => `#${i+1}\n${formatObject(item)}`).join("\n\n");
    }

    return Object.entries(obj)
        .map(([key, value]) => {
            if (Array.isArray(value)) return `${key}: ${value.join(", ")}`;
            else if (typeof value === "object") return `${key}:\n${formatObject(value).replace(/^/gm, "  ")}`;
            else return `${key}: ${value}`;
        })
        .join("\n");
}
