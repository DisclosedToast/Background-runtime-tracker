import unittest
from src.process_tracker import ProcessTracker
from src.models.process_session import ProcessSession

class TestProcessTracker(unittest.TestCase):

    def setUp(self):
        self.tracker = ProcessTracker()

    def test_start_tracking(self):
        self.tracker.start_tracking('notepad.exe')
        self.assertIn('notepad.exe', self.tracker.active_processes)

    def test_stop_tracking(self):
        self.tracker.start_tracking('notepad.exe')
        self.tracker.stop_tracking('notepad.exe')
        self.assertNotIn('notepad.exe', self.tracker.active_processes)

    def test_process_session_creation(self):
        self.tracker.start_tracking('notepad.exe')
        session = self.tracker.create_session('notepad.exe')
        self.assertIsInstance(session, ProcessSession)
        self.assertEqual(session.start_time, self.tracker.start_time['notepad.exe'])

    def test_runtime_calculation(self):
        self.tracker.start_tracking('notepad.exe')
        # Simulate some time passing
        import time
        time.sleep(1)
        self.tracker.stop_tracking('notepad.exe')
        session = self.tracker.get_session('notepad.exe')
        self.assertGreater(session.duration, 0)

if __name__ == '__main__':
    unittest.main()