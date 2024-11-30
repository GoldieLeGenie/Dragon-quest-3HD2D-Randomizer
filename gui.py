import tkinter as tk
from tkinter import ttk, messagebox
import randomize
import subprocess
import shutil
import os
# Paths and commands
unrealpak_path = r"repak.exe"
source_folder = r"Game-WindowsNoEditor_test"
command = [unrealpak_path, "pack", source_folder]
game_folder = r"Game-WindowsNoEditor_test/Game/Content/Nicola/Data/DataTable"

def clear_game_folder():
    """Clear the contents of the game folder before proceeding."""
    try:
        for filename in os.listdir(game_folder):
            file_path = os.path.join(game_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete files in {game_folder}: {e}")


def toggle_area_options():
    """Enable or disable options related to area randomization."""
    state = 'normal' if area_var.get() else 'disabled'
    min_area_spinbox.config(state=state)
    max_area_spinbox.config(state=state)
    gold_spinbox.config(state=state)
    items_spinbox.config(state=state)
    empty_spinbox.config(state=state)


def toggle_price_options():
    """Enable or disable options related to price randomization."""
    state = 'normal' if price_var.get() else 'disabled'
    min_price_spinbox.config(state=state)
    max_price_spinbox.config(state=state)

def toggle_shine_options():
    """Enable or disable options related to shine object randomization."""
    state = 'normal' if shine_var.get() else 'disabled'
    min_shine_spinbox.config(state=state)
    max_shine_spinbox.config(state=state)

def process_selection():
    if not (shop_var.get() or price_var.get() or area_var.get() or shine_var.get() or medals_var.get() or other_var.get() or monster_var.get() or monster_drop_var.get() or skills_var.get()):
        messagebox.showerror("Error", "Please select at least one randomization option.")
        return
    
    clear_game_folder()
    if shop_var.get():
        randomize.randomize_shop_items()
    if price_var.get():
        min_price = int(min_price_spinbox.get())
        max_price = int(max_price_spinbox.get())
        if min_price >= max_price:
            messagebox.showerror("Error", "Min Price should be less than Max Price")
            return
        randomize.randomize_buy_price(min_price, max_price)
    if area_var.get():
        min_area = int(min_area_spinbox.get())
        max_area = int(max_area_spinbox.get())
        if min_area >= max_area:
            messagebox.showerror("Error", "Min Gold should be less than Max Gold")
            return
        gold_percentage = int(gold_spinbox.get())
        items_percentage = int(items_spinbox.get())
        empty_percentage = int(empty_spinbox.get())
        if gold_percentage + items_percentage + empty_percentage != 100:
            messagebox.showerror("Error", "Total percentage should equal 100%")
            return
        randomize.randomize_all_area_loot(min_area, max_area, gold_percentage, items_percentage, empty_percentage)
    
    if shine_var.get():
        min_gold = int(min_shine_spinbox.get())
        max_gold = int(max_shine_spinbox.get())
        if min_gold >= max_gold:
            messagebox.showerror("Error", "Min Price should be less than Max Price")
            return
        randomize.randomize_shine_items(min_gold, max_gold)
        
    if medals_var.get():
        randomize.randomize_mini_medals_rewards()
    if other_var.get():
        randomize.randomize_start_bag_items()
    if monster_var.get():
        randomize.randomize_monster_spawn()
    if monster_drop_var.get():
        randomize.randomize_monster_drop()
    if skills_var.get():
        randomize.randomize_learning()
    try:
        subprocess.run(command, check=True)
        shutil.move("Game-WindowsNoEditor_test.pak", "./pak/Game-WindowsNoEditor_test.pak")
        clear_game_folder()
        messagebox.showinfo("Success", "Randomization completed! Copy the .pak file and paste it into the game folder's pak directory (..\Program Files (x86)\Steam\steamapps\common\DRAGON QUEST III HD-2D Remake\Game\Content\Paks).")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "There was an error creating the .pak file!")
    
# Main interface
root = tk.Tk()
root.title("DQ3-HD-RANDOMIZER V0.1 by Goldie :)")
root.geometry('450x650')
root.config(bg="#2e2e2e")

style = ttk.Style()
style.configure('TNotebook', background="#2e2e2e", foreground="white", padding=5)
style.configure('TCheckbutton', background="#2e2e2e", foreground="white", font=('Arial', 12))
style.configure('TLabel', background="#2e2e2e", foreground="white", font=('Arial', 12))
style.configure('TSpinbox', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12))

notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill="both", expand=True)

shop_tab = tk.Frame(notebook, bg="#1e1e1e")
area_tab = tk.Frame(notebook, bg="#1e1e1e")
other_tab = tk.Frame(notebook, bg="#1e1e1e")

notebook.add(shop_tab, text="Shop")
notebook.add(area_tab, text="Area")
notebook.add(other_tab, text="Other")

# Variables
shop_var = tk.BooleanVar()
price_var = tk.BooleanVar()
area_var = tk.BooleanVar()
medals_var = tk.BooleanVar()
other_var = tk.BooleanVar()
monster_var = tk.BooleanVar()
monster_drop_var = tk.BooleanVar()
shine_var = tk.BooleanVar()
skills_var =  tk.BooleanVar()

# Shop tab
ttk.Checkbutton(shop_tab, text="Randomize Shop Items", variable=shop_var).pack(anchor="w", pady=5)
ttk.Checkbutton(shop_tab, text="Randomize Shop Prices", variable=price_var, command=toggle_price_options).pack(anchor="w", pady=5)

price_frame = tk.Frame(shop_tab, bg="#1e1e1e")
price_frame.pack(anchor="w", pady=5)

ttk.Label(price_frame, text="Min Gold:").grid(row=0, column=0, sticky="w", padx=10)
min_price_spinbox = ttk.Spinbox(price_frame, from_=1, to=500000, state='disabled', font=('Arial', 12), width=10)
min_price_spinbox.set(1)  # Default value
min_price_spinbox.grid(row=0, column=1, padx=20)

ttk.Label(price_frame, text="Max Gold:").grid(row=1, column=0, sticky="w", padx=10)
max_price_spinbox = ttk.Spinbox(price_frame, from_=1, to=500000, state='disabled', font=('Arial', 12), width=10)
max_price_spinbox.set(500000)  # Default value
max_price_spinbox.grid(row=1, column=1, padx=20)

# Area tab
ttk.Checkbutton(area_tab, text="Randomize Areas (chest,pot...)", variable=area_var, command=toggle_area_options).pack(anchor="w", pady=5)

area_frame = tk.Frame(area_tab, bg="#1e1e1e")
area_frame.pack(anchor="w", pady=5)

ttk.Label(area_frame, text="Min Gold:").grid(row=0, column=0, sticky="w", padx=10)
min_area_spinbox = ttk.Spinbox(area_frame, from_=1, to=500000, state='disabled', font=('Arial', 12), width=10)
min_area_spinbox.set(1)  # Default value
min_area_spinbox.grid(row=0, column=1, padx=20)

ttk.Label(area_frame, text="Max Gold:").grid(row=1, column=0, sticky="w", padx=10)
max_area_spinbox = ttk.Spinbox(area_frame, from_=1, to=500000, state='disabled', font=('Arial', 12), width=10)
max_area_spinbox.set(500000)  # Default value
max_area_spinbox.grid(row=1, column=1, padx=20)

ttk.Label(area_frame, text="Gold %:").grid(row=2, column=0, sticky="w", padx=10)
gold_spinbox = ttk.Spinbox(area_frame, from_=0, to=100, state='disabled', font=('Arial', 12), width=10)
gold_spinbox.set(0)  # Default value
gold_spinbox.grid(row=2, column=1, padx=20)

ttk.Label(area_frame, text="Items %:").grid(row=3, column=0, sticky="w", padx=10)
items_spinbox = ttk.Spinbox(area_frame, from_=0, to=100, state='disabled', font=('Arial', 12), width=10)
items_spinbox.set(0)  # Default value
items_spinbox.grid(row=3, column=1, padx=20)

ttk.Label(area_frame, text="Empty %:").grid(row=4, column=0, sticky="w", padx=10)
empty_spinbox = ttk.Spinbox(area_frame, from_=0, to=100, state='disabled', font=('Arial', 12), width=10)
empty_spinbox.set(0)  # Default value
empty_spinbox.grid(row=4, column=1, padx=20)

# Shine tab
ttk.Checkbutton(area_tab, text="Randomize Shine Object", variable=shine_var, command=toggle_shine_options).pack(anchor="w", pady=5)

shine_frame = tk.Frame(area_tab, bg="#1e1e1e")
shine_frame.pack(anchor="w", pady=5)

ttk.Label(shine_frame, text="Min Gold:").grid(row=0, column=0, sticky="w", padx=10)
min_shine_spinbox = ttk.Spinbox(shine_frame, from_=1, to=500000, state='disabled', font=('Arial', 12), width=10)
min_shine_spinbox.set(1)  # Default value
min_shine_spinbox.grid(row=0, column=1, padx=20)

ttk.Label(shine_frame, text="Max Gold:").grid(row=1, column=0, sticky="w", padx=10)
max_shine_spinbox = ttk.Spinbox(shine_frame, from_=1, to=500000, state='disabled', font=('Arial', 12), width=10)
max_shine_spinbox.set(500000)  # Default value
max_shine_spinbox.grid(row=1, column=1, padx=20)

# Other tab
ttk.Checkbutton(other_tab, text="Randomize Learning Skills", variable=skills_var).pack(anchor="w", pady=5)
ttk.Checkbutton(other_tab, text="Randomize Mini Medals Rewards", variable=medals_var).pack(anchor="w", pady=5)
ttk.Checkbutton(other_tab, text="Randomize Start Bag Items", variable=other_var).pack(anchor="w", pady=5)
ttk.Checkbutton(other_tab, text="Randomize Monster Spawns", variable=monster_var).pack(anchor="w", pady=5)
ttk.Checkbutton(other_tab, text="Randomize Monster Drops", variable=monster_drop_var).pack(anchor="w", pady=5)

# Apply Button
apply_button = ttk.Button(root, text="Randomize", command=process_selection)
apply_button.pack(pady=10)

def start():
    root.mainloop()
