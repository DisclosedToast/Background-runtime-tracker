import json
import os
import threading
import time
from datetime import datetime
from pathlib import Path

import psutil
import tkinter as tk
from tkinter import ttk, scrolledtext


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "runtime_sessions.json"
SUMMARY_FILE = BASE_DIR / "runtime_summary.txt"
POLL_SECONDS = 2

TARGETED_APPLICATIONS = {"notepad.exe", "code.exe", "calc.exe"}

current_processes = {}
sessions = []
stop_event = threading.Event()
lock = threading.Lock()
tracking_thread = None
root = None
summary_box = None
status_var = None


def format_hours(seconds):
    return round(seconds / 3600, 2)


def update_status(message):
    if status_var is not None:
        status_var.set(message)


def save_sessions():
    with lock:
        DATA_FILE.write_text(json.dumps(sessions, indent=2), encoding="utf-8")


def load_targets(value):
    names = set()
    for item in value.replace(",", "\n").splitlines():
        clean = item.strip()
        if clean:
            names.add(clean.lower())
    return names


def is_targeted_application(name):
    if not name:
        return False
    return name.lower() in {app.lower() for app in TARGETED_APPLICATIONS}


def scan_processes():
    found = {}

    for process in psutil.process_iter(["pid", "name", "create_time"]):
        try:
            pid = process.info["pid"]
            if pid == os.getpid():
                continue

            app_name = process.info["name"] or "Unknown"

            if not is_targeted_application(app_name):
                continue

            create_time = float(process.info["create_time"])
            found[pid] = {
                "name": app_name,
                "opened": create_time,
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError, TypeError):
            continue

    return found


def refresh_summary_ui():
    if summary_box is None:
        return

    totals = {}
    for session in sessions:
        app = session["application"]
        totals[app] = totals.get(app, 0) + float(session["runtime_hours"])

    lines = ["Application runtime summary", ""]
    if not totals:
        lines.append("No completed sessions yet.")
    else:
        for app, hours in sorted(totals.items()):
            lines.append(f"{app}: {round(hours, 2)} hours")

    summary_box.configure(state="normal")
    summary_box.delete("1.0", tk.END)
    summary_box.insert(tk.END, "\n".join(lines))
    summary_box.configure(state="disabled")


def tracker_loop():
    global current_processes

    current_processes = scan_processes()

    while not stop_event.wait(POLL_SECONDS):
        new_processes = scan_processes()

        for pid, info in new_processes.items():
            if pid not in current_processes:
                current_processes[pid] = info

        for pid in list(current_processes):
            if pid not in new_processes:
                info = current_processes.pop(pid)
                closed = time.time()
                duration = max(0.0, closed - float(info["opened"]))

                with lock:
                    sessions.append({
                        "application": info["name"],
                        "opened": datetime.fromtimestamp(float(info["opened"])).isoformat(timespec="seconds"),
                        "closed": datetime.fromtimestamp(closed).isoformat(timespec="seconds"),
                        "runtime_hours": format_hours(duration),
                    })
                save_sessions()

                if root is not None:
                    root.after(0, refresh_summary_ui)

    update_status("Tracking stopped.")


def start_tracking():
    global TARGETED_APPLICATIONS, tracking_thread

    target_text = app_entry.get()
    target_set = load_targets(target_text)

    if not target_set:
        update_status("Enter at least one app to track.")
        return

    TARGETED_APPLICATIONS = target_set
    update_status("Tracking started...")

    if tracking_thread is not None and tracking_thread.is_alive():
        return

    stop_event.clear()
    tracking_thread = threading.Thread(target=tracker_loop, daemon=True)
    tracking_thread.start()


def stop_tracking():
    global tracking_thread

    stop_event.set()
    update_status("Stopping tracking...")
    save_sessions()
    refresh_summary_ui()


def open_summary_file():
    try:
        os.startfile(str(SUMMARY_FILE.resolve()))
    except OSError:
        pass


def build_gui():
    global root, summary_box, app_entry, status_var

    root = tk.Tk()
    root.title("Application Runtime Tracker")
    root.geometry("520x500")
    root.minsize(420, 420)

    frame = ttk.Frame(root, padding=12)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Tracked apps (one per line or comma-separated):").pack(anchor="w")
    app_entry = ttk.Entry(frame, width=60)
    app_entry.insert(0, "notepad.exe, code.exe, calc.exe")
    app_entry.pack(fill="x", pady=(6, 10))

    btn_row = ttk.Frame(frame)
    btn_row.pack(fill="x", pady=8)

    ttk.Button(btn_row, text="Start Tracking", command=start_tracking).pack(side="left", padx=(0, 8))
    ttk.Button(btn_row, text="Stop Tracking", command=stop_tracking).pack(side="left", padx=(0, 8))
    ttk.Button(btn_row, text="Open Summary", command=open_summary_file).pack(side="left")

    status_var = tk.StringVar(value="Ready")
    ttk.Label(frame, textvariable=status_var, foreground="#2f5f8f").pack(anchor="w", pady=(8, 4))

    ttk.Label(frame, text="Runtime Summary:").pack(anchor="w", pady=(10, 4))
    summary_box = scrolledtext.ScrolledText(frame, height=14, state="disabled")
    summary_box.pack(fill="both", expand=True)

    refresh_summary_ui()

    root.mainloop()


if __name__ == "__main__":
    build_gui()