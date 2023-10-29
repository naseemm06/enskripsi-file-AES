# Mengimpor modul-modul yang diperlukan
import PySimpleGUI as sg
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Membuat fungsi untuk enkripsi foto
def encrypt_photo(filename, key):
    # Membuka file foto dalam mode biner
    with open(filename, "rb") as f:
        # Membaca data biner dari file foto
        data = f.read()
    # Membuat objek AES dengan mode CBC dan key yang diberikan
    cipher = AES.new(key, AES.MODE_CBC)
    # Menambahkan padding jika data tidak kelipatan 16 byte
    pad = 16 - len(data) % 16
    data += bytes([pad]) * pad
    # Mengenkripsi data dengan objek AES
    ciphertext = cipher.encrypt(data)
    # Mengembalikan ciphertext dan iv (initialization vector)
    return ciphertext, cipher.iv

# Membuat fungsi untuk dekripsi foto
def decrypt_photo(ciphertext, iv, key):
    # Membuat objek AES dengan mode CBC, key, dan iv yang diberikan
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Mendekripsi ciphertext dengan objek AES
    data = cipher.decrypt(ciphertext)
    # Menghapus padding jika ada
    pad = data[-1]
    if pad < 16:
        data = data[:-pad]
    # Mengembalikan data biner yang telah didekripsi
    return data

# Membuat layout GUI dengan PySimpleGUI
layout = [
    [sg.Text("Program Enkripsi dan Dekripsi Foto")],
    [sg.Text("Pilih file foto yang ingin dienkripsi:")],
    [sg.Input(key="input_file"), sg.FileBrowse()],
    [sg.Text("Masukkan key enkripsi (16 byte):")],
    [sg.Input(key="key")],
    [sg.Button("Enkripsi"), sg.Button("Dekripsi"), sg.Button("Keluar")],
    [sg.Output(key="output", size=(60, 10))]
]

# Membuat window GUI dengan layout yang telah dibuat
window = sg.Window("Program Enkripsi dan Dekripsi Foto", layout)

# Membuat loop untuk menangani event dan value dari window GUI
while True:
    # Membaca event dan value dari window GUI
    event, values = window.read()
    
    # Jika event adalah "Enkripsi"
    if event == "Enkripsi":
        # Mendapatkan nilai input file dan key dari window GUI
        input_file = values["input_file"]
        key = values["key"]
        
        # Jika input file dan key tidak kosong
        if input_file and key:
            try:
                # Memanggil fungsi encrypt_photo dengan input file dan key yang diberikan
                ciphertext, iv = encrypt_photo(input_file, key.encode())
                # Membuat nama output file dengan menambahkan ekstensi .enc ke input file
                output_file = input_file + ".enc"
                # Membuka output file dalam mode biner
                with open(output_file, "wb") as f:
                    # Menulis iv dan ciphertext ke output file
                    f.write(iv + ciphertext)
                # Menampilkan pesan sukses ke output GUI
                print(f"File {input_file} berhasil dienkripsi menjadi {output_file}")
            except Exception as e:
                # Menampilkan pesan error ke output GUI jika terjadi exception
                print(f"Terjadi kesalahan: {e}")
        else:
            # Menampilkan pesan peringatan ke output GUI jika input file atau key kosong
            print("Harap pilih file foto dan masukkan key enkripsi")
    
    # Jika event adalah "Dekripsi"
    elif event == "Dekripsi":
        # Mendapatkan nilai input file dan key dari window GUI
        input_file = values["input_file"]
        key = values["key"]
        
        # Jika input file dan key tidak kosong
        if input_file and key:
            try:
                # Membuka input file dalam mode biner
                with open(input_file, "rb") as f:
                    # Membaca data biner dari input file
                    data = f.read()
                # Memisahkan iv (16 byte pertama) dan ciphertext (sisanya) dari data biner
                iv = data[:16]
                ciphertext = data[16:]
                # Memanggil fungsi decrypt_photo dengan ciphertext, iv, dan key yang diberikan
                data = decrypt_photo(ciphertext, iv, key.encode())
                # Membuat nama output file dengan menghapus ekstensi .enc dari input file
                output_file = input_file.replace(".enc", "")
                # Membuka output file dalam mode biner
                with open(output_file, "wb") as f:
                    # Menulis data biner yang telah didekripsi ke output file
                    f.write(data)
                # Menampilkan pesan sukses ke output GUI
                print(f"File {input_file} berhasil didekripsi menjadi {output_file}")
            except Exception as e:
                # Menampilkan pesan error ke output GUI jika terjadi exception
                print(f"Terjadi kesalahan: {e}")
        else:
            # Menampilkan pesan peringatan ke output GUI jika input file atau key kosong
            print("Harap pilih file foto dan masukkan key dekripsi")
    
    # Jika event adalah "Keluar" atau window ditutup
    elif event == "Keluar" or event == sg.WIN_CLOSED:
        # Keluar dari loop
        break

# Menutup window GUI
window.close()
