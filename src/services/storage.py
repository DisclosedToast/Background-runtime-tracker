class StorageService:
    def __init__(self, storage_file='sessions.json'):
        self.storage_file = storage_file

    def save_session(self, session_data):
        import json
        try:
            with open(self.storage_file, 'a') as file:
                json.dump(session_data, file)
                file.write('\n')
        except Exception as e:
            print(f"Error saving session data: {e}")

    def load_sessions(self):
        import json
        sessions = []
        try:
            with open(self.storage_file, 'r') as file:
                for line in file:
                    sessions.append(json.loads(line))
        except FileNotFoundError:
            print("Storage file not found. Returning empty session list.")
        except Exception as e:
            print(f"Error loading session data: {e}")
        return sessions