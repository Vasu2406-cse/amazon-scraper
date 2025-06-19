import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image,ImageTk
import os

class ImageViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Viewer")
        self.geometry("600x450")
        self.configure(bg="gray")

        self.image_list = []
        self.image_index = 0
        self.current_image = None  # Keep a reference to the image

        # Canvas for displaying images
        self.canvas = tk.Canvas(self, width=600, height=400, bg="black")
        self.canvas.pack()

        # Frame for buttons
        button_frame = tk.Frame(self, bg="gray")
        button_frame.pack(pady=10)

        # Previous button
        self.prev_button = tk.Button(button_frame, text="Previous", width=10, command=self.show_previous_image)
        self.prev_button.grid(row=0, column=0, padx=10)

        # Load Images button
        self.load_button = tk.Button(button_frame, text="Load Images", width=15, command=self.load_images)
        self.load_button.grid(row=0, column=1, padx=10)

        # Next button
        self.next_button = tk.Button(button_frame, text="Next", width=10, command=self.show_next_image)
        self.next_button.grid(row=0, column=2, padx=10)

    def load_images(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.image_list = [os.path.join(folder_selected, f) for f in os.listdir(folder_selected)
                               if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            if self.image_list:
                self.image_index = 0
                self.show_image(self.image_list[self.image_index])
            else:
                messagebox.showerror("No Images", "No supported image files found in the selected folder.")

    def show_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((600, 400), Image.Resampling.LANCZOS)  # Updated for Pillow ≥10
            self.current_image = ImageTk.PhotoImage(img)
            self.canvas.delete("all")  # Clear previous image
            self.canvas.create_image(0, 0, anchor="nw", image=self.current_image)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load image:\n{e}")

    def show_next_image(self):
        if self.image_list:
            self.image_index = (self.image_index + 1) % len(self.image_list)
            self.show_image(self.image_list[self.image_index])

    def show_previous_image(self):
        if self.image_list:
            self.image_index = (self.image_index - 1) % len(self.image_list)
            self.show_image(self.image_list[self.image_index])

if __name__ == "__main__":
    app = ImageViewer()
    app.mainloop()

 