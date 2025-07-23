import os
from PIL import Image
from pyzbar.pyzbar import decode

QR_FOLDER = "backend/qr_codes"

# List all QR code image files in the folder
qr_files = [f for f in os.listdir(QR_FOLDER) if f.endswith('.png')]

if not qr_files:
    print("No QR code images found in the folder.")
    exit()

print("Available QR code files:")
for idx, file in enumerate(qr_files, start=1):
    print(f"{idx}. {file}")

choice = int(input("Enter the number of the QR code you want to decode: "))

# Get the selected file
selected_file = qr_files[choice - 1]
selected_path = os.path.join(QR_FOLDER, selected_file)

# Decode and show result
def scan_qrcode(image_path):
    img = Image.open(image_path)
    result = decode(img)

    if not result:
        print("No QR code detected.")
        return

    for qr in result:
        print("Decoded QR code content:", qr.data.decode("utf-8"))

scan_qrcode(selected_path)
