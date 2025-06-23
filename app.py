# Required: pip install tk sqlite3 (built-in)
import tkinter as tk
from tkinter import messagebox, filedialog, ttk, PhotoImage
import sqlite3
import os
from PIL import Image, ImageTk
import datetime

# Database Setup
def init_db():
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        department TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        image_blob BLOB
    )
    """)
    conn.commit()
    conn.close()
    # إنشاء مجلد الصور إذا لم يكن موجودًا
    if not os.path.exists("images"):
        os.makedirs("images")

def save_data():
    """Ensure all data is properly saved to database"""
    try:
        conn = sqlite3.connect("employees.db")
        conn.commit()
        conn.close()
        print("Data saved successfully!")
    except Exception as e:
        print(f"Error saving data: {e}")

# متغير لتخزين مسار الصورة المؤقت
selected_image_path = None

def choose_image():
    global selected_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        selected_image_path = file_path
        image_label.config(text=os.path.basename(file_path))
    else:
        selected_image_path = None
        image_label.config(text="No image selected")

# Core Functions - Employees
def add_employee():
    name = name_entry.get()
    email = email_entry.get()
    dept = dept_entry.get()
    if not (name and email and dept):
        messagebox.showwarning("Input error", "All fields are required.")
        return
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO employees (name, email, department) VALUES (?, ?, ?)", (name, email, dept))
    conn.commit()
    conn.close()
    save_data()  # Ensure data is saved
    show_employees()
    clear_form()

def show_employees():
    for row in employee_listbox.get_children():
        employee_listbox.delete(row)
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    for row in cur.fetchall():
        employee_listbox.insert("", tk.END, values=row)
    conn.close()

def delete_employee():
    selected = employee_listbox.selection()
    if not selected:
        return
    item = employee_listbox.item(selected[0])
    emp_id = item['values'][0]
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()
    save_data()  # Ensure data is saved
    show_employees()

def clear_form():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)

# Core Functions - Products
def add_product():
    global selected_image_path
    name = product_name_entry.get()
    category = product_category_combobox.get()
    try:
        price = float(product_price_entry.get())
        quantity = int(product_quantity_entry.get())
    except ValueError:
        messagebox.showwarning("Input error", "Price and quantity must be numbers.")
        return
    if not (name and category):
        messagebox.showwarning("Input error", "All fields are required.")
        return
    image_blob = None
    if selected_image_path:
        try:
            with open(selected_image_path, 'rb') as f:
                image_blob = f.read()
        except Exception as e:
            messagebox.showwarning("Image error", f"فشل قراءة الصورة: {e}")
            image_blob = None
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, category, price, quantity, image_blob) VALUES (?, ?, ?, ?, ?)", (name, category, price, quantity, image_blob))
    conn.commit()
    conn.close()
    save_data()  # Ensure data is saved
    show_products()
    clear_product_form()
    image_label.config(text="No image selected")
    selected_image_path = None

def show_products():
    for row in product_listbox.get_children():
        product_listbox.delete(row)
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, price, quantity FROM products")
    for row in cur.fetchall():
        product_listbox.insert("", tk.END, values=row)
    conn.close()

def delete_product():
    selected = product_listbox.selection()
    if not selected:
        return
    item = product_listbox.item(selected[0])
    product_id = item['values'][0]
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    save_data()  # Ensure data is saved
    show_products()

def clear_product_form():
    product_name_entry.delete(0, tk.END)
    product_category_combobox.set("")
    product_price_entry.delete(0, tk.END)
    product_quantity_entry.delete(0, tk.END)

# --- Product Search ---
def search_products():
    query = search_entry.get().strip().lower()
    for row in product_listbox.get_children():
        product_listbox.delete(row)
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, price, quantity FROM products")
    for row in cur.fetchall():
        if (query in str(row[1]).lower() or query in str(row[2]).lower() or query in str(row[3]).lower() or query in str(row[4]).lower()):
            product_listbox.insert("", tk.END, values=row)
    conn.close()

# --- Category Management ---
def add_category():
    name = category_name_entry.get().strip()
    if not name:
        messagebox.showwarning("خطأ", "يرجى إدخال اسم الفئة.")
        return
    try:
        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        save_data()  # Ensure data is saved
        show_categories()
        update_category_combobox()
        category_name_entry.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showwarning("خطأ", "اسم الفئة موجود بالفعل.")

def show_categories():
    for row in category_listbox.get_children():
        category_listbox.delete(row)
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories")
    for row in cur.fetchall():
        category_listbox.insert("", tk.END, values=row)
    conn.close()

def delete_category():
    selected = category_listbox.selection()
    if not selected:
        return
    item = category_listbox.item(selected[0])
    cat_id = item['values'][0]
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM categories WHERE id=?", (cat_id,))
    conn.commit()
    conn.close()
    save_data()  # Ensure data is saved
    show_categories()
    update_category_combobox()

def update_category_combobox():
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM categories")
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    product_category_combobox['values'] = categories
    if categories:
        product_category_combobox.current(0)
    else:
        product_category_combobox.set("")

# GUI Setup
init_db()
root = tk.Tk()
root.title("Employee & Product Management System")
root.geometry("1200x800")
root.configure(bg="#eaf0fa")  # خلفية هادئة

# Center the window on screen
def center_window():
    """Center the window on the screen"""
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

# Create main container for centering
main_container = tk.Frame(root, bg="#eaf0fa")
main_container.pack(expand=True, fill="both", padx=20, pady=20)

# Create canvas for scrolling
main_canvas = tk.Canvas(main_container, bg="#eaf0fa", highlightthickness=0)
main_canvas.pack(side="left", fill="both", expand=True)
main_scrollbar = tk.Scrollbar(main_container, orient="vertical", command=main_canvas.yview)
main_scrollbar.pack(side="right", fill="y")
main_canvas.configure(yscrollcommand=main_scrollbar.set)

# Create content frame with proper centering
content_frame = tk.Frame(main_canvas, bg="#eaf0fa")
main_canvas.create_window((0, 0), window=content_frame, anchor="nw")

def on_configure(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))
content_frame.bind("<Configure>", on_configure)

# Configure grid weights for centering
content_frame.grid_columnconfigure(0, weight=1)
content_frame.grid_columnconfigure(1, weight=1)
content_frame.grid_columnconfigure(2, weight=1)
content_frame.grid_columnconfigure(3, weight=1)

# Header section - centered
header_frame = tk.Frame(content_frame, bg="#eaf0fa")
header_frame.grid(row=0, column=0, columnspan=4, pady=(0, 20), sticky="ew")

try:
    logo_img = Image.open("logo.png")
    logo_img = logo_img.resize((60, 60))
    logo_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header_frame, image=logo_tk, bg="#eaf0fa")
    logo_label.image = logo_tk
    logo_label.pack(side="left", padx=(0, 10))
except Exception:
    logo_label = tk.Label(header_frame, text="🛰️", font=("Arial", 36), bg="#eaf0fa")
    logo_label.pack(side="left", padx=(0, 10))

main_title = tk.Label(header_frame, text="Employee & Product Management System", font=("Arial", 28, "bold"), fg="#d32f2f", bg="#eaf0fa")
main_title.pack(side="left")

# Employee Form - centered
emp_frame = tk.LabelFrame(content_frame, text="إضافة موظف", padx=15, pady=15, font=("Arial", 13, "bold"), bg="#f5f7fa", fg="#1976d2")
emp_frame.grid(row=1, column=0, columnspan=2, padx=(0, 10), pady=10, sticky="nsew")

emp_label_style = {"font": ("Arial", 12), "bg": "#f5f7fa"}
emp_entry_style = {"font": ("Arial", 12), "bd": 1, "relief": "solid", "bg": "#fff"}

name_label = tk.Label(emp_frame, text="Employee Name", **emp_label_style)
name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
name_entry = tk.Entry(emp_frame, **emp_entry_style)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

email_label = tk.Label(emp_frame, text="Email", **emp_label_style)
email_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
email_entry = tk.Entry(emp_frame, **emp_entry_style)
email_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

dept_label = tk.Label(emp_frame, text="Department", **emp_label_style)
dept_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
dept_entry = tk.Entry(emp_frame, **emp_entry_style)
dept_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Configure employee frame grid weights
emp_frame.grid_columnconfigure(1, weight=1)

add_btn = tk.Button(emp_frame, text="Add Employee", command=add_employee, font=("Arial", 12, "bold"), bg="#388e3c", fg="#fff", activebackground="#2e7d32", activeforeground="#fff", bd=0, relief="ridge", cursor="hand2")
add_btn.grid(row=3, column=0, columnspan=2, pady=15, ipadx=20, sticky="ew")

# Employee Table - centered
employee_table_frame = tk.LabelFrame(content_frame, text="قائمة الموظفين", font=("Arial", 13, "bold"), bg="#f5f7fa", fg="#1976d2")
employee_table_frame.grid(row=2, column=0, columnspan=2, padx=(0, 10), pady=10, sticky="nsew")

employee_columns = ("ID", "Name", "Email", "Department")
employee_listbox = ttk.Treeview(employee_table_frame, columns=employee_columns, show='headings', height=7)
for col in employee_columns:
    employee_listbox.heading(col, text=col)
    employee_listbox.column(col, width=110)
employee_listbox.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")

# Scrollbar for employee table
employee_scrollbar = tk.Scrollbar(employee_table_frame, orient="vertical", command=employee_listbox.yview)
employee_listbox.configure(yscrollcommand=employee_scrollbar.set)
employee_scrollbar.grid(row=0, column=1, sticky="ns")

# Configure employee table frame grid weights
employee_table_frame.grid_columnconfigure(0, weight=1)
employee_table_frame.grid_rowconfigure(0, weight=1)

style = ttk.Style()
style.configure("Treeview", font=("Arial", 11), rowheight=28, background="#fff", fieldbackground="#fff")
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#1976d2", foreground="#000")

# Employee Delete Button
delete_btn = tk.Button(employee_table_frame, text="Delete Employee", command=delete_employee, font=("Arial", 11, "bold"), bg="#d32f2f", fg="#fff", activebackground="#b71c1c", activeforeground="#fff", bd=0, relief="ridge", cursor="hand2")
delete_btn.grid(row=1, column=0, columnspan=2, pady=5, ipadx=10, sticky="ew")

# Product Form - centered
prod_frame = tk.LabelFrame(content_frame, text="إضافة منتج", padx=15, pady=15, font=("Arial", 13, "bold"), bg="#f5f7fa", fg="#1976d2")
prod_frame.grid(row=1, column=2, columnspan=2, padx=(10, 0), pady=10, sticky="nsew")

prod_label_style = {"font": ("Arial", 12), "bg": "#f5f7fa"}
prod_entry_style = {"font": ("Arial", 12), "bd": 1, "relief": "solid", "bg": "#fff"}

product_name_label = tk.Label(prod_frame, text="Product Name", **prod_label_style)
product_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
product_name_entry = tk.Entry(prod_frame, **prod_entry_style)
product_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

product_category_label = tk.Label(prod_frame, text="Category", **prod_label_style)
product_category_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
product_category_combobox = ttk.Combobox(prod_frame, state="readonly", font=("Arial", 11))
product_category_combobox.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

product_price_label = tk.Label(prod_frame, text="Price", **prod_label_style)
product_price_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
product_price_entry = tk.Entry(prod_frame, **prod_entry_style)
product_price_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

product_quantity_label = tk.Label(prod_frame, text="الكمية", **prod_label_style)
product_quantity_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
product_quantity_entry = tk.Entry(prod_frame, **prod_entry_style)
product_quantity_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

image_btn = tk.Button(prod_frame, text="اختيار صورة", command=choose_image, font=("Arial", 11), bg="#1976d2", fg="#fff", activebackground="#1565c0", activeforeground="#fff", bd=0, relief="ridge", cursor="hand2")
image_btn.grid(row=2, column=0, pady=5, ipadx=10, sticky="w")
image_label = tk.Label(prod_frame, text="No image selected", font=("Arial", 10), bg="#f5f7fa")
image_label.grid(row=2, column=1, pady=5, sticky="w")

# Configure product frame grid weights
prod_frame.grid_columnconfigure(1, weight=1)
prod_frame.grid_columnconfigure(3, weight=1)

add_product_btn = tk.Button(prod_frame, text="Add Product", command=add_product, font=("Arial", 12, "bold"), bg="#388e3c", fg="#fff", activebackground="#2e7d32", activeforeground="#fff", bd=0, relief="ridge", cursor="hand2")
add_product_btn.grid(row=3, column=0, columnspan=4, pady=15, ipadx=20, sticky="ew")

# Product Table - centered
product_table_frame = tk.LabelFrame(content_frame, text="قائمة المنتجات", font=("Arial", 13, "bold"), bg="#f5f7fa", fg="#1976d2")
product_table_frame.grid(row=2, column=2, columnspan=2, padx=(10, 0), pady=10, sticky="nsew")

# Search section
search_frame = tk.Frame(product_table_frame, bg="#f5f7fa")
search_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

search_entry = tk.Entry(search_frame, font=("Arial", 12), width=18)
search_entry.pack(side="left", padx=(5, 5))
search_btn = tk.Button(search_frame, text="بحث", command=search_products, font=("Arial", 11, "bold"), bg="#1976d2", fg="#fff", bd=0, relief="ridge", cursor="hand2")
search_btn.pack(side="left", padx=(0, 5))

product_columns = ("ID", "Name", "Category", "Price", "Quantity")
product_listbox = ttk.Treeview(product_table_frame, columns=product_columns, show='headings', height=7)
for col in product_columns:
    product_listbox.heading(col, text=col)
    product_listbox.column(col, width=110)
product_listbox.grid(row=1, column=0, pady=5, padx=5, sticky="nsew")

# Scrollbar for product table
product_scrollbar = tk.Scrollbar(product_table_frame, orient="vertical", command=product_listbox.yview)
product_listbox.configure(yscrollcommand=product_scrollbar.set)
product_scrollbar.grid(row=1, column=1, sticky="ns")

# Configure product table frame grid weights
product_table_frame.grid_columnconfigure(0, weight=1)
product_table_frame.grid_rowconfigure(1, weight=1)

# Product Delete Button
delete_product_btn = tk.Button(product_table_frame, text="Delete Product", command=delete_product, font=("Arial", 11, "bold"), bg="#d32f2f", fg="#fff", activebackground="#b71c1c", activeforeground="#fff", bd=0, relief="ridge", cursor="hand2")
delete_product_btn.grid(row=2, column=0, columnspan=2, pady=5, ipadx=10, sticky="ew")

# عند تحديد منتج، عرض صورته
product_image_panel = None

def on_product_select(event):
    selected = product_listbox.selection()
    if not selected:
        return
    item = product_listbox.item(selected[0])
    product_id = item['values'][0]
    show_product_image_popup(product_id)

def show_product_image_popup(product_id):
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("SELECT name, image_blob FROM products WHERE id=?", (product_id,))
    row = cur.fetchone()
    conn.close()
    if row and row[1]:
        import io
        img = Image.open(io.BytesIO(row[1]))
        img = img.resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        popup = tk.Toplevel(root)
        popup.title(f"صورة المنتج: {row[0]}")
        popup.geometry("340x360")
        popup.configure(bg="#eaf0fa")
        label = tk.Label(popup, text=row[0], font=("Arial", 14, "bold"), bg="#eaf0fa")
        label.pack(pady=10)
        img_label = tk.Label(popup, image=img_tk, bg="#eaf0fa")
        img_label.img_tk = img_tk
        img_label.pack(pady=10)
    else:
        messagebox.showinfo("لا توجد صورة", "لا توجد صورة محفوظة لهذا المنتج.")

# --- Category UI ---
category_frame = tk.LabelFrame(content_frame, text="إدارة الفئات", padx=15, pady=15, font=("Arial", 13, "bold"), bg="#f5f7fa", fg="#1976d2")
category_frame.grid(row=3, column=0, columnspan=4, pady=20, sticky="ew")

# Category input section
category_input_frame = tk.Frame(category_frame, bg="#f5f7fa")
category_input_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")

category_name_entry = tk.Entry(category_input_frame, font=("Arial", 12), bd=1, relief="solid", bg="#fff")
category_name_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)

add_category_btn = tk.Button(category_input_frame, text="إضافة فئة", command=add_category, font=("Arial", 11, "bold"), bg="#388e3c", fg="#fff", activebackground="#2e7d32", activeforeground="#fff", bd=0, relief="ridge", cursor="hand2")
add_category_btn.pack(side="left", padx=(0, 10))

# Configure category input frame
category_input_frame.grid_columnconfigure(0, weight=1)

category_listbox = ttk.Treeview(category_frame, columns=("ID", "Name"), show='headings', height=4)
category_listbox.heading("ID", text="ID")
category_listbox.heading("Name", text="اسم الفئة")
category_listbox.column("ID", width=40)
category_listbox.column("Name", width=200)
category_listbox.grid(row=1, column=0, pady=5, padx=5, sticky="nsew")

# Scrollbar for category table
category_scrollbar = tk.Scrollbar(category_frame, orient="vertical", command=category_listbox.yview)
category_listbox.configure(yscrollcommand=category_scrollbar.set)
category_scrollbar.grid(row=1, column=1, sticky="ns")

# Configure category frame grid weights
category_frame.grid_columnconfigure(0, weight=1)
category_frame.grid_rowconfigure(1, weight=1)

delete_category_btn = tk.Button(category_frame, text="حذف الفئة", command=delete_category, font=("Arial", 11, "bold"), bg="#d32f2f", fg="#fff", activebackground="#b71c1c", activeforeground="#fff", bd=0, relief="ridge", cursor="hand2")
delete_category_btn.grid(row=2, column=0, columnspan=2, pady=5, ipadx=10, sticky="ew")

# بعد تعريف main_canvas:
def _on_mousewheel(event):
    if event.keysym == 'Down':
        main_canvas.yview_scroll(1, 'units')
    elif event.keysym == 'Up':
        main_canvas.yview_scroll(-1, 'units')

main_canvas.bind_all('<Down>', _on_mousewheel)
main_canvas.bind_all('<Up>', _on_mousewheel)

# اربط النقر المزدوج:
product_listbox.bind("<Double-1>", on_product_select)

# Handle window close event to ensure data is saved
def on_closing():
    """Handle application closing"""
    try:
        save_data()
        print("Application closing - data saved successfully!")
    except Exception as e:
        print(f"Error saving data on close: {e}")
    finally:
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Load initial data BEFORE starting the mainloop
print("Loading saved data...")
show_categories()
update_category_combobox()
show_employees()
show_products()
print("Data loaded successfully!")

# Center the window
center_window()

# Add automatic data refresh every 30 seconds to ensure data stays current
def auto_refresh_data():
    """Automatically refresh data every 30 seconds"""
    try:
        show_categories()
        update_category_combobox()
        show_employees()
        show_products()
    except Exception as e:
        print(f"Auto-refresh error: {e}")
    finally:
        # Schedule next refresh in 30 seconds
        root.after(30000, auto_refresh_data)

# Start auto-refresh
root.after(30000, auto_refresh_data)

root.mainloop()
