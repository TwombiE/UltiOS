import time
from process_manager import ProcessManager

def main():
    manager = ProcessManager()
    print("UltiOS - Automatische Prozessverwaltung gestartet.")

    try:
        while True:
            print("Suche nach unnötigen Prozessen...")
            manager.auto_terminate_unnecessary_processes()
            print("Warte 60 Sekunden vor der nächsten Prüfung...")
            time.sleep(60)  # Überprüfung alle 60 Sekunden
    except KeyboardInterrupt:
        print("UltiOS wurde beendet.")

if __name__ == "__main__":
    main()
