import tkinter as tk
from tkinter import messagebox, Toplevel
import subprocess
import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.models import load_model

def on_collect_click(information_text):
    # Warning for collect
    result = messagebox.askyesno("Warning", "This will collect data. Do you want to proceed?")
    
    if result:
        try:
            output = subprocess.check_output(["python3", "scanip1.py"], text=True)
            information_text.insert(tk.END, f"collect clicked. Collecting data...\n{output}\n")
        except subprocess.CalledProcessError as e:
            information_text.insert(tk.END, f"Error running scanip1.py: {e}\n")

# Fetch Model
current_directory = os.getcwd()
model_file = 'PD1-1.h5'
model_path = os.path.join(current_directory, model_file)
model = load_model(model_path)

def on_forecast_click():
    # Warning
    result = messagebox.askyesno("Warning", "This will run forecasting. Do you want to proceed?")
    
    if result:
        try:
            # Perform forecasting using your loaded model
            # For example, you can generate some dummy input data for demonstration
            input_data = np.random.rand(50, 10, 1)  # Adjust input_shape according to your model
            
            # Perform prediction using the loaded model
            predictions = model.predict(input_data)
            
            # Process predictions as needed
            # For demonstration purposes, you can convert predictions to a string
            output = "\n".join([str(prediction) for prediction in predictions])
            
            # Show forecasting information
            show_forecasting_information(output, None)
        except Exception as e:
            show_forecasting_information(None, f"Error during forecasting: {e}")

def show_forecasting_information(output, error_output):
    # Create a new window for forecasting information
    forecasting_window = tk.Toplevel()
    forecasting_window.title("Forecasting Information")
    
    # Set background color for the forecasting window
    forecasting_window.configure(bg='#238BD6')
    
    # Create and add widgets to the forecasting window
    forecasting_label = tk.Label(forecasting_window, text="Forecasting information:", bg='#238BD6', fg='black')  # Set text and background color
    forecasting_label.pack(pady=10)
    
    forecasting_text = tk.Text(forecasting_window, fg='black')  # Set text and background color
    if output is not None:
        forecasting_text.insert(tk.END, f"\n{output}")
    elif error_output is not None:
        forecasting_text.insert(tk.END, f"{error_output}")
    forecasting_text.pack(padx=10, pady=10)

def customize_gui(background_color, window_size):
    root = tk.Tk()
    root.title("Predictive Maintenance System")
    
    # Set background color
    root.configure(bg=background_color)
    
    # Set window size
    root.geometry(window_size)
    
    # Define appearance customization
    button_style = {
        "bg": '#0F6BAE',  # Background color
        "fg": 'white',    # Text color
        "font": ('Helvetica'),  # Font family and size
        "width": 15,      # Button width
        "height": 1,      # Button height
        "relief": tk.FLAT,  # Button border style (RAISED, SUNKEN, FLAT, etc.)
    }
    
    # Create a frame for centering buttons vertically
    center_frame = tk.Frame(root, bg=background_color)
    center_frame.pack(side=tk.LEFT, padx=30, pady=(root.winfo_reqheight() // 0.8), fill=tk.Y)
    
    # Info Display Widget
    information_text = tk.Text(root, height=35, width=90, wrap=tk.WORD)
    information_text.pack(side=tk.RIGHT, padx=40, pady=10)
    
    # Collect Button
    collect = tk.Button(center_frame, text="Collect", command=lambda: on_collect_click(information_text), **button_style)
    collect.pack(pady=10, fill=tk.X)
    
    # Forecast Button
    forecast = tk.Button(center_frame, text="Forecast", command=on_forecast_click, **button_style)
    forecast.pack(pady=10, fill=tk.X)
    
    # Run the main loop
    root.mainloop()

# Customize your GUI here
custom_background_color = '#238BD6'  # Example color code
custom_window_size = "1000x600"  # Example window size (width x height)

# Call the function to create the customized GUI
customize_gui(custom_background_color, custom_window_size)
