import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from form_pdf import create_pdf
import os
from image_hadler import image_handler
from pdf_to_images import pdf_to_images_mupdf
from text_to_cards import place_text_on_image
from images_into_cards import resize_and_orient_images


# расстанока картинок в pdf
def start_processing():
    # Извлекаем параметры
    folder = source_folder_path.get()
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
        create_pdf(folder, width, height, save_folder, 'create_pdf', border_width, margin,
                   max_separation=max_sep_checkbox.get())
        messagebox.showinfo("Успех", "Создание PDF успешно завершено.")
    except Exception as e:
        messagebox.showerror("Ошибка ввода", str(e))


app = tk.Tk()
app.title('Помощник РИ')
tabControl = ttk.Notebook(app)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
# tab5 = ttk.Frame(tabControl)
tab6 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Картиинки в PDF')
tabControl.add(tab2, text='Обработка изображений')
tabControl.add(tab3, text='Pdf на картинки')
tabControl.add(tab4, text='Текст на карточки')
# tabControl.add(tab5, text='Повороты')
tabControl.add(tab6, text='Вписать картинки')
tabControl.pack(expand=1, fill="both")

# Устанавливаем текущую директори в качестве исходнй
source_folder_path = tk.StringVar(value=os.getcwd())
save_folder_path = tk.StringVar(value=os.getcwd())

# Вкладка 1
# tk.Label(tab1, text="Путь до папки с изображениями:").grid(row=0, column=0)
# tk.Entry(tab1, textvariable=folder_path, width=50).grid(row=0, column=1)
# tk.Button(tab1, text="Выбрать", command=lambda: select_folder(folder_path)).grid(row=0, column=2)

# tk.Label(tab1, text="Путь сохранения по умолачнию ПУТЬ_ИСТОЧНИКА/compress_result").grid(row=1, column=0)
# tk.Entry(tab1, textvariable=save_folder_path, width=50).grid(row=1, column=1)
# tk.Button(tab1, text="Выбрать", command=lambda: select_folder(save_folder_path)).grid(row=1, column=2)

tk.Label(tab1, text="Итоговый размер карт в мм (ширина):").grid(row=0, column=0, sticky="w")
width_entry = tk.Entry(tab1)
width_entry.insert(0, "50")
width_entry.grid(row=0, column=1, sticky="ew")

tk.Label(tab1, text="Итоговый размер карт в мм (высота):").grid(row=1, column=0, sticky="w")
height_entry = tk.Entry(tab1)
height_entry.insert(0, "50")
height_entry.grid(row=1, column=1, sticky="ew")

tk.Label(tab1, text="Ширина разделительной сетки, мм (0-4.9):").grid(row=2, column=0, sticky="w")
border_width_entry = tk.Entry(tab1)
border_width_entry.insert(0, "1")
border_width_entry.grid(row=2, column=1, sticky="ew")

tk.Label(tab1, text="Отступ от края мм (0-19.9):").grid(row=3, column=0, sticky="w")
margin_entry = tk.Entry(tab1)
margin_entry.insert(0, "5")
margin_entry.grid(row=3, column=1, sticky="ew")

tk.Label(tab1, text="Равномерный макс. отступ").grid(row=4, column=0, sticky="w")
max_sep_checkbox = tk.BooleanVar()
max_sep_checkbutton = tk.Checkbutton(tab1, variable=max_sep_checkbox)
max_sep_checkbox.set(True)
max_sep_checkbutton.grid(row=4, column=1, sticky="ew")


def select_source_folder(entry):
    folder_selected = filedialog.askdirectory(initialdir=entry.get())
    if folder_selected != "":
        entry.set(folder_selected)
    tab_name = tabControl.tab(tabControl.index("current"), "text")
    end_path = ""
    if tab_name == 'Картиинки в PDF':
        end_path = ""
    elif tab_name == "Обработка изображений":
        end_path = "processed_result"
    elif tab_name == "Pdf на картинки":
        end_path = "images_from_pdf"
    elif tab_name == "Текст на карточки":
        end_path = ""
    elif tab_name == "Вписать картинки":
        end_path = "formated_images"
    to_save_folder = os.path.join(entry.get(), end_path)
    save_folder_path.set(to_save_folder)


def select_folder(entry):
    folder_selected = filedialog.askdirectory(initialdir=entry.get())
    if folder_selected != "":
        entry.set(folder_selected)


def tab2_handler():
    folder_path = source_folder_path.get()
    save_folder = save_folder_path.get()
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    if not folder_path:
        messagebox.showwarning("Внимание", "Пожалуйста, выберите папку.")
        return
    try:
        image_handler(folder_path, save_folder, brightness_level=brightness_level_entry.get(),
                      contrast_level=contrast_level_entry.get(), saturation_level=saturation_level_entry.get(),
                      compression_level=compression_level_entry.get(), operation=operation_menu.get())
        messagebox.showinfo("Готово", "Обработка успешно выполнена!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


# Вкладка 2: Сжатие изображений

tk.Label(tab2, text="Сжатиe [1 - 100]:").grid(row=0, column=0, sticky="w")
compression_level_entry = tk.Scale(tab2, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
compression_level_entry.grid(row=0, column=1, sticky="w")

tk.Label(tab2, text="Яркость [-100 - 100]:").grid(row=1, column=0, sticky="w")
brightness_level_entry = tk.Scale(tab2, from_=-100, to=100, orient=tk.HORIZONTAL, length=200)
brightness_level_entry.grid(row=1, column=1, sticky="w")

tk.Label(tab2, text="Контрастность [-100 - 100]:").grid(row=2, column=0, sticky="w")
contrast_level_entry = tk.Scale(tab2, from_=-100, to=100, orient=tk.HORIZONTAL, length=200)
contrast_level_entry.grid(row=2, column=1, sticky="w")

tk.Label(tab2, text="Насыщенность [-100 - 100]:").grid(row=3, column=0, sticky="w")
saturation_level_entry = tk.Scale(tab2, from_=-100, to=100, orient=tk.HORIZONTAL, length=200)
saturation_level_entry.grid(row=3, column=1, sticky="w")

tk.Label(tab2, text="Преобразование:").grid(row=4, column=0, sticky="w")
options = ["-", "90", "180", "270", "отр. по гориз.", "отр. по верт."]
operation_menu = ttk.Combobox(tab2, values=options, state="readonly")
operation_menu.grid(row=4, column=1, sticky="w")
operation_menu.set("-")


# Вкладка 3: Извлечь картинки из PDF

def select_pdf_file():
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_path.set(file_path)
        save_folder_path.set(os.path.join(os.path.dirname(file_path), "images_from_pdf"))


def extract_images_from_pdf():
    start_page = int(start_page_entry.get())
    end_page = int(end_page_entry.get())
    step = int(step_entry.get())
    pdf_file = pdf_path.get()
    output_folder = save_folder_path.get()
    pdf_to_images_mupdf(pdf_path=pdf_file, output_folder=output_folder, first=start_page, last=end_page, step=step)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    messagebox.showinfo("Успех",
                        f"Изображения из {pdf_file} успешно извлечены в {output_folder}.\nСтраницы с {start_page} по {end_page}, шаг {step}.")


pdf_path = tk.StringVar(value=os.getcwd())

tk.Label(tab3, text="Путь до PDF файла:").grid(row=0, column=0, sticky="w")
tk.Entry(tab3, textvariable=pdf_path, width=50).grid(row=0, column=1, sticky="ew")
tk.Button(tab3, text="Выбрать", command=select_pdf_file).grid(row=0, column=2)

tk.Label(tab3, text="Страницы начиная с:").grid(row=1, column=0, sticky="w")
start_page_entry = tk.Entry(tab3)
start_page_entry.insert(0, "1")
start_page_entry.grid(row=1, column=1, sticky="ew")

tk.Label(tab3, text="по: [-1 послед]").grid(row=2, column=0, sticky="w")
end_page_entry = tk.Entry(tab3)
end_page_entry.insert(0, "-1")
end_page_entry.grid(row=2, column=1, sticky="ew")

tk.Label(tab3, text="каждая:").grid(row=3, column=0, sticky="w")
step_entry = tk.Entry(tab3)
step_entry.insert(0, "1")
step_entry.grid(row=3, column=1, sticky="ew")


# Вкладка 4: Текст на карточки
def select_font_path():
    initial_dir = os.getcwd()  # Текущая директория приложения
    if font_path.get() != "":
        initial_dir = font_path.get()

    folder_selected = filedialog.askopenfilename(initialdir=initial_dir,
                                                 filetypes=[("Font files", "*.ttf *.otf"), ("All files", "*.*")])
    if folder_selected != "":
        font_path.set(folder_selected)


def submit_data():
    # Здесь должна быть ваша логика для размещения текста на изображениях

    main_text = text_input.get("1.0", tk.END)
    ls = main_text.split("\n")
    my_colors = {"белый": "#ffffff", "черный": "#000000", "серый": "#C0C0C0", "красный": "#fe0000",
                 "оранжевый": "#ff7513",
                 "желтый": "#ffcc00", "зеленый": "#019934", "голубой": "#00FFFF", "синий": "#3401cc",
                 "фиолетовый": "#990099", "коричневый": "#8B4513", "розовый": "#FFC0CB"}

    # Пример использования
    counter = 0
    for x in range(repeat_times.get()):
        for text_string in ls:
            counter += 1
            place_text_on_image((image_width.get(), image_height.get()), text_string, counter,
                                font_path=font_path.get(), initial_font_size=max_font_size.get(),
                                save_path=save_folder_path.get(), bg_color=my_colors[bg_color_combobox.get()],
                                text_color=my_colors[text_color_combobox.get()], name_prefix=name_prefix.get())
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


font_path = tk.StringVar()
max_font_size = tk.IntVar(value=200)
image_width = tk.IntVar(value=900)
image_height = tk.IntVar(value=600)
repeat_times = tk.IntVar(value=1)
name_prefix = tk.StringVar(value="name")
colors = ["белый", "черный", "серый", "красный", "оранжевый", "желтый", "зеленый", "голубой", "синий", "фиолетовый",
          "коричневый", "розовый"]

# Элементы интерфейса для вкладки\
tk.Label(tab4, text="Путь до шрифта:").grid(row=0, column=0, sticky="w")
ttk.Entry(tab4, textvariable=font_path).grid(row=0, column=1, columnspan=4, sticky="ew")
ttk.Button(tab4, text="Выбрать", command=select_font_path).grid(row=0, column=5, sticky="ew")

tk.Label(tab4, text="Макс. размер шрифта:").grid(row=1, column=0, sticky="w")
ttk.Entry(tab4, textvariable=max_font_size).grid(row=1, column=1, sticky="ew")

tk.Label(tab4, text="Ширина изоб.:").grid(row=1, column=2, sticky="w")
ttk.Entry(tab4, textvariable=image_width).grid(row=1, column=3, sticky="ew")

tk.Label(tab4, text="Высота изоб.").grid(row=1, column=4, sticky="w")
ttk.Entry(tab4, textvariable=image_height).grid(row=1, column=5, sticky="ew")

tk.Label(tab4, text="Число копий:").grid(row=2, column=0, sticky="w")
ttk.Entry(tab4, textvariable=repeat_times).grid(row=2, column=1, sticky="ew")

tk.Label(tab4, text="Цвет текста:").grid(row=2, column=2, sticky="w")
text_color_combobox = ttk.Combobox(tab4, values=colors, state="readonly")
text_color_combobox.grid(row=2, column=3, sticky="ew")
text_color_combobox.set("черный")

tk.Label(tab4, text="Цвет фона:").grid(row=2, column=4, sticky="w")
bg_color_combobox = ttk.Combobox(tab4, values=colors, state="readonly")
bg_color_combobox.grid(row=2, column=5, sticky="ew")
bg_color_combobox.set("белый")

text_input = tk.Text(tab4, height=10)
text_input.grid(row=3, column=0, columnspan=6, sticky="ew")

ttk.Button(tab4, text="Вставить", command=paste_from_clipboard).grid(row=4, column=0, sticky="ew")
ttk.Button(tab4, text="Копировать", command=copy_to_clipboard).grid(row=4, column=1, sticky="ew")

tk.Label(tab4, text="Префикс результата:").grid(row=4, column=2, sticky="w")
ttk.Entry(tab4, textvariable=name_prefix).grid(row=4, column=3, sticky="ew")

# Создаем общий фрейм для всех вкладок
common_frame = tk.Frame(app)
common_frame.pack(side=tk.TOP, fill=tk.X)


# Вкладка 6:  вписать в картинки
def start_format_images():
    folder_path = source_folder_path.get()
    save_folder = save_folder_path.get()
    width = int(cards_width_entry.get())
    height = int(cards_height_entry.get())
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    if not folder_path:
        messagebox.showwarning("Внимание", "Пожалуйста, выберите папку.")
        return
    try:
        resize_and_orient_images(folder_path, save_folder, width, height, cut=cut_images.get())
        messagebox.showinfo("Готово", "Операция успешно выполнена!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


tk.Label(tab6, text="Размер карт в мм (ширина):").grid(row=0, column=0, sticky="w")
cards_width_entry = tk.Entry(tab6)
cards_width_entry.insert(0, "50")
cards_width_entry.grid(row=0, column=1, sticky="ew")

tk.Label(tab6, text="Размер карт в мм (высота):").grid(row=1, column=0, sticky="w")
cards_height_entry = tk.Entry(tab6)
cards_height_entry.insert(0, "50")
cards_height_entry.grid(row=1, column=1, sticky="ew")

tk.Label(tab6, text="На весь размер (обрезать):").grid(row=2, column=0, sticky="w")
cut_images = tk.BooleanVar()
checkbutton = tk.Checkbutton(tab6, variable=cut_images)
checkbutton.grid(row=2, column=1, sticky="w")


#  общий фрейм
def main_button():
    tab_name = tabControl.tab(tabControl.index("current"), "text")
    if tab_name == 'Картиинки в PDF':
        start_processing()
    elif tab_name == "Обработка изображений":
        tab2_handler()
    elif tab_name == "Pdf на картинки":
        extract_images_from_pdf()
    elif tab_name == "Текст на карточки":
        submit_data()
    elif tab_name == "Вписать картинки":
        start_format_images()


label = tk.Label(common_frame, text="This is a common label for all tabs")

tk.Label(common_frame, text="Путь до папки с изображениями:").grid(row=0, column=0)
tk.Entry(common_frame, textvariable=source_folder_path, width=50).grid(row=0, column=1)
tk.Button(common_frame, text="Выбрать", command=lambda: select_source_folder(source_folder_path)).grid(row=0, column=2)

tk.Label(common_frame, text="Путь сохранения:").grid(row=1, column=0)
tk.Entry(common_frame, textvariable=save_folder_path, width=50).grid(row=1, column=1)
tk.Button(common_frame, text="Выбрать", command=lambda: select_folder(save_folder_path)).grid(row=1, column=2)

ttk.Button(common_frame, text="Пуск", command=main_button, width=30).grid(row=0, column=3)

app.mainloop()
