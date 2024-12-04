import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
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
    state = 'normal' if area_var.get() else 'disabled'
    min_area_spinbox.config(state=state)
    max_area_spinbox.config(state=state)
    gold_spinbox.config(state=state)
    items_spinbox.config(state=state)
    empty_spinbox.config(state=state)

def toggle_price_options():
    state = 'normal' if price_var.get() else 'disabled'
    min_price_spinbox.config(state=state)
    max_price_spinbox.config(state=state)

def toggle_shine_options():
    state = 'normal' if shine_var.get() else 'disabled'
    min_shine_spinbox.config(state=state)
    max_shine_spinbox.config(state=state)

def process_selection():
    if not any([area_no_dupe_var.get(), shop_var.get(), price_var.get(), area_var.get(), shine_var.get(), medals_var.get(), other_var.get(), monster_var.get(), monster_drop_var.get(), skills_var.get(), shine_no_dupe_var.get()]):
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
        else:
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
    if shine_no_dupe_var.get():
        randomize.randomize_shine_items_no_dupes()
    if area_no_dupe_var.get():
        randomize.randomize_all_area_loot_no_dupes()
    try:
        subprocess.run(command, check=True)
        shutil.move("Game-WindowsNoEditor_test.pak", "./pak/Game-WindowsNoEditor_test.pak")
        clear_game_folder()
        messagebox.showinfo("Success", "Randomization completed! Copy the .pak file and paste it into the game folder's pak directory.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "There was an error creating the .pak file!")


# Main interface
root = ttk.Window(themename="darkly")  # Options: darkly, litera, journal, etc.
root.title("DQ3-HD-RANDOMIZER V0.3 by Goldie :)")
root.geometry('500x700')

notebook = ttk.Notebook(root, bootstyle="primary")
notebook.pack(padx=10, pady=10, fill="both", expand=True)

# Create Tabs
shop_tab = ttk.Frame(notebook)
area_tab = ttk.Frame(notebook)
other_tab = ttk.Frame(notebook)

notebook.add(shop_tab, text="Shop")
notebook.add(area_tab, text="Area")
notebook.add(other_tab, text="Other")

# Variables
shop_var = ttk.BooleanVar()
price_var = ttk.BooleanVar()
area_var = ttk.BooleanVar()
area_no_dupe_var = ttk.BooleanVar()
medals_var = ttk.BooleanVar()
other_var = ttk.BooleanVar()
monster_var = ttk.BooleanVar()
monster_drop_var = ttk.BooleanVar()
shine_var = ttk.BooleanVar()
skills_var = ttk.BooleanVar()
shine_no_dupe_var = ttk.BooleanVar()

# Shop tab
ttk.Checkbutton(shop_tab, text="Randomize Shop Items", variable=shop_var, bootstyle="info").pack(anchor="w", pady=5)
ttk.Checkbutton(shop_tab, text="Randomize Shop Prices", variable=price_var, bootstyle="info", command=toggle_price_options).pack(anchor="w", pady=5)

price_frame = ttk.Frame(shop_tab)
price_frame.pack(anchor="w", pady=5)

ttk.Label(price_frame, text="Min Gold:").grid(row=0, column=0, sticky="w", padx=10)
min_price_spinbox = ttk.Spinbox(price_frame, from_=1, to=500000, state='disabled', width=10)
min_price_spinbox.set(1)
min_price_spinbox.grid(row=0, column=1, padx=20)

ttk.Label(price_frame, text="Max Gold:").grid(row=1, column=0, sticky="w", padx=10)
max_price_spinbox = ttk.Spinbox(price_frame, from_=1, to=500000, state='disabled', width=10)
max_price_spinbox.set(500000)
max_price_spinbox.grid(row=1, column=1, padx=20)

# Area tab
ttk.Checkbutton(area_tab, text="Randomize Areas\n(only with items available in area)", variable=area_no_dupe_var).pack(anchor="w", pady=5)
ttk.Checkbutton(area_tab, text="Randomize Areas\n(randomize all chest,pot...)", variable=area_var, command=toggle_area_options).pack(anchor="w", pady=5)

area_frame = ttk.Frame(area_tab)
area_frame.pack(anchor="w", pady=5)

ttk.Label(area_frame, text="Min Gold:").grid(row=0, column=0, sticky="w", padx=10)
min_area_spinbox = ttk.Spinbox(area_frame, from_=1, to=500000, state='disabled',width=10)
min_area_spinbox.set(1)  # Default value
min_area_spinbox.grid(row=0, column=1, padx=20)

ttk.Label(area_frame, text="Max Gold:").grid(row=1, column=0, sticky="w", padx=10)
max_area_spinbox = ttk.Spinbox(area_frame, from_=1, to=500000, state='disabled', width=10)
max_area_spinbox.set(500000)  # Default value
max_area_spinbox.grid(row=1, column=1, padx=20)

ttk.Label(area_frame, text="Gold %:").grid(row=2, column=0, sticky="w", padx=10)
gold_spinbox = ttk.Spinbox(area_frame, from_=0, to=100, state='disabled', width=10)
gold_spinbox.set(0)  # Default value
gold_spinbox.grid(row=2, column=1, padx=20)

ttk.Label(area_frame, text="Items %:").grid(row=3, column=0, sticky="w", padx=10)
items_spinbox = ttk.Spinbox(area_frame, from_=0, to=100, state='disabled', width=10)
items_spinbox.set(0)  # Default value
items_spinbox.grid(row=3, column=1, padx=20)

ttk.Label(area_frame, text="Empty %:").grid(row=4, column=0, sticky="w", padx=10)
empty_spinbox = ttk.Spinbox(area_frame, from_=0, to=100, state='disabled', width=10)
empty_spinbox.set(0)  # Default value
empty_spinbox.grid(row=4, column=1, padx=20)

ttk.Checkbutton(area_tab, text="Randomize Shine Object \n(only with items available in the map)", variable=shine_no_dupe_var).pack(anchor="w", pady=5)
ttk.Checkbutton(area_tab, text="Randomize Shine Object\n(randomize all items)", variable=shine_var, command=toggle_shine_options).pack(anchor="w", pady=5)

shine_frame = ttk.Frame(area_tab)
shine_frame.pack(anchor="w", pady=5)

ttk.Label(shine_frame, text="Min Gold:").grid(row=0, column=0, sticky="w", padx=10)
min_shine_spinbox = ttk.Spinbox(shine_frame, from_=1, to=500000, state='disabled', width=10)
min_shine_spinbox.set(1)  # Default value
min_shine_spinbox.grid(row=0, column=1, padx=20)

ttk.Label(shine_frame, text="Max Gold:").grid(row=1, column=0, sticky="w", padx=10)
max_shine_spinbox = ttk.Spinbox(shine_frame, from_=1, to=500000, state='disabled', width=10)
max_shine_spinbox.set(500000)  # Default value
max_shine_spinbox.grid(row=1, column=1, padx=20)


# Other tab
ttk.Checkbutton(other_tab, text="Randomize Learning Skills", variable=skills_var).pack(anchor="w", pady=5)
ttk.Checkbutton(other_tab, text="Randomize Mini-Medals Rewards", variable=medals_var).pack(anchor="w", pady=5)
ttk.Checkbutton(other_tab, text="Randomize Start Bag Items", variable=other_var).pack(anchor="w", pady=5)
ttk.Checkbutton(other_tab, text="Randomize Monster Spawns", variable=monster_var).pack(anchor="w", pady=5)
ttk.Checkbutton(other_tab, text="Randomize Monster Drops", variable=monster_drop_var).pack(anchor="w", pady=5)


apply_button = ttk.Button(root, text="Randomize", command=process_selection, bootstyle="success")
apply_button.pack(pady=10)

def start():
    root.mainloop()
