class ProcessSession:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.duration = self.calculate_duration()

    def calculate_duration(self):
        return (self.end_time - self.start_time).total_seconds() / 3600  # Convert seconds to hours

    def __repr__(self):
        return f"ProcessSession(start_time={self.start_time}, end_time={self.end_time}, duration={self.duration:.2f} hours)"