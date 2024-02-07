import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from form_pdf import create_pdf
import os
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import black
from compress import compress_images
from pdf_to_images import pdf_to_images_mupdf


def select_folder(entry, entry2=None):
    folder_selected = filedialog.askdirectory(initialdir=os.getcwd())
    entry.set(folder_selected)
    if entry2 != None:
        result_folder = os.path.join(folder_selected, "compress_result")
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        entry2.set(result_folder)


def start_processing():
    # Извлекаем параметры
    folder = folder_path.get()
    save_folder = save_folder_path.get()
    try:
        width = float(width_entry.get())
        height = float(height_entry.get())
        border_width = float(border_width_entry.get())
        margin = float(margin_entry.get())
        # Проверяем параметры
        if not (0.1 <= width <= 200 and 0.1 <= height <= 200):
            raise ValueError("Размер карты должен быть в диапазоне от 1 до 200 мм.")
        if not (0 <= border_width <= 5):
            raise ValueError("Ширина разделительной полосы должна быть в диапазоне от 0 до 10 мм.")
        if not (0 <= margin <= 20):
            raise ValueError("Отступ от края листа должен быть в диапазоне от 0 до 20 мм.")
        # Вызываем вашу функцию обработки с параметрами
        create_pdf(folder, width, height, save_folder, 'create_pdf', border_width, margin)
    except ValueError as e:
        messagebox.showerror("Ошибка ввода", str(e))


app = tk.Tk()
app.title('Помощник РИ')
tabControl = ttk.Notebook(app)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

# Получаем текущий рабочий каталог
tabControl.add(tab1, text='Картиинки в PDF')
tabControl.add(tab2, text='Сжать картинки')
tabControl.add(tab3, text='Pdf на картинки')
tabControl.pack(expand=1, fill="both")

# Получаем текущий рабочий каталог
current_directory = os.getcwd()

folder_path = tk.StringVar(value=current_directory)
save_folder_path = tk.StringVar(value=current_directory)

# Вкладка 1
tk.Label(tab1, text="Путь до папки с изображениями:").grid(row=0, column=0)
tk.Entry(tab1, textvariable=folder_path, width=50).grid(row=0, column=1)
tk.Button(tab1, text="Выбрать", command=lambda: select_folder(folder_path)).grid(row=0, column=2)

tk.Label(tab1, text="Путь сохранения:").grid(row=1, column=0)
tk.Entry(tab1, textvariable=save_folder_path, width=50).grid(row=1, column=1)
tk.Button(tab1, text="Выбрать", command=lambda: select_folder(save_folder_path)).grid(row=1, column=2)

tk.Label(tab1, text="Итоговый размер карт в мм (ширина):").grid(row=2, column=0)
width_entry = tk.Entry(tab1)
width_entry.insert(0, "50")  # Значение по умолчанию для ширины
width_entry.grid(row=2, column=1)

tk.Label(tab1, text="Итоговый размер карт в мм (высота):").grid(row=3, column=0)
height_entry = tk.Entry(tab1)
height_entry.insert(0, "50")  # Значение по умолчанию для высоты
height_entry.grid(row=3, column=1)

tk.Label(tab1, text="Ширина разделительной сетки, мм (0-4.9):").grid(row=4, column=0)
border_width_entry = tk.Entry(tab1)
border_width_entry.insert(0, "1")  # Значение по умолчанию для ширины разделительной полосы
border_width_entry.grid(row=4, column=1)

tk.Label(tab1, text="Отступ от края мм (0-19.9):").grid(row=5, column=0)
margin_entry = tk.Entry(tab1)
margin_entry.insert(0, "5")  # Значение по умолчанию для отступа от края
margin_entry.grid(row=5, column=1)

# Кнопка запуска обработки
start_button = tk.Button(tab1, text="Пуск", command=start_processing)
start_button.grid(row=6, column=0, columnspan=3)


def create_compression_result_folder():
    result_folder = os.path.join(os.getcwd(), "compress_result")
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    return result_folder


def start_compression():
    source_folder = compress_folder_path.get()
    compression_level = compression_level_entry.get()
    target_folder = compress_save_folder_path.get()

    try:
        compression_level = int(compression_level)
        if not (1 <= compression_level <= 10):
            raise ValueError("Степень сжатия должна быть в диапазоне от 1 до 10.")
        # Здесь должна быть логика сжатия изображений
        compress_images(source_folder, target_folder, compression_level)
        messagebox.showinfo("Успех", "Сжатие изображений успешно завершено.")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))


# Вкладка 2: Сжатие изображений

compress_folder_path = tk.StringVar(value=os.getcwd())
compress_save_folder_path = tk.StringVar(value=create_compression_result_folder())

tk.Label(tab2, text="Путь до папки с изображениями:").grid(row=0, column=0)
tk.Entry(tab2, textvariable=compress_folder_path, width=50).grid(row=0, column=1)
tk.Button(tab2, text="Выбрать", command=lambda: select_folder(compress_folder_path, compress_save_folder_path)).grid(
    row=0, column=2)

tk.Label(tab2, text="Путь сохранения:").grid(row=1, column=0)
tk.Entry(tab2, textvariable=compress_save_folder_path, width=50).grid(row=1, column=1)
tk.Button(tab2, text="Выбрать", command=lambda: select_folder(compress_save_folder_path)).grid(row=1, column=2)

tk.Label(tab2, text="Степень сжатия изображений (1-10):").grid(row=2, column=0)
compression_level_entry = tk.Entry(tab2)
compression_level_entry.insert(0, "3")  # Значение по умолчанию для степени сжатия
compression_level_entry.grid(row=2, column=1)

tk.Button(tab2, text="Запустить сжатие", command=start_compression).grid(row=3, column=0, columnspan=3)


# Вкладка 3: Извлечь картинки из PDF

def select_pdf_file():
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_path.set(file_path)
        default_output_folder = os.path.join(os.path.dirname(file_path), "images_from_pdf")
        pdf_output_folder.set(default_output_folder)


def extract_images_from_pdf():
    # Заглушка для функции извлечения изображений
    start_page = int(start_page_entry.get())
    end_page = int(end_page_entry.get())
    step = int(step_entry.get())
    pdf_file = pdf_path.get()
    output_folder = pdf_output_folder.get()
    pdf_to_images_mupdf(pdf_path=pdf_file,output_folder=output_folder, first=start_page, last =end_page, step = step  )

    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    messagebox.showinfo("Успех",
                        f"Изображения из {pdf_file} успешно извлечены в {output_folder}.\nСтраницы с {start_page} по {end_page}, шаг {step}.")


pdf_path = tk.StringVar()
pdf_output_folder = tk.StringVar()

tk.Label(tab3, text="Путь до PDF файла:").grid(row=0, column=0)
tk.Entry(tab3, textvariable=pdf_path, width=50).grid(row=0, column=1)
tk.Button(tab3, text="Выбрать", command=select_pdf_file).grid(row=0, column=2)

tk.Label(tab3, text="Папка для сохранения изображений:").grid(row=1, column=0)
tk.Entry(tab3, textvariable=pdf_output_folder, width=50).grid(row=1, column=1)
tk.Button(tab3, text="Выбрать", command=lambda: select_folder(pdf_output_folder)).grid(row=1, column=2)

tk.Label(tab3, text="Страницы начиная с:").grid(row=2, column=0)
start_page_entry = tk.Entry(tab3)
start_page_entry.grid(row=2, column=1)
start_page_entry.insert(0, "1")

tk.Label(tab3, text="по: [-1 послед]").grid(row=3, column=0)
end_page_entry = tk.Entry(tab3)
end_page_entry.grid(row=3, column=1)
end_page_entry.insert(0, "-1")

tk.Label(tab3, text="каждая:").grid(row=4, column=0)
step_entry = tk.Entry(tab3)
step_entry.grid(row=4, column=1)
step_entry.insert(0, "1")

tk.Button(tab3, text="Извлечь изображения", command=extract_images_from_pdf).grid(row=5, column=0, columnspan=3)

app.mainloop()
