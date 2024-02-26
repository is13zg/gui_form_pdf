import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from form_pdf import create_pdf
import os
from compress import compress_images
from pdf_to_images import pdf_to_images_mupdf
from text_to_cards import place_text_on_image
from PIL import Image

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
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)

# Получаем текущий рабочий каталог
tabControl.add(tab1, text='Картиинки в PDF')
tabControl.add(tab2, text='Сжать картинки')
tabControl.add(tab3, text='Pdf на картинки')
tabControl.add(tab4, text='Текст на карточки')
tabControl.add(tab5, text='Повороты')
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
    pdf_to_images_mupdf(pdf_path=pdf_file, output_folder=output_folder, first=start_page, last=end_page, step=step)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    messagebox.showinfo("Успех",
                        f"Изображения из {pdf_file} успешно извлечены в {output_folder}.\nСтраницы с {start_page} по {end_page}, шаг {step}.")


pdf_path = tk.StringVar(value=os.getcwd())
pdf_output_folder = tk.StringVar(value=os.getcwd())

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


# Вкладка 4: Текст на карточки
def select_font_path():
    initial_dir = os.getcwd()  # Текущая директория приложения
    font_path.set(filedialog.askopenfilename(initialdir=initial_dir,
                                             filetypes=[("Font files", "*.ttf *.otf"), ("All files", "*.*")]))


def select_save_folder():
    initial_dir = os.getcwd()  # Текущая директория приложения
    save_folder_path.set(filedialog.askdirectory(initialdir=initial_dir))


def submit_data():
    # Здесь должна быть ваша логика для размещения текста на изображениях

    main_text = text_input.get("1.0", tk.END)
    ls = main_text.split("\n")
    colors = {"белый": "#ffffff", "черный": "#000000", "серый": "#C0C0C0", "красный": "#fe0000", "оранжевый": "#ff7513",
              "желтый": "#ffcc00", "зеленый": "#019934", "голубой": "#00FFFF", "синий": "#3401cc",
              "фиолетовый": "#990099", "коричневый": "#8B4513", "розовый": "#FFC0CB"}

    # Пример использования
    counter = 0
    for x in range(repeat_times.get()):
        for text_string in ls:
            counter += 1
            place_text_on_image((image_width.get(), image_height.get()), text_string, counter,
                                font_path=font_path.get(), initial_font_size=max_font_size.get(),
                                save_path=save_folder_path.get(), bg_color=colors[bg_color_combobox.get()],
                                text_color=colors[text_color_combobox.get()], name_prefix=name_prefix.get())
    messagebox.showinfo("Успех")


def paste_from_clipboard():
    try:
        text = app.clipboard_get()
        text_input.insert(tk.INSERT, text)
    except tk.TclError:
        messagebox.showwarning("Warning", "Nothing to paste from clipboard")


def copy_to_clipboard():
    app.clipboard_clear()  # Очистка текущего содержимого буфера обмена
    text = text_input.get("1.0", tk.END)  # Получение текста из текстового поля
    app.clipboard_append(text)  # Добавление текста в буфер обмена




# Основное окно


font_path = tk.StringVar(value=os.getcwd())
max_font_size = tk.IntVar(value=200)
image_width = tk.IntVar(value=900)
image_height = tk.IntVar(value=600)
save_folder_path = tk.StringVar(value=os.getcwd())
repeat_times = tk.IntVar(value=1)
name_prefix = tk.StringVar(value="name")
colors = ["белый", "черный", "серый", "красный", "оранжевый", "желтый", "зеленый", "голубой", "синий", "фиолетовый",
          "коричневый", "розовый"]

# Элементы интерфейса для вкладки\
tk.Label(tab3, text="Путь до PDF файла:").grid(row=0, column=0)
tk.Entry(tab3, textvariable=pdf_path).grid(row=0, column=1)
tk.Button(tab3, text="Выбрать", command=select_pdf_file).grid(row=0, column=2)

tk.Label(tab4, text="Путь до шрифта:").grid(row=0, column=0)
ttk.Entry(tab4, textvariable=font_path).grid(row=0, column=1, sticky="ew", columnspan=4)
ttk.Button(tab4, text="Выбрать", command=select_font_path).grid(row=0, column=5, sticky="ew")

ttk.Label(tab4, text="Макс. размер шрифта:").grid(row=1, column=4, sticky="w")
ttk.Entry(tab4, textvariable=max_font_size).grid(row=1, column=5, sticky="ew", )

ttk.Label(tab4, text="Ширина изоб.:").grid(row=1, column=0, sticky="w")
ttk.Entry(tab4, textvariable=image_width).grid(row=1, column=1, sticky="ew")

ttk.Label(tab4, text="Высота изоб.").grid(row=1, column=2, sticky="w")
ttk.Entry(tab4, textvariable=image_height).grid(row=1, column=3, sticky="ew")

tk.Label(tab4, text="Путь сохранения:").grid(row=2, column=0)
ttk.Entry(tab4, textvariable=save_folder_path).grid(row=2, column=1, sticky="ew", columnspan=4)
ttk.Button(tab4, text="Выбрать", command=select_save_folder).grid(row=2, column=5, sticky="ew")

ttk.Label(tab4, text="Число копий:").grid(row=3, column=0, sticky="w")
ttk.Entry(tab4, textvariable=repeat_times).grid(row=3, column=1, sticky="ew")

ttk.Label(tab4, text="Цвет текста:").grid(row=3, column=2, sticky="w")
text_color_combobox = ttk.Combobox(tab4, values=colors, state="readonly")
text_color_combobox.grid(row=3, column=3, sticky="ew")
text_color_combobox.set("черный")

ttk.Label(tab4, text="Цвет фона:").grid(row=3, column=4, sticky="w")
bg_color_combobox = ttk.Combobox(tab4, values=colors, state="readonly")
bg_color_combobox.grid(row=3, column=5, sticky="ew")
bg_color_combobox.set("белый")

text_input = tk.Text(tab4, height=10)
text_input.grid(row=4, column=0, sticky="ew", columnspan=6)

ttk.Button(tab4, text="Вставить", command=paste_from_clipboard).grid(row=5, column=0, sticky="ew")
ttk.Button(tab4, text="Копировать", command=copy_to_clipboard).grid(row=5, column=1, sticky="ew")

ttk.Label(tab4, text="Префикс результата:").grid(row=5, column=2, sticky="w")
ttk.Entry(tab4, textvariable=name_prefix).grid(row=5, column=3, sticky="ew")

ttk.Button(tab4, text="Пуск", command=submit_data).grid(row=5, column=4, sticky="ew", columnspan=2)

# Вкладка 5: Повороты

def rotate_images(folder_path, operation):
    try:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(folder_path, filename)
                with Image.open(image_path) as img:
                    if operation == '90':
                        img_rotated = img.rotate(90, expand=True)
                    elif operation == '180':
                        img_rotated = img.rotate(180, expand=True)
                    elif operation == '270':
                        img_rotated = img.rotate(270, expand=True)
                    elif operation == 'отр. по гориз.':
                        img_rotated = img.transpose(Image.FLIP_LEFT_RIGHT)
                    elif operation == 'отр. по верт.':
                        img_rotated = img.transpose(Image.FLIP_TOP_BOTTOM)

                    img_rotated.save(image_path)
        messagebox.showinfo("Готово", "Операция успешно выполнена!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


def rot_select_folder():
    rot_folder_path = filedialog.askdirectory()
    if rot_folder_path:
        rot_folder_entry.delete(0, tk.END)
        rot_folder_entry.insert(0, rot_folder_path)


def start_operation():
    rot_folder_path = rot_folder_entry.get()
    operation = operation_var.get()
    if not rot_folder_path:
        messagebox.showwarning("Внимание", "Пожалуйста, выберите папку.")
        return
    rotate_images(rot_folder_path, operation)



rot_folder_entry = ttk.Entry(tab5, width=50)
tk.Label(tab5, text="Путь изображений:").grid(row=0, column=0)
rot_folder_entry.grid(row=0, column=1, sticky="ew",columnspan=3)

rot__button = ttk.Button(tab5, text="Выбрать папку", command=rot_select_folder)
rot__button.grid(row=0, column=4)

operation_var = tk.StringVar()
operation_var.set("90")  # Значение по умолчанию

options = ["90", "180", "270", "отр. по гориз.", "отр. по верт."]
operation_menu = ttk.OptionMenu(tab5, operation_var, *options)
operation_menu.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

start_button = ttk.Button(tab5, text="Пуск", command=start_operation)
start_button.grid(row=1, column=1, padx=10, pady=20)

# Установка минимальной ширины колонки, чтобы обеспечить достаточное место для элементов
tab5.grid_columnconfigure(0, weight=1)



app.mainloop()
