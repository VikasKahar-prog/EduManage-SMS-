from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import os

root = Tk()
image = PhotoImage(file="image/edumanage_logo (2).png")

height = 430
width = 530

x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)

root.geometry(f"{width}x{height}+{x}+{y}")
root.overrideredirect(True)

# Function to create a gradient background
def create_gradient(canvas, width, height, color1, color2):
    line_count = 500
    for i in range(line_count):
        ratio = i / line_count
        color = "#"
        for j in range(3):
            color_component = int(color1[j] * (1 - ratio) + color2[j] * ratio)
            color += f"{color_component:02x}"
        canvas.create_line(0, i * height // line_count, width, i * height // line_count, fill=color)

root.config(background="#1679AB")
canvas = Canvas(root, width=width, height=height)
canvas.pack(fill="both", expand=True)

# Define the gradient colors (RGB tuples)
color1 = (0, 0, 51)  # Dark Blue
color2 = (0, 102, 204)  # Light Blue

create_gradient(canvas, width, height, color1, color2)

txt = "Welcome to EduManage"
count = 0
text = ""

# Create a text item for the sliding text
sliding_text_item = canvas.create_text(265, 35, text="", font=("Helvetica", 27, "bold"), fill="#FFFFFF")  # White text

def slider():
    global count, text
    if count >= len(txt):
        return
    else:
        text += txt[count]
        canvas.itemconfig(sliding_text_item, text=text)
    
    count += 1
    canvas.after(100, slider)

slider()

# Add the image to the canvas
canvas.create_image(265, 200, image=image)

# Add the progress label to the canvas
progress_label = canvas.create_text(265, 350, text="Loading...", font=("Helvetica", 15, "bold"), fill="#FFFFFF")  # White text

# Customize the progress bar style
progress_style = ttk.Style()
progress_style.theme_use('clam')

# Gradient for progress bar
progress_style.configure("custom.Horizontal.TProgressbar",
                         troughcolor='#1E1E1E',  # Dark grey
                         background='cyan',  # Dark blue for gradient start
                         lightcolor='#0080FF',  # Lighter blue for gradient end
                         darkcolor='#004C99',   # Dark blue (same as background)
                         thickness=20,
                         borderwidth=1,
                         relief='flat')

progress = Progressbar(root, orient=HORIZONTAL, length=400, mode="determinate", style="custom.Horizontal.TProgressbar")
progress.place(x=60, y=380)

def top():
    root.withdraw()
    os.system("python code/schoolmanagementsystem.py")
    root.destroy()

i = 0

def load():
    global i
    if i <= 100:
        txt = f"Loading... {i}%"
        canvas.itemconfig(progress_label, text=txt)
        canvas.after(50, load)  # Speed up the animation for a smoother effect
        progress["value"] = i
        i += 1
    else:
        top()

load()

root.resizable(False, False)
root.mainloop()
