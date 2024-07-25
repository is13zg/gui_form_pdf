import os
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import black
import imghdr


#  create_pdf(directory, width, height, output_path='.', file_name='create_pdf', separation=1, margin=5)
#
# формирует pdf по заданной ширине и высоте картинки с разделительной сеткой, из папки с картинками
#
#  directory - путь до папки с картинками
#  width, height -  ширина и высота картинок на листе а4
#  output_path  -  путь куда сохранить полученный pdf, по умолчанию текущая папка откуда запускается скрипт
#  file_name  -  название конечного pdf файла, по умолчанию create_pdf
#  separation - толщина разделительной сетки, по умолчанию 1 мм
#  margin  -  отсуп от края листа, т.к. принтер не печатает с краев,  по умолчанию 5 мм
#
# Пример использования
# image_files = ['image1.png', 'image2.png', 'image3.png']
# create_pdf(image_files, 50, 50)


def get_files_with_full_paths(directory):
    try:
        # Используем метод listdir() из модуля os для получения списка файлов и директорий в указанной директории
        entries = os.listdir(directory)
        # Создаем список полных путей до файлов, исключая поддиректории
        file_paths = [os.path.join(directory, entry) for entry in entries if
                      os.path.isfile(os.path.join(directory, entry))]
        return file_paths
    except OSError as e:
        # Обработка ошибки, если директория не существует или не может быть прочитана
        print(f"Ошибка при получении списка файлов: {e}")
        return []


def update_file_name(name, path):
    counter = 1
    new_name = name
    while os.path.exists(os.path.join(path, f"{new_name}.pdf")):
        new_name = f"{name}_{counter}"
        counter += 1
    return new_name


def mm_to_pixels(mm, dpi=300):
    # Перевод мм в дюймы (1 дюйм = 25.4 мм), затем в пиксели
    return int(mm / 25.4 * dpi)


def resize_image(image_file, width_mm, height_mm, dpi=300):
    with Image.open(image_file) as img:
        # Конвертируем размеры из мм в пиксели
        width_px = mm_to_pixels(width_mm, dpi)
        height_px = mm_to_pixels(height_mm, dpi)

        # Проверяем текущие размеры изображения
        if img.size[0] != width_px or img.size[1] != height_px:
            # Изменяем размер изображения с высоким качеством
            img = img.resize((width_px, height_px), Image.Resampling.LANCZOS)
            temp_file = f'temp_{os.path.basename(image_file)}'
            img.save(temp_file)
            return temp_file
        else:
            # Если размеры уже подходят, возвращаем оригинальный файл
            return image_file


def draw_grid(c, a4_width, a4_height, width_pts, height_pts, separation_pts, width_margin_pts, height_margin_pts, linewidth):
    if separation_pts > 0:
        # Вертикальные линии
        current_x = width_margin_pts
        while current_x <= a4_width - width_margin_pts:
            c.setStrokeColor(black)
            c.setLineWidth(linewidth)
            c.line(current_x, 0, current_x, a4_height)
            current_x += width_pts + separation_pts

        # Горизонтальные линии
        current_y = a4_height - height_margin_pts
        while current_y >= 0:
            c.setStrokeColor(black)
            c.setLineWidth(linewidth)
            c.line(0, current_y, a4_width, current_y)
            current_y -= height_pts + separation_pts


def create_pdf_new(directory, width, height, output_path='.', file_name='create_pdf', separation=1, margin=5):
    print(
        f"directory{directory}, width{width}, height{height}, output_path={output_path}, file_name={file_name}, separation={separation}, margin={margin}")
    image_files = get_files_with_full_paths(directory)
    file_name = update_file_name(file_name, output_path)
    a4_width, a4_height = A4
    margin_pts = margin * mm
    width_pts = width * mm
    height_pts = height * mm
    separation_pts = separation * mm
    c = canvas.Canvas(os.path.join(output_path, f"{file_name}.pdf"), pagesize=A4)
    x, y = margin_pts, a4_height - height_pts - margin_pts

    width_count = (a4_width - 2 * margin_pts) // (width_pts + separation_pts)
    height_count = (a4_height - 2 * margin_pts) // (height_pts + separation_pts)
    width_margin_pts = (a4_width - width_count * (width_pts + separation_pts)) / 2
    height_margin_pts = (a4_height - height_count * (height_pts + separation_pts)) / 2

    x = width_margin_pts
    for image_file in image_files:
        temp_file = resize_image(image_file, width_pts / mm, height_pts / mm)
        if x + width_pts > a4_width - width_margin_pts:
            x = width_margin_pts
            y -= (height_pts + separation_pts)
            if y < height_margin_pts:
                draw_grid(c, a4_width, a4_height, width_pts, height_pts, separation_pts, width_margin_pts, separation)
                c.showPage()
                y = a4_height - height_pts - height_margin_pts
        c.drawImage(temp_file, x, y, width=width_pts, height=height_pts)
        os.remove(temp_file)
        x += width_pts + separation_pts
    draw_grid(c, a4_width, a4_height, width_pts, height_pts, separation_pts, width_margin_pts, separation)
    draw_grid(c, a4_width, a4_height, width_pts, height_pts, separation_pts, height_margin_pts, separation)
    c.save()


def is_image(file_path):
    # Проверяем, существует ли файл
    if not os.path.isfile(file_path):
        return False

    # Проверяем MIME-тип файла
    image_type = imghdr.what(file_path)
    return image_type is not None


def create_pdf_old(directory, width, height, output_path='.', file_name='create_pdf', separation=1, margin=5):
    print(
        f"directory{directory}, width{width}, height{height}, output_path={output_path}, file_name={file_name}, separation={separation}, margin={margin}")
    image_files = get_files_with_full_paths(directory)
    file_name = update_file_name(file_name, output_path)
    a4_width, a4_height = A4
    margin_pts = margin * mm
    width_pts = width * mm
    height_pts = height * mm
    separation_pts = separation * mm
    c = canvas.Canvas(os.path.join(output_path, f"{file_name}.pdf"), pagesize=A4)
    x, y = margin_pts, a4_height - height_pts - margin_pts

    for image_file in image_files:
        if not is_image(image_file):
            continue
        temp_file = resize_image(image_file, width_pts / mm, height_pts / mm)
        if x + width_pts > a4_width - margin_pts:
            x = margin_pts
            y -= (height_pts + separation_pts)
            if y < margin_pts:
                draw_grid(c, a4_width, a4_height, width_pts, height_pts, separation_pts, margin_pts, separation)
                c.showPage()
                y = a4_height - height_pts - margin_pts
        c.drawImage(temp_file, x, y, width=width_pts, height=height_pts)
        os.remove(temp_file)
        x += width_pts + separation_pts

    draw_grid(c, a4_width, a4_height, width_pts, height_pts, separation_pts, margin_pts, separation)
    c.save()


def create_pdf(directory, width, height, output_path='.', file_name='create_pdf', separation=1, margin=5,max_separation=True):
    print(
        f"directory{directory}, width{width}, height{height}, output_path={output_path}, file_name={file_name}, separation={separation}, margin={margin}")
    image_files = get_files_with_full_paths(directory)
    file_name = update_file_name(file_name, output_path)
    a4_width, a4_height = A4
    margin_pts = margin * mm
    width_pts = width * mm
    height_pts = height * mm
    separation_pts = separation * mm
    c = canvas.Canvas(os.path.join(output_path, f"{file_name}.pdf"), pagesize=A4)



    if max_separation:
        ww = margin_pts * 2 + separation_pts
        while a4_width - ww > 0:
            ww += width_pts + separation_pts
        ww -= width_pts + separation_pts
        w_margin_pts = max(0.95 * (margin_pts + (a4_width - ww) / 2), margin_pts)

        hh = margin_pts * 2 + separation_pts
        while a4_height - hh > 0:
            hh += height_pts + separation_pts
        hh -= height_pts + separation_pts
        h_margin_pts = max(0.95 * (margin_pts + (a4_height - hh) / 2), margin_pts)

        height_margin_pts = h_margin_pts
        width_margin_pts = w_margin_pts
    else:
        height_margin_pts = margin_pts
        width_margin_pts = margin_pts


    x, y = width_margin_pts, a4_height - height_pts - height_margin_pts


    for image_file in image_files:
        if not is_image(image_file):
            continue
        temp_file = resize_image(image_file, width_pts / mm, height_pts / mm)
        if x + width_pts > a4_width - width_margin_pts:
            x = width_margin_pts
            y -= (height_pts + separation_pts)
            if y < height_margin_pts:
                draw_grid(c, a4_width, a4_height, width_pts, height_pts, separation_pts, width_margin_pts, height_margin_pts, separation)
                c.showPage()
                y = a4_height - height_pts - height_margin_pts
        c.drawImage(temp_file, x, y, width=width_pts, height=height_pts)
        os.remove(temp_file)
        x += width_pts + separation_pts

    draw_grid(c, a4_width, a4_height, width_pts, height_pts, separation_pts, width_margin_pts, height_margin_pts, separation)
    c.save()
#  create_pdf(directory, width, height, output_path='.', file_name='create_pdf', separation=1, margin=5)
#
#  directory - путь до папки с картинками
#  width, height -  ширина и высота картинок на листе а4
#  output_path  -  путь куда сохранить полученный pdf, по умолчанию текущая папка откуда запускается скрипт
#  file_name  -  название конечного pdf файла, по умолчанию create_pdf
#  separation - толщина разделительной сетки, по умолчанию 1 мм
#  margin  -  отсуп от края листа, т.к. принтер не печатает с краев,  по умолчанию 5 мм
#
# Пример использования
# image_files = ['image1.png', 'image2.png', 'image3.png']
# create_pdf(image_files, 50, 50)
