import unittest
from src.runtime_summary import RuntimeSummary
from src.models.process_session import ProcessSession

class TestRuntimeSummary(unittest.TestCase):

    def setUp(self):
        self.runtime_summary = RuntimeSummary()

    def test_generate_summary_no_sessions(self):
        summary = self.runtime_summary.generate_summary()
        self.assertEqual(summary, {})

    def test_generate_summary_single_session(self):
        session = ProcessSession(start_time="2023-10-01 10:00:00", end_time="2023-10-01 12:00:00")
        self.runtime_summary.add_session("TestApp", session)
        summary = self.runtime_summary.generate_summary()
        self.assertEqual(summary["TestApp"], 2.0)

    def test_generate_summary_multiple_sessions(self):
        session1 = ProcessSession(start_time="2023-10-01 10:00:00", end_time="2023-10-01 12:00:00")
        session2 = ProcessSession(start_time="2023-10-01 13:00:00", end_time="2023-10-01 15:30:00")
        self.runtime_summary.add_session("TestApp", session1)
        self.runtime_summary.add_session("TestApp", session2)
        summary = self.runtime_summary.generate_summary()
        self.assertEqual(summary["TestApp"], 4.5)

    def test_generate_summary_with_different_apps(self):
        session1 = ProcessSession(start_time="2023-10-01 10:00:00", end_time="2023-10-01 12:00:00")
        session2 = ProcessSession(start_time="2023-10-01 13:00:00", end_time="2023-10-01 15:30:00")
        session3 = ProcessSession(start_time="2023-10-01 09:00:00", end_time="2023-10-01 11:00:00")
        self.runtime_summary.add_session("TestApp1", session1)
        self.runtime_summary.add_session("TestApp2", session2)
        self.runtime_summary.add_session("TestApp1", session3)
        summary = self.runtime_summary.generate_summary()
        self.assertEqual(summary["TestApp1"], 3.0)
        self.assertEqual(summary["TestApp2"], 2.5)

if __name__ == '__main__':
    unittest.main()