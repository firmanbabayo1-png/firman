import tkinter as tk
from tkinter import messagebox

# Debug: Print status import
print("Step 1: Starting imports...")

# Coba import PIL; jika gagal, lanjut tanpa gambar
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
    print("PIL imported successfully.")
except ImportError as e:
    PIL_AVAILABLE = False
    print(f"PIL not available: {e}. Running without images. Install with: pip install pillow")

print("Step 2: Imports complete. Setting up functions...")

# Fungsi hitung BMI dengan validasi
def hitung_bmi(berat, tinggi_cm):
    try:
        if tinggi_cm <= 0:
            return None  # Hindari division by zero
        tinggi_m = tinggi_cm / 100
        bmi = berat / (tinggi_m ** 2)
        return bmi
    except Exception as e:
        print(f"Error in hitung_bmi: {e}")
        return None

# Fungsi kategori BMI
def kategori_bmi(bmi):
    if bmi is None:
        return "Error: Tinggi tidak valid (harus > 0)"
    if bmi < 18.5:
        return "Underweight (kurus)"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight (kelebihan berat)"
    else:
        return "Obese (obesitas)"

# Fungsi saran AI rinci (dengan font menarik diintegrasikan nanti)
def saran_ai(kategori):
    saran_detail = {
        "Underweight (kurus)": """AI Saran Detail:
- Risiko: Anemia, osteoporosis, kekebalan lemah.
- Diet: Tambah 500-700 kcal/hari (oatmeal, ayam, ikan). Minum susu harian.
- Olahraga: Latihan kekuatan 3x seminggu, yoga.
- Gaya Hidup: Tidur cukup, kelola stres.
- Tips: Target naik 0.5 kg/bulan; konsultasikan ahli gizi.""",
        "Normal": """AI Saran Detail:
- Risiko: Rendah, tapi jaga pola hidup.
- Diet: Seimbang (karbohidrat 45-65%, protein 10-35%, lemak 20-35%). Hindari gula.
- Olahraga: 150 menit/minggu aktivitas sedang + kekuatan 2x.
- Gaya Hidup: Check-up tahunan, hindari rokok.
- Tips: Pantau BMI; promosikan kesehatan mental.""",
        "Overweight (kelebihan berat)": """AI Saran Detail:
- Risiko: Hipertensi, diabetes, jantung.
- Diet: Kurangi 500 kcal/hari (sayur, protein tanpa lemak). Hindari minuman manis.
- Olahraga: Kardio 30 menit/hari + kekuatan 2x.
- Gaya Hidup: Kurangi stres, tidur cukup.
- Tips: Catat makanan; target turun 0.5-1 kg/minggu.""",
        "Obese (obesitas)": """AI Saran Detail:
- Risiko: Stroke, kanker, masalah sendi.
- Diet: 1200-1500 kcal/hari (sayur, protein rendah lemak). Konsultasikan ahli gizi.
- Olahraga: Jalan kaki 20 menit/hari, tingkatkan kardio.
- Gaya Hidup: Ikuti program medis; kelola kondisi seperti sleep apnea.
- Tips: Konsultasikan dokter; fokus jangka panjang.""",
        "Error: Tinggi tidak valid (harus > 0)": "AI Saran: Masukkan tinggi yang valid (>0 cm)."
    }
    return saran_detail.get(kategori, "AI Saran: Periksa input dan konsultasikan profesional.")

# Fungsi animasi fade-in untuk label (ubah fg dari bg ke fg)
def fade_in_label(label, target_fg, steps=10, delay=50):
    current_color = label.cget("bg")  # Mulai dari bg
    label.config(fg=current_color)
    def step(current_step):
        if current_step <= steps:
            # Interpolasi warna sederhana (dari bg ke fg)
            # Untuk kesederhanaan, gunakan gradien biru
            if current_step == steps:
                label.config(fg=target_fg)
            else:
                # Placeholder: langsung set di akhir
                root.after(delay, lambda: step(current_step + 1))
        else:
            label.config(fg=target_fg)
    step(0)

# Fungsi animasi typing effect untuk saran
def type_text(label, text, delay=50):
    label.config(text="")
    def type_char(index):
        if index < len(text):
            label.config(text=label.cget("text") + text[index])
            root.after(delay, lambda: type_char(index + 1))
    type_char(0)

# Fungsi untuk load dan tampilkan gambar berdasarkan kategori
def load_bmi_icon(kategori):
    if not PIL_AVAILABLE:
        return None
    icon_files = {
        "Underweight (kurus)": "underweight_icon.png",
        "Normal": "normal_icon.png",
        "Overweight (kelebihan berat)": "overweight_icon.png",
        "Obese (obesitas)": "obese_icon.png",
        "Error: Tinggi tidak valid (harus > 0)": "error_icon.png"
    }
    file = icon_files.get(kategori, None)
    if file:
        try:
            img = Image.open(file)
            img = img.resize((80, 80))  # Ukuran kecil untuk output
            return ImageTk.PhotoImage(img)
        except FileNotFoundError:
            print(f"Icon file '{file}' not found. Skipping icon.")
        except Exception as e:
            print(f"Error loading icon '{file}': {e}")
    return None

# Flag global untuk mencegah animasi berulang
is_animating = False

# Fungsi tombol hitung dengan debug, animasi, dan gambar
def hitung():
    global is_animating
    if is_animating:
        return  # Abaikan klik jika animasi sedang berlangsung
    
    print("Step 4: Hitung button clicked.")
    try:
        berat = float(entry_berat.get())
        tinggi_cm = float(entry_tinggi.get())
        if berat <= 0 or tinggi_cm <= 0:
            messagebox.showerror("Error", "Berat dan tinggi harus positif!")
            return
        
        is_animating = True  # Set flag
        
        # Reset output sebelum mulai perhitungan baru
        label_bmi.config(text="", fg="#e3f2fd")
        label_kategori.config(text="", fg="#e3f2fd")
        label_saran.config(text="")
        label_icon.pack_forget()  # Hide icon
        
        bmi = hitung_bmi(berat, tinggi_cm)
        kategori = kategori_bmi(bmi)
        saran = saran_ai(kategori)
        
        # Set teks awal (kosong untuk animasi)
        label_bmi.config(text=f"BMI Anda: {bmi:.2f}" if bmi else "BMI: Error")
        label_kategori.config(text=f"Kategori: {kategori}")
        label_saran.config(text="")  # Mulai kosong untuk typing
        
        # Load dan tampilkan gambar icon
        icon = load_bmi_icon(kategori)
        if icon:
            label_icon.config(image=icon)
            label_icon.image = icon  # Keep reference
            label_icon.pack(pady=5)  # Tampilkan jika ada
        else:
            label_icon.pack_forget()  # Sembunyikan jika tidak ada
        
        # Animasi fade-in untuk BMI dan kategori
        fade_in_label(label_bmi, "#1976d2")
        fade_in_label(label_kategori, "#1976d2")
        
        # Animasi typing untuk saran, dan reset flag setelah selesai
        def finish_animation():
            global is_animating
            is_animating = False
        
        type_text(label_saran, saran)
        # Estimasi waktu animasi typing (panjang teks * delay)
        root.after(len(saran) * 50 + 100, finish_animation)  # Tambah buffer
        
        print(f"Calculation complete: BMI {bmi}, Kategori {kategori}")
    except ValueError:
        messagebox.showerror("Error", "Input harus berupa angka!")
        print("Error: Invalid input type.")
        is_animating = False  # Reset flag jika error
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan tak terduga: {str(e)}")
        print(f"Unexpected error in hitung: {e}")
        is_animating = False  # Reset flag jika error

print("Step 3: Functions defined. Setting up GUI...")

# Setup GUI dengan try-except
try:
    root = tk.Tk()
    root.title("Kalkulator BMI dengan AI - xAI Health Assistant")
    root.geometry("550x750")  # Lebih besar untuk saran rinci
    root.configure(bg="#e3f2fd")  # Light blue background

    # Header dengan gambar (fallback tanpa gambar)
    if PIL_AVAILABLE:
        try:
            img = Image.open("health_icon.png")
            img = img.resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            label_img = tk.Label(root, image=photo, bg="#e3f2fd")
            label_img.pack(pady=10)
            print("Image loaded successfully.")
        except FileNotFoundError:
            print("Image file 'health_icon.png' not found. Skipping image.")
        except Exception as e:
            print(f"Error loading image: {e}")
    else:
        print("PIL not available; skipping image.")

    # Judul dengan font menarik (lebih besar, bold, dan underline untuk kesan dramatis)
    title_label = tk.Label(root, text="Kalkulator BMI Pintar", font=("Arial", 26, "bold underline"), bg="#e3f2fd", fg="#1976d2")
    title_label.pack(pady=10)

    # Input Berat (font lebih besar dan bold untuk label)
    frame_berat = tk.Frame(root, bg="#e3f2fd")
    frame_berat.pack(pady=5)
    label_berat = tk.Label(frame_berat, text="Berat Badan (kg):", font=("Arial", 14, "bold"), bg="#e3f2fd", fg="#1976d2")
    label_berat.pack(side=tk.LEFT)
    entry_berat = tk.Entry(frame_berat, font=("Arial", 14), width=10)
    entry_berat.pack(side=tk.LEFT, padx=10)

    # Input Tinggi (font lebih besar dan bold untuk label)
    frame_tinggi = tk.Frame(root, bg="#e3f2fd")
    frame_tinggi.pack(pady=5)
    label_tinggi = tk.Label(frame_tinggi, text="Tinggi Badan (cm):", font=("Arial", 14, "bold"), bg="#e3f2fd", fg="#1976d2")
    label_tinggi.pack(side=tk.LEFT)
    entry_tinggi = tk.Entry(frame_tinggi, font=("Arial", 14), width=10)
    entry_tinggi.pack(side=tk.LEFT, padx=10)

    # Tombol Hitung dengan font menarik (lebih besar, bold, dan relief untuk efek 3D)
    button_hitung = tk.Button(root, text="Hitung BMI", command=hitung, font=("Arial", 16, "bold"), bg="#2196f3", fg="white", relief="raised", bd=5)
    button_hitung.pack(pady=20)

    # Output dengan font menarik (hierarki ukuran untuk menarik perhatian)
    label_bmi = tk.Label(root, text="", font=("Arial", 20, "bold"), bg="#e3f2fd", fg="#e3f2fd")  # Mulai dengan fg sama bg untuk fade
    label_bmi.pack(pady=5)
    label_kategori = tk.Label(root, text="", font=("Arial", 16, "bold italic"), bg="#e3f2fd", fg="#e3f2fd")  # Sama
    label_kategori.pack(pady=5)
    
    # Label untuk icon tubuh (awalnya tidak tampil)
    label_icon = tk.Label(root, bg="#e3f2fd")
    
    label_saran = tk.Label(root, text="", font=("Arial", 12, "italic"), bg="#e3f2fd", fg="#1976d2", wraplength=500, justify="left", anchor="w")
    label_saran.pack(pady=10, padx=20)

    # Footer (font lebih kecil tapi tetap menarik dengan italic)
    footer_label = tk.Label(root, text="Dibuat dengan AI oleh xAI - Konsultasikan dokter untuk nasihat medis.", font=("Arial", 10, "italic"), bg="#e3f2fd", fg="#666")
    footer_label.pack(side=tk.BOTTOM, pady=10)

    print("GUI setup complete. Starting main loop...")
    root.mainloop()
except Exception as e:
    print(f"Error setting up GUI: {e}")
    messagebox.showerror("Error", f"Gagal setup GUI: {str(e)}")

