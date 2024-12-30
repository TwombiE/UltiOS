import tkinter as tk
from tkinter import ttk, messagebox
from process_manager import ProcessManager

class UltiOSUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("UltiOS - Prozessmanager")
        self.root.geometry("700x500")
        self.manager = ProcessManager()
        self.check_vars = []  # Liste für Checkbox-Variablen
        self.processes = []  # Liste der gefundenen Prozesse

        # UI-Elemente erstellen
        self.setup_ui()

    def setup_ui(self):
        # Label
        tk.Label(self.root, text="Laufende Prozesse", font=("Arial", 14)).pack(pady=10)

        # Scrollable Frame für Prozesse
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Prozesse laden", command=self.load_processes).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Ausgewählte Prozesse beenden", command=self.terminate_selected_processes).pack(side=tk.LEFT, padx=5)

    def load_processes(self):
        """Lädt Prozesse in die Checkliste."""
        # Alte Daten löschen
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.check_vars.clear()
        self.processes = self.manager.get_unnecessary_processes()

        # Prozesse hinzufügen
        for process in self.processes:
            var = tk.BooleanVar(value=True)  # Checkbox standardmäßig aktiviert
            self.check_vars.append(var)
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill="x", padx=5, pady=2)

            # Checkbox und Prozessdetails
            chk = tk.Checkbutton(frame, variable=var)
            chk.pack(side="left")
            lbl = ttk.Label(frame, text=f"{process['name']} (PID: {process['pid']}, Speicher: {process['memory']} MB)")
            lbl.pack(side="left", padx=5)

    def terminate_selected_processes(self):
        """Beendet die ausgewählten Prozesse."""
        selected_processes = [
            process for process, var in zip(self.processes, self.check_vars) if var.get()
        ]

        if not selected_processes:
            messagebox.showinfo("Keine Auswahl", "Es wurden keine Prozesse zum Beenden ausgewählt.")
            return

        for process in selected_processes:
            try:
                self.manager.terminate_process(process["pid"])
                messagebox.showinfo(
                    "Erfolg", f"Prozess {process['name']} (PID: {process['pid']}) wurde beendet."
                )
            except Exception as e:
                messagebox.showerror(
                    "Fehler", f"Prozess {process['name']} (PID: {process['pid']}) konnte nicht beendet werden: {e}"
                )

        self.load_processes()  # Aktualisiere die Liste nach dem Beenden

    def run(self):
        """Startet die Tkinter-Hauptschleife."""
        self.root.mainloop()

if __name__ == "__main__":
    ui = UltiOSUI()
    ui.run()
