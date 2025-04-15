import tkinter as tk
from tkinter import messagebox

# Cek Target Tercapai/Tidak
def is_target_reached(jug1, jug2, jug3, target):
    return jug1 == target or jug2 == target or jug3 == target

# Win using DFS
def water_jug_dfs(capacity1, capacity2, capacity3, target):
    stack = [(0, 0, 0)] 
    visited = set()
    visited.add((0, 0, 0))
    path = []

    while stack:
      # Tampilkan stack di UI
        update_stack_display(stack)
        
        jug1, jug2, jug3 = stack.pop()  # Ambil elemen terakhir 
        path.append((jug1, jug2, jug3))

        if is_target_reached(jug1, jug2, jug3, target):
            return path  # Target tercapai, return langkah-langkah yang diambil

        # Kemungkinan keadaan berikutnya
        possible_states = [
            (capacity1, jug2, jug3),  # Isi kendi 1
            (jug1, capacity2, jug3),  # Isi kendi 2
            (jug1, jug2, capacity3),  # Isi kendi 3
            (0, jug2, jug3),          # Kosongkan jug1
            (jug1, 0, jug3),          # Kosongkan jug2
            (jug1, jug2, 0),          # Kosongkan jug3
            # Tuang dari 1 ke 2
            (jug1 - min(jug1, capacity2 - jug2), jug2 + min(jug1, capacity2 - jug2), jug3),
            # Tuang dari 1 ke 3
            (jug1 - min(jug1, capacity3 - jug3), jug2, jug3 + min(jug1, capacity3 - jug3)),
            # Tuang dari 2 ke 1
            (jug1 + min(jug2, capacity1 - jug1), jug2 - min(jug2, capacity1 - jug1), jug3),
            # Tuang dari 2 ke 3
            (jug1, jug2 - min(jug2, capacity3 - jug3), jug3 + min(jug2, capacity3 - jug3)),
            # Tuang dari 3 ke 1
            (jug1 + min(jug3, capacity1 - jug1), jug2, jug3 - min(jug3, capacity1 - jug1)),
            # Tuang dari 3 ke 2
            (jug1, jug2 + min(jug3, capacity2 - jug2), jug3 - min(jug3, capacity2 - jug2))
        ]

        # Tambahkan keadaan yang belum dikunjungi ke stack
        for state in possible_states:
            if state not in visited:
                stack.append(state)
                visited.add(state)

    return []  # No solution
  
  
# Gambar Jug di Canvas
def update_canvas(jug1, jug2, jug3, target):
    canvas.delete("all")  
    canvas_width = canvas.winfo_width()  
    margin = 50  
    spacing = (canvas_width - 2 * margin - 3 * 100) // 2 

    # Posisi Jug Simetris di Canvas
    draw_jug(margin, 50, 100, 200, jug1, capacity1, "Jug 1", target)
    draw_jug(margin + 100 + spacing, 50, 100, 200, jug2, capacity2, "Jug 2", target)
    draw_jug(margin + 2 * (100 + spacing), 50, 100, 200, jug3, capacity3, "Jug 3", target)  

# Label Jug
def draw_jug(x, y, width, height, current_volume, max_capacity, label, target):
    # Jug
    canvas.create_rectangle(x, y, x + width, y + height, outline="black", width=2)

    if max_capacity > 0:
        filled_height = int((current_volume / max_capacity) * height)
    else:
        filled_height = 0

    # Win Color
    fill_color = "#007C01" if current_volume == target else "#085DB4"
    
    canvas.create_rectangle(x, y + (height - filled_height), x + width, y + height, fill=fill_color)
    # Label Atas Jug
    canvas.create_text(x + width / 2, y - 15, text=label, font=("Arial", 12, "bold"))
    # Label Bawah Jug
    canvas.create_text(x + width / 2, y + height + 10, text=f"{current_volume}L", font=("Arial", 12))

# Animasi Delay DFS
def animate_solution(steps, delay=1000):
    if steps:
        jug1, jug2, jug3 = steps.pop(0)
        update_canvas(jug1, jug2, jug3, target)
        solution_label.config(text=f"Langkah Akhir: Jug1: {jug1}L, Jug2: {jug2}L, Jug3: {jug3}L")
        root.after(delay, animate_solution, steps)

# Fungsi untuk memperbarui tampilan stack di UI
def update_stack_display(stack):
    stack_display.delete(1.0, tk.END)  # Hapus isi sebelumnya
    stack_display.insert(tk.END, "Stack DFS:\n")
    
    for state in stack:
        stack_display.insert(tk.END, f"{state[0]}L - {state[1]}L - {state[2]}L\n")

# Fungsi untuk memulai game berdasarkan input dari UI
def start_game():
    global capacity1, capacity2, capacity3, target
    try:
        capacity1 = int(entry_kendi1.get())
        capacity2 = int(entry_kendi2.get())
        capacity3 = int(entry_kendi3.get())
        target = int(entry_target.get())

        if target > max(capacity1, capacity2, capacity3):
            messagebox.showerror("Error", "Target tidak mungkin dicapai.")
        else:
            path = water_jug_dfs(capacity1, capacity2, capacity3, target)
            if path:
                animate_solution(path)
            else:
                messagebox.showinfo("Tidak ada solusi", "Tidak ada solusi yang ditemukan.")
    except ValueError:
        messagebox.showerror("Input Error", "Pastikan semua input adalah angka.")

# Fungsi untuk menempatkan window di tengah layar
def center_window(root, width=619, height=700):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

# Membuat UI menggunakan Tkinter
root = tk.Tk()
root.title("Water Jug Game")
root.configure(bg="#085DB4")  
center_window(root)

# Grid configuration to stretch the layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# JUDUL
title_label = tk.Label(root, text="WATER JUG", font=("Arial", 24, "bold"), bg="#085DB4", fg="white")
title_label.grid(row=0, column=0, pady=(20, 10), sticky="nsew")  

# Frame untuk Input
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.grid(row=1, column=0, sticky="ew")

# Mengatur agar input_frame mengisi kolom secara horizontal
input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_columnconfigure(1, weight=1)

# Label dan Entry Jug1
label_kendi1 = tk.Label(input_frame, text="Kapasitas Kendi 1 (L) :", font=("Arial", 12), bg="#F0F0F0")
label_kendi1.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
entry_kendi1 = tk.Entry(input_frame, width=10)
entry_kendi1.grid(row=0, column=1, padx=5, pady=5)

# Label dan Entry Jug2 
label_kendi2 = tk.Label(input_frame, text="Kapasitas Kendi 2 (L) :", font=("Arial", 12), bg="#F0F0F0")
label_kendi2.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
entry_kendi2 = tk.Entry(input_frame, width=10)
entry_kendi2.grid(row=1, column=1, padx=5, pady=5)

# Label dan Entry Jug3
label_kendi3 = tk.Label(input_frame, text="Kapasitas Kendi 3 (L) :", font=("Arial", 12), bg="#F0F0F0")
label_kendi3.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
entry_kendi3 = tk.Entry(input_frame, width=10)
entry_kendi3.grid(row=2, column=1, padx=5, pady=5)

# Label dan Entry Target
label_target = tk.Label(input_frame, text="Target (L) :", font=("Arial", 12), bg="#F0F0F0")
label_target.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
entry_target = tk.Entry(input_frame, width=10)
entry_target.grid(row=3, column=1, padx=5, pady=5)

# Button Start
start_button = tk.Button(input_frame, text="Mulai Game", font=("Arial", 12, "bold"), bg="#085DB4", fg="white", command=start_game)
start_button.grid(row=4, column=0, pady=10, sticky="e") 


# Frame untuk Canvas dan Stack
canvas_stack_frame = tk.Frame(root)
canvas_stack_frame.grid(row=2, column=0, sticky="nsew")

# Canvas Jug
canvas = tk.Canvas(canvas_stack_frame, width=450, height=325, bg="white")
canvas.pack(side="left", padx=10, pady=50)

# Textbox Stack
stack_display = tk.Text(canvas_stack_frame, width=20, height=18.5)
stack_display.pack(side="right", padx=10, pady=10)

# Label Final Path
solution_label = tk.Label(root, text="", font=("Arial", 13, "bold"),fg="white", bg="#085DB4")
solution_label.grid(row=3, column=0, pady=10)

root.mainloop()
