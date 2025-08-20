import customtkinter as ctk
import cv2
import qrcode
from PIL import Image, ImageTk
import numpy as np
import webbrowser
import os
from tkinter import filedialog, messagebox
import threading
import time
import re

class QRScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("QR Code Scanner")
        self.geometry("800x700")
        self.resizable(True, True)
        
        # Set dark theme as default
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#1a1a1a")
        
        # Initialize variables
        self.camera = None
        self.is_scanning = False
        self.scanned_data = ""
        self.theme_mode = "dark"
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="QR Code Scanner",
            font=("Arial", 32, "bold"),
            text_color="#FFFFFF"
        )
        self.title_label.grid(row=0, column=0, pady=(30, 20))
        
        # Theme toggle button
        self.theme_button = ctk.CTkButton(
            self,
            text="☀️",
            width=50,
            height=35,
            font=("Arial", 18),
            command=self.toggle_theme
        )
        self.theme_button.place(relx=0.95, rely=0.05, anchor="ne")
        
        # Camera frame
        self.camera_frame = ctk.CTkFrame(self)
        self.camera_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.camera_frame.grid_columnconfigure(0, weight=1)
        
        # Camera display label
        self.camera_label = ctk.CTkLabel(
            self.camera_frame,
            text="Camera Feed\n(Click 'Start Camera' to begin)",
            font=("Arial", 16),
            width=400,
            height=300
        )
        self.camera_label.grid(row=0, column=0, pady=20)
        
        # Control buttons frame
        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.grid(row=2, column=0, pady=10, sticky="ew")
        controls_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Start/Stop camera button
        self.camera_button = ctk.CTkButton(
            controls_frame,
            text="Start Camera",
            font=("Arial", 16, "bold"),
            width=150,
            height=40,
            command=self.toggle_camera,
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.camera_button.grid(row=0, column=0, padx=10, pady=10)
        
        # Upload image button
        self.upload_button = ctk.CTkButton(
            controls_frame,
            text="Upload Image",
            font=("Arial", 16, "bold"),
            width=150,
            height=40,
            command=self.upload_image,
            fg_color="#007bff",
            hover_color="#0056b3"
        )
        self.upload_button.grid(row=0, column=1, padx=10, pady=10)
        
        # Clear button
        self.clear_button = ctk.CTkButton(
            controls_frame,
            text="Clear",
            font=("Arial", 16, "bold"),
            width=150,
            height=40,
            command=self.clear_results,
            fg_color="#6c757d",
            hover_color="#545b62"
        )
        self.clear_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Results frame
        results_frame = ctk.CTkFrame(self)
        results_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        # Results title
        results_title = ctk.CTkLabel(
            results_frame,
            text="Scanned Content",
            font=("Arial", 20, "bold"),
            text_color="#FFFFFF"
        )
        results_title.grid(row=0, column=0, pady=(15, 10))
        
        # Results text area
        self.results_text = ctk.CTkTextbox(
            results_frame,
            width=600,
            height=150,
            font=("Arial", 12)
        )
        self.results_text.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="nsew")
        
        # Action buttons frame
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=4, column=0, pady=10, sticky="ew")
        action_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Open link button
        self.open_link_button = ctk.CTkButton(
            action_frame,
            text="Open Link",
            font=("Arial", 16, "bold"),
            width=200,
            height=40,
            command=self.open_link,
            fg_color="#17a2b8",
            hover_color="#138496"
        )
        self.open_link_button.grid(row=0, column=0, padx=10, pady=10)
        
        # Copy to clipboard button
        self.copy_button = ctk.CTkButton(
            action_frame,
            text="Copy to Clipboard",
            font=("Arial", 16, "bold"),
            width=200,
            height=40,
            command=self.copy_to_clipboard,
            fg_color="#ffc107",
            hover_color="#e0a800"
        )
        self.copy_button.grid(row=0, column=1, padx=10, pady=10)
        
        # Info label
        info_label = ctk.CTkLabel(
            self,
            text="Camera scanning and image upload are both supported. Point your camera at a QR code or upload an image.",
            font=("Arial", 12),
            text_color="#888888"
        )
        info_label.grid(row=5, column=0, pady=10)
        
    def toggle_camera(self):
        if not self.is_scanning:
            self.start_camera()
        else:
            self.stop_camera()
            
    def start_camera(self):
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                messagebox.showerror("Error", "Could not open camera! Please check if your camera is connected and not being used by another application.")
                return
                
            self.is_scanning = True
            self.camera_button.configure(text="Stop Camera", fg_color="#dc3545", hover_color="#c82333")
            self.scan_camera()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
            
    def stop_camera(self):
        self.is_scanning = False
        if self.camera:
            self.camera.release()
            self.camera = None
        self.camera_button.configure(text="Start Camera", fg_color="#28a745", hover_color="#218838")
        self.camera_label.configure(text="Camera Feed\n(Click 'Start Camera' to begin)")
        
    def scan_camera(self):
        if not self.is_scanning or self.camera is None:
            return
            
        try:
            ret, frame = self.camera.read()
            if ret:
                # Convert frame to PIL Image for display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame_rgb)
                
                # Resize for display
                display_size = (400, 300)
                pil_image_resized = pil_image.resize(display_size, Image.Resampling.LANCZOS)
                
                # Convert to CTkImage
                ctk_image = ctk.CTkImage(light_image=pil_image_resized, dark_image=pil_image_resized, size=display_size)
                self.camera_label.configure(image=ctk_image, text="")
                
                # Scan for QR codes using OpenCV
                qr_detector = cv2.QRCodeDetector()
                data, bbox, _ = qr_detector.detectAndDecode(frame)
                
                if data and data != self.scanned_data:
                    self.scanned_data = data
                    self.display_results(data)
                    messagebox.showinfo("QR Code Detected", f"Found QR code: {data[:50]}...")
                    self.stop_camera()
                    return
                        
            # Schedule next frame
            self.after(100, self.scan_camera)  # Update every 100ms
            
        except Exception as e:
            print(f"Camera error: {e}")
            self.after(100, self.scan_camera)
        
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select QR Code Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if file_path:
            try:
                # Load and display image
                image = cv2.imread(file_path)
                if image is None:
                    messagebox.showerror("Error", "Could not load image!")
                    return
                    
                # Display image
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(image_rgb)
                display_size = (400, 300)
                pil_image_resized = pil_image.resize(display_size, Image.Resampling.LANCZOS)
                ctk_image = ctk.CTkImage(light_image=pil_image_resized, dark_image=pil_image_resized, size=display_size)
                self.camera_label.configure(image=ctk_image, text="")
                
                # Try to decode QR code using OpenCV
                qr_detector = cv2.QRCodeDetector()
                data, bbox, _ = qr_detector.detectAndDecode(image)
                
                if data:
                    self.scanned_data = data
                    self.display_results(data)
                    messagebox.showinfo("QR Code Found", f"Successfully scanned QR code!")
                else:
                    # If OpenCV fails, try manual QR code detection
                    self.try_manual_qr_detection(image)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {str(e)}")
                
    def try_manual_qr_detection(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Look for square-like contours (potential QR codes)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Minimum area threshold
                # Approximate contour to polygon
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Check if it's roughly square (4 corners)
                if len(approx) == 4:
                    # Extract the region and try to decode
                    x, y, w, h = cv2.boundingRect(contour)
                    roi = image[y:y+h, x:x+w]
                    
                    # Try QR detection on ROI
                    qr_detector = cv2.QRCodeDetector()
                    data, _, _ = qr_detector.detectAndDecode(roi)
                    
                    if data:
                        self.scanned_data = data
                        self.display_results(data)
                        messagebox.showinfo("QR Code Found", f"Successfully scanned QR code!")
                        return
        
        messagebox.showwarning("No QR Code", "No QR code found in the selected image!")
        
    def display_results(self, data):
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", data)
        
    def clear_results(self):
        self.scanned_data = ""
        self.results_text.delete("1.0", "end")
        self.camera_label.configure(image=None, text="Camera Feed\n(Click 'Start Camera' to begin)")
        
    def open_link(self):
        if self.scanned_data:
            # Check if it's a URL
            if self.is_url(self.scanned_data):
                try:
                    webbrowser.open(self.scanned_data)
                    messagebox.showinfo("Success", "Link opened in browser!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open link: {str(e)}")
            else:
                messagebox.showinfo("Info", "The scanned content is not a valid URL.")
        else:
            messagebox.showwarning("Warning", "No content to open!")
            
    def is_url(self, text):
        # Simple URL validation
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(text))
            
    def copy_to_clipboard(self):
        if self.scanned_data:
            self.clipboard_clear()
            self.clipboard_append(self.scanned_data)
            messagebox.showinfo("Success", "Content copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No content to copy!")
            
    def toggle_theme(self):
        if self.theme_mode == "dark":
            self.theme_mode = "light"
            self.theme_button.configure(text="🌙")
            ctk.set_appearance_mode("light")
            self.configure(fg_color="#f8f9fa")
            self.title_label.configure(text_color="#000000")
        else:
            self.theme_mode = "dark"
            self.theme_button.configure(text="☀️")
            ctk.set_appearance_mode("dark")
            self.configure(fg_color="#1a1a1a")
            self.title_label.configure(text_color="#FFFFFF")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = QRScannerApp()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop() 
