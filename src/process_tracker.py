class ProcessTracker:
    def __init__(self):
        self.process_sessions = {}
        self.tracking = False

    def start_tracking(self):
        self.tracking = True
        # Logic to start monitoring processes goes here

    def stop_tracking(self):
        self.tracking = False
        # Logic to stop monitoring processes goes here

    def _on_process_start(self, process_name):
        # Logic to handle process start event
        pass

    def _on_process_end(self, process_name):
        # Logic to handle process end event
        pass

    def get_sessions(self):
        return self.process_sessions