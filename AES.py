from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import tkinter as tk
from tkinter import filedialog

# Fungsi untuk mengenkripsi file dengan kunci yang diberikan


def encrypt_file(key):
    # Membuat objek cipher AES dengan mode ECB
    cipher = AES.new(key, AES.MODE_ECB)
    # Memilih file yang akan dienkripsi
    input_file = filedialog.askopenfilename()
    # Membaca isi file sebagai data biner
    with open(input_file, "rb") as f:
        data = f.read()
    # Mengenkripsi data dengan padding jika perlu
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    # Menyimpan data terenkripsi ke file baru dengan ekstensi .enc
    output_file = input_file + ".enc"
    with open(output_file, "wb") as f:
        f.write(ciphertext)
    # Menampilkan pesan sukses
    tk.messagebox.showinfo("Enkripsi", "File berhasil dienkripsi")

# Fungsi untuk mendekripsi file dengan kunci yang diberikan


def decrypt_file(key):
    # Membuat objek cipher AES dengan mode ECB
    cipher = AES.new(key, AES.MODE_ECB)
    # Memilih file yang akan didekripsi
    input_file = filedialog.askopenfilename()
    # Membaca isi file sebagai data biner
    with open(input_file, "rb") as f:
        data = f.read()
    # Mendekripsi data dengan unpadding jika perlu
    plaintext = unpad(cipher.decrypt(data), AES.block_size)
    # Menyimpan data terdekripsi ke file baru dengan menghapus ekstensi .enc
    output_file = input_file[:-4]
    with open(output_file, "wb") as f:
        f.write(plaintext)
    # Menampilkan pesan sukses
    tk.messagebox.showinfo("Dekripsi", "File berhasil didekripsi")


# Membuat jendela utama GUI
window = tk.Tk()
window.title("Program Python GUI AES")
window.geometry("300x200")

# Membuat label untuk memasukkan kunci enkripsi
key_label = tk.Label(window, text="Masukkan kunci enkripsi (32 byte):")
key_label.pack()

# Membuat entri untuk memasukkan kunci enkripsi
key_entry = tk.Entry(window)
key_entry.pack()

# Membuat tombol untuk mengenkripsi file
encrypt_button = tk.Button(window, text="Enkripsi File",
                           command=lambda: encrypt_file(key_entry.get().encode()))
encrypt_button.pack()

# Membuat tombol untuk mendekripsi file
decrypt_button = tk.Button(window, text="Dekripsi File",
                           command=lambda: decrypt_file(key_entry.get().encode()))
decrypt_button.pack()

# Menjalankan loop utama GUI
window.mainloop()
