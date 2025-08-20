# 📷 QR Code Scanner App (Python + CustomTkinter)

A desktop QR Code Scanner application with camera feed support and image upload functionality built using **Python**, **CustomTkinter**, **OpenCV**, and **Pillow**. Users can scan QR codes in real-time using their webcam or upload an image to detect and decode QR codes.

---

## 🔗 Clone the Repository

```bash
git clone https://github.com/GITWithAkshay/qr-code-scanner-app.git
cd qr-code-scanner-app
```

---

## 🖼️ Features

* 📸 Real-time QR code scanning via webcam
* 🖼️ Image file upload support for scanning QR codes
* 🌗 Light/Dark theme toggle
* 🔗 Open scanned URL in browser
* 📋 Copy scanned content to clipboard
* 📤 Manual fallback decoding using image processing if automatic detection fails
* 🧼 Clear/reset scanning area
* 🪟 Fully resizable and modern GUI built with `CustomTkinter`

---

## 📦 Requirements

Make sure you have **Python 3.8+** installed. Then install dependencies using pip:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

1. Clone the repository
2. Navigate to the project folder
3. Run the app

```bash
python qr_scanner.py
```

---

## 📸 How it Works

* **Start Camera**: Activates your default webcam to scan for QR codes.
* **Upload Image**: Upload any image containing a QR code. The app attempts to decode it.
* **Open Link**: If the scanned data is a URL, open it in your default browser.
* **Copy to Clipboard**: Copies the scanned QR content for easy use.
* **Clear**: Resets the view and scan data.
* **Theme Toggle**: Switch between dark and light modes.

---

## 🛠️ File Structure

```
qr-code-scanner-app/
├── qr_scanner.py      # Main application code
├── README.md          # Project documentation
└── requirements.txt   # (Optional) Dependency list
```

---

## 🧠 Tech Stack

* [Python](https://www.python.org/)
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* [OpenCV](https://opencv.org/)
* [Pillow (PIL)](https://python-pillow.org/)
* [qrcode](https://pypi.org/project/qrcode/)

---

## 📷 Screenshots

![image alt](https://github.com/GITWithAkshay/PRODIGY_AD_05/blob/b49679c338967246b7fcf685c697dd0635f6d62d/Screenshot%20(205).png)
![image alt](https://github.com/GITWithAkshay/PRODIGY_AD_05/blob/b49679c338967246b7fcf685c697dd0635f6d62d/Screenshot%20(206).png)
![image alt](https://github.com/GITWithAkshay/PRODIGY_AD_05/blob/b49679c338967246b7fcf685c697dd0635f6d62d/Screenshot%20(209).png)

---

## 🙏 Acknowledgements

* [Tom Schimansky](https://github.com/TomSchimansky) for [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - a beautiful, modern replacement for Tkinter.
* [OpenCV](https://opencv.org/) for providing the computer vision toolkit.
* [Pillow](https://python-pillow.org/) for image processing.
* All contributors and open-source maintainers who power the Python ecosystem.

---

## 📄 License

Feel free to use, modify, and distribute.

---
