import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

class SignatureVerificationApp:

        
    def __init__(self, master):
        self.master = master
        self.master.title("Signature Verification")
        self.master.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Signature Verification", font=("Arial", 20))
        self.title_label.pack(pady=20)

        self.frame1 = tk.Frame(self.master)
        self.frame1.pack(side=tk.LEFT, padx=20)

        self.frame2 = tk.Frame(self.master)
        self.frame2.pack(side=tk.RIGHT, padx=20)

        self.label1 = tk.Label(self.frame1, text="Signature 1")
        self.label1.pack()

        self.canvas1 = tk.Canvas(self.frame1, width=300, height=200, bg="white")
        self.canvas1.pack()

        self.upload_btn1 = tk.Button(self.frame1, text="Upload Signature 1", command=lambda: self.upload_image(1))
        self.upload_btn1.pack(pady=10)

        self.label2 = tk.Label(self.frame2, text="Signature 2")
        self.label2.pack()

        self.canvas2 = tk.Canvas(self.frame2, width=300, height=200, bg="white")
        self.canvas2.pack()

        self.upload_btn2 = tk.Button(self.frame2, text="Upload Signature 2", command=lambda: self.upload_image(2))
        self.upload_btn2.pack(pady=10)

        self.verify_btn = tk.Button(self.master, text="Verify Signatures", command=self.verify_signatures)
        self.verify_btn.pack(pady=20)

        self.result_label = tk.Label(self.master, text="", font=("Arial", 14))
        self.result_label.pack()

        self.start_again_btn = tk.Button(self.master, text="Start Again", command=self.start_again)
        self.start_again_btn.pack(pady=10)

    def upload_image(self, canvas_num):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((300, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            if canvas_num == 1:
                self.canvas1.image = photo
                self.canvas1.create_image(0, 0, anchor=tk.NW, image=photo)
                self.signature1 = cv2.imread(file_path, 0)
            else:
                self.canvas2.image = photo
                self.canvas2.create_image(0, 0, anchor=tk.NW, image=photo)
                self.signature2 = cv2.imread(file_path, 0)

    def verify_signatures(self):
        if hasattr(self, 'signature1') and hasattr(self, 'signature2'):
            result = cv2.matchTemplate(self.signature1, self.signature2, cv2.TM_CCOEFF_NORMED)
            similarity = np.max(result)
            
            if similarity > 0.8:
                self.result_label.config(text="Signatures match!", fg="green")
            else:
                self.result_label.config(text="Signatures do not match.", fg="red")
        else:
            messagebox.showwarning("Warning", "Please upload both signatures.")

    def start_again(self):
        self.canvas1.delete("all")
        self.canvas2.delete("all")
        self.result_label.config(text="")
        if hasattr(self, 'signature1'):
            del self.signature1
        if hasattr(self, 'signature2'):
            del self.signature2

if __name__ == "__main__":
    root = tk.Tk()
    app = SignatureVerificationApp(root)
    root.mainloop()
