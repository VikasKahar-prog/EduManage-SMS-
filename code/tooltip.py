import tkinter as tk

class ToolTip:
    def __init__(self, widget , text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<FocusIn>", self.destroy_tooltip)

    def show_tooltip(self, event):
        if self.tip_window:
            return
        x, y , cx, cy = self.widget.bbox("insert")

        x += self.widget.winfo_rootx() + 28
        y += self.widget.winfo_rooty() + 28

        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")

        frame = tk.Frame(self.tip_window, background="white",relief='solid', highlightthickness=2, highlightbackground="#050C9C")
        frame.pack()

        label = tk.Label(frame, text=self.text, justify='left',
        background="white", foreground="#050C9C", 
        font=("Calibri", 11), wraplength=200, padx=10, pady=5)
        label.pack()

    def hide_tooltip(self, event):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

    def destroy_tooltip(self, event):
        if self.tip_window:
            self.tip_window.destroy()


