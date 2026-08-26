import tkinter as tk
import json #imports the json tab.
import os
from tkinter import messagebox
from metallicCharacter import elementChange #imports the metallic character class.


#data


def load_elements(file_name): # Load elements from a JSON file
    if not os.path.exists(file_name):
        return []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('elements', [])
    except Exception as e:
        print(f"Error: {e}")
        return []


#state
selected_objects = []
selected_amounts = []   
current_el = None


#functions


COLOR_MAP = { #has colors for each type of element
    "transition metal": "#ADD8E6", "alkali metal": "#FF6B6B",
    "alkaline earth metal": "#FFAD60", "metalloid": "#FFEEAD",
    "lanthanide": "#96CEB4", "actinide": "#D4A5A5",
    "noble gas": "#D291BC", "reactive nonmetal": "#90EE90",
    "post-transition metal": "#D8BFD8", "unknown": "#D3D3D3"
}


def update_display(): # Show the elements in the bottom middle
    if not selected_objects:
        selection_label.config(text="No elements selected")
        return
   
    # Formats the list like: H(2)  O(1)
    txt = ""
    for i in range(len(selected_objects)):
        txt += f"{selected_objects[i]['Symbol']}({selected_amounts[i]})  "
    selection_label.config(text=txt)


def add_element(): # Add the current element to the selected list
    if current_el is None: return
   
    found = False
    for i in range(len(selected_objects)):
        if selected_objects[i]["Symbol"] == current_el["Symbol"]:
            selected_amounts[i] += 1
            found = True
            break
    if not found:
        selected_objects.append(current_el)
        selected_amounts.append(1)
    update_display()


def remove_element(): # Remove the current element from the selected list
    if current_el is None: return
   
    for i in range(len(selected_objects)):
        if selected_objects[i]["Symbol"] == current_el["Symbol"]: # if the element is found in the list, remove it
            selected_amounts[i] -= 1
            if selected_amounts[i] <= 0:
                selected_objects.pop(i)
                selected_amounts.pop(i)
            break
    update_display() #updates display after removing it


def combine_elements():
    if not selected_objects: return
   
    mass = 0 # starting mass at 0 as requested
    mass = eC.massCalculate(selected_objects, selected_amounts)
   
    messagebox.showinfo("Mass Result", f"Total Combined Mass: {mass:.3f} u") # show the combined mass in a messagebox
   
    # Clear the lists
    selected_objects.clear()
    selected_amounts.clear() #clears the amount and objects after the messagebox is shown
    update_display()


def show_info(element): # information on each element when clicked
    global current_el
    current_el = element # set it as current, making it show
   
    for widget in info_content.winfo_children():
        widget.destroy()
       
    tk.Label(info_content, text=element["Name"], font=("Arial", 18, "bold"), bg=COLOR_MAP.get(element["Metallic Character"], "#FFFFFF")).pack(pady=10)
   
    details = [
        ("Symbol", element["Symbol"]),
        ("Atomic Number", element["Atomic Number"]),
        ("Atomic Mass", f"{element['Atomic Mass']} u"),
        ("Type", element.get("Metallic Character", "Unknown"))
    ]
   
    for label, val in details:
        row = tk.Frame(info_content, bg=COLOR_MAP.get(element['Metallic Character'], '#FFFFFF'))
        row.pack(fill="x", padx=10, pady=2)
        tk.Label(row, text=f"{label}:", font=("Arial", 10, "bold"), bg=COLOR_MAP.get(element['Metallic Character'], '#FFFFFF')).pack(side="left")
        tk.Label(row, text=f" {val}", font=("Arial", 10), bg=COLOR_MAP.get(element['Metallic Character'], '#FFFFFF')).pack(side="left")
        info_content.configure(bg=COLOR_MAP.get(element['Metallic Character'], '#FFFFFF'))


elements = load_elements("elements.json") # loads the elements from the json file.
eC = elementChange()
eC.give_Metallic_Character(elements)


root = tk.Tk()
root.title("Periodic Table")
root.geometry("14000x600")


main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill="both", expand=True)




table_frame = tk.Frame(main_frame)
table_frame.pack(side="left", fill="both", expand=True)




right_panel = tk.Frame(main_frame, width=300)
right_panel.pack(side="right", fill="y", padx=10)


# Information Panel
info_panel = tk.LabelFrame(right_panel, text="Information", height=300)
info_panel.pack(fill="x", pady=(0, 10))
info_panel.pack_propagate(False)
info_content = tk.Frame(info_panel, bg="#FFFFFF")
info_content.pack(fill="both", expand=True)
#making the information box wider
info_panel.config(width=280)


# Controls (Replacing Calculator)
tk.Button(right_panel, text="Add Element", font=("Arial", 11), height=2, command=add_element).pack(fill="x", pady=2)
tk.Button(right_panel, text="Remove Element", font=("Arial", 11), height=2, command=remove_element).pack(fill="x", pady=2)
#combine button
combine_btn = tk.Button(right_panel, text="Combine Elements", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2, command=combine_elements)
combine_btn.pack(side="bottom", fill="x", pady=20)




# This sits right below the table frame in the main window
selection_label = tk.Label(root, text="No elements selected", font=("Arial", 16, "bold"), pady=20)
selection_label.pack(side="bottom")


placedL = False
gapButton = tk.Button(table_frame, text=" ", width=5, height=2, state="disabled", relief="flat", font=("Arial", 8, "bold"))
LgapButton = tk.Button(table_frame, text=" ", width=5, height=2, state="disabled", relief="flat", bg = COLOR_MAP.get("lanthanide", "#FFFFFF"),  font=("Arial", 8, "bold"))
AgapButton = tk.Button(table_frame, text=" ", width=5, height=2, state="disabled", relief="flat", bg = COLOR_MAP.get("actinide", "#FFFFFF"),  font=("Arial", 8, "bold"))


for i in range(1, 19): # Create group labels 1 to 18
    tk.Label(table_frame, text=str(i), font=("Arial", 10, "bold")).grid(row=0, column=i + 1, padx=1, pady=1)


for i in range(1, 8): # Create period labels 1 to 7 but doesnt pass lanthanide and actinide
    tk.Label(table_frame, text=str(i), font=("Arial", 10, "bold")).grid(row=i + 1, column=0, padx=1, pady=1)




for el in elements: # Loop through each element and create a button for it
    bg_color = COLOR_MAP.get(el["Metallic Character"], "#FFFFFF")
   
    btn = tk.Button(
        table_frame,
        text=f"{el['Symbol']}\n {el['Atomic Number']}", # \n is to make the atomic number appear below the symbol
        width=5, height=2, bg=bg_color,
        font=("Arial", 8, "bold"),
        command=lambda e=el: show_info(e)
    )
    if el["Metallic Character"] == "lanthanide": #special case for lanthanides and actinides.
        if not placedL:
            gapButton.grid(row= 8 + 1, column=3 + 1, padx=1, pady=1)
            LgapButton.grid(row= 6 + 1, column=3 + 1, padx=1, pady=1)
            AgapButton.grid(row= 7 + 1, column=3 + 1, padx=1, pady=1)
            placedL = True
        btn.grid(row= 9 + 1, column=el["Group"] + 1, padx=1, pady=1)
    elif el["Metallic Character"] == "actinide":
        btn.grid(row= 10 + 1, column=el["Group"] + 1, padx=1, pady=1)
    else:
        btn.grid(row=el["Period"] + 1, column=el["Group"] + 1, padx=1, pady=1)


root.mainloop()

