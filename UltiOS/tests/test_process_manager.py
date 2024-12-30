import unittest
from src.process_manager import ProcessManager

class TestProcessManager(unittest.TestCase):
    def test_get_unnecessary_processes(self):
        manager = ProcessManager()
        processes = manager.get_unnecessary_processes()
        self.assertIsInstance(processes, list)

    def test_terminate_process(self):
        # Hier kann ein Mock-Prozess verwendet werden
        pass

if __name__ == "__main__":
    unittest.main()
