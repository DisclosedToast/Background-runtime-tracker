class RuntimeSummary:
    def __init__(self):
        self.sessions = {}

    def add_session(self, process_name, start_time, end_time):
        if process_name not in self.sessions:
            self.sessions[process_name] = []
        self.sessions[process_name].append((start_time, end_time))

    def generate_summary(self):
        summary = {}
        for process_name, session_list in self.sessions.items():
            total_runtime = sum((end - start).total_seconds() for start, end in session_list)
            summary[process_name] = total_runtime / 3600  # Convert seconds to hours
        return summary