import psutil

class ProcessManager:
    def __init__(self):
        self.excluded_processes = ["explorer.exe", "svchost.exe", "System Idle Process"]

    def get_unnecessary_processes(self):
        """Findet Prozesse, die unnötig sind (z. B. hoher Speicherverbrauch, niedrige CPU-Auslastung)."""
        unnecessary_processes = []
        for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info', 'cpu_percent']):
            try:
                # Prozessinformationen abrufen
                name = proc.info['name']
                pid = proc.info['pid']
                memory = proc.info['memory_info'].rss / (1024 * 1024)  # In MB
                cpu = proc.info['cpu_percent']

                # Kriterien für unnötige Prozesse
                if name not in self.excluded_processes and memory > 100 and cpu < 1:
                    unnecessary_processes.append({
                        "pid": pid,
                        "name": name,
                        "memory": round(memory, 2),
                        "cpu": cpu,
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return unnecessary_processes

    def terminate_process(self, pid):
        """Beendet einen Prozess anhand der PID."""
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait()  # Warte, bis der Prozess beendet ist
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            raise RuntimeError(f"Fehler beim Beenden des Prozesses: {e}")

    def auto_terminate_unnecessary_processes(self):
        """Beendet alle unnötigen Prozesse automatisch."""
        processes = self.get_unnecessary_processes()
        for proc in processes:
            try:
                self.terminate_process(proc["pid"])
                print(f"Beendet: {proc['name']} (PID: {proc['pid']}, Speicher: {proc['memory']} MB)")
            except RuntimeError as e:
                print(f"Fehler beim Beenden von {proc['name']} (PID: {proc['pid']}): {e}")
