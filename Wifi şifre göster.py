import subprocess
import re
import tkinter as tk
from tkinter import ttk
import pyperclip
import qrcode
from PIL import Image, ImageTk

def get_connected_wifi_password():
    try:
        # Bağlı WiFi ağının adını al
        command = 'netsh wlan show interfaces'
        result = subprocess.check_output(command, shell=True, text=True)
        ssid_match = re.search(r'SSID\s*:\s*(.*)', result)
        if ssid_match:
            connected_wifi_name = ssid_match.group(1)

        # Bağlı WiFi ağının şifresini al
        password_command = f'netsh wlan show profile name="{connected_wifi_name}" key=clear'
        password_result = subprocess.check_output(password_command, shell=True, text=True)
        password_match = re.search(r'Key Content\s*:\s*(.*)', password_result)
        if password_match:
            password = password_match.group(1)
            return connected_wifi_name, password

    except subprocess.CalledProcessError:
        return None, None

def copy_password_to_clipboard(password):
    pyperclip.copy(password)

def generate_qr_code(ssid, password, qr_size=200):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'WIFI:T:WPA;S:{ssid};P:{password};;')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((qr_size, qr_size), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    return img_tk

def main():
    ssid, password = get_connected_wifi_password()

    if ssid and password:
        # GUI oluşturma
        root = tk.Tk()
        root.title("WiFi QR Kodu")
        root.configure(bg="black")

        # Pencere boyutu ayarla
        root.geometry("300x350")

        # QR Kodu görüntüle
        qr_code = generate_qr_code(ssid, password, qr_size=200)
        label = tk.Label(root, image=qr_code, bg="black")
        label.pack(padx=10, pady=10)

        # WiFi Adı ve Şifre etiketleri
        ttk.Label(root, text=f"WiFi Adı: {ssid}", foreground="white", background="black").pack(pady=5)
        ttk.Label(root, text=f"WiFi Şifresi: {password}", foreground="white", background="black").pack(pady=5)

        # Kopyala butonu
        ttk.Button(root, text="Şifreyi Kopyala", command=lambda: copy_password_to_clipboard(password)).pack(pady=10)

        root.mainloop()

    else:
        print("Bağlı WiFi ağı bilgileri alınamadı.")

if __name__ == "__main__":
    main()
