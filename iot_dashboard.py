import random
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ALERT_THRESHOLD = 35.0

temperatures = [
    35.32, 44.82, 33.83, 42.20, 31.00,
    42.25, 44.20, 25.96, 22.11, 41.75
]

root = tk.Tk()
root.title("IoT Temperature Dashboard")
root.geometry("900x750")
root.configure(bg="#f4f6f9")

title = tk.Label(
    root,
    text="IoT Temperature Dashboard",
    font=("Arial", 22, "bold"),
    bg="#183153",
    fg="white",
    pady=15
)
title.pack(fill="x")

current_label = tk.Label(
    root, font=("Arial", 17, "bold"),
    bg="#f4f6f9"
)
current_label.pack(pady=15)

alert_label = tk.Label(
    root, font=("Arial", 15, "bold"),
    bg="#f4f6f9"
)
alert_label.pack(pady=5)

graph_frame = tk.Frame(root, bg="#f4f6f9")
graph_frame.pack(fill="both", expand=True, padx=20, pady=10)

figure = Figure(figsize=(8, 3.5), dpi=100)
ax = figure.add_subplot(111)

canvas = FigureCanvasTkAgg(figure, master=graph_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

readings_title = tk.Label(
    root,
    text="Temperature Readings",
    font=("Arial", 15, "bold"),
    bg="#f4f6f9"
)
readings_title.pack(pady=5)

readings_box = tk.Listbox(
    root, height=5, width=35,
    font=("Arial", 10)
)
readings_box.pack(pady=5)


def refresh_dashboard():
    # Add a new simulated sensor reading
    new_temperature = round(random.uniform(22, 46), 2)
    temperatures.append(new_temperature)

    # Keep the latest 10 readings
    if len(temperatures) > 10:
        temperatures.pop(0)

    current = temperatures[-1]

    current_label.config(
        text=f"Current Temperature: {current:.2f} °C"
    )

    if current > ALERT_THRESHOLD:
        alert_label.config(
            text="ALERT: High Temperature!",
            fg="#d62828"
        )
    else:
        alert_label.config(
            text="Status: Normal",
            fg="#218838"
        )

    ax.clear()
    readings = range(1, len(temperatures) + 1)

    ax.plot(
        readings, temperatures,
        marker="o", label="Temperature"
    )
    ax.axhline(
        y=ALERT_THRESHOLD,
        linestyle="--",
        label="Alert Threshold (35°C)"
    )

    ax.set_title("Temperature Trend")
    ax.set_xlabel("Reading Number")
    ax.set_ylabel("Temperature (°C)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    figure.tight_layout()
    canvas.draw()

    readings_box.delete(0, tk.END)

    for index, value in enumerate(temperatures, start=1):
        readings_box.insert(
            tk.END,
            f"Reading {index}: {value:.2f} °C"
        )


refresh_button = ttk.Button(
    root,
    text="Refresh Dashboard",
    command=refresh_dashboard
)
refresh_button.pack(pady=12)

refresh_dashboard()
root.mainloop()
