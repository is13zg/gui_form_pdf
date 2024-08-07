from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import sys

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

def try_set_custom_font(font_path, font_size):
    try:
        # Попытка загрузить шрифт из файла
        custom_font = ImageFont.truetype(font_path, font_size)
        return custom_font
    except (IOError, OSError) as e:
        return ImageFont.truetype(resource_path('TildaSans-Medium.ttf'), font_size)
        # Файл шрифта не найден, возвращаем None



def calculate_text_parameters(font_path, text, image_size, initial_font_size=194):
    """
    Адаптируем размер шрифта исходя из соотношения размеров изображения и предполагаемого количества текста.
    """
    width, height = image_size
    max_width = width - 0.2 * width
    max_height = height - 0.2 * height

    font_size = initial_font_size
    font = try_set_custom_font(font_path, font_size)
    # Оцениваем количество символов в строке и количество строк
    avg_char_width = sum(font.getbbox(char)[2] for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") / 52
    characters_per_line = int(max_width / avg_char_width)
    while characters_per_line < 1:
        font_size -= 1
        font = try_set_custom_font(font_path, font_size)
        avg_char_width = sum(
            font.getbbox(char)[2] for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") / 52
        characters_per_line = int(max_width / avg_char_width)

    lines = textwrap.wrap(text, width=characters_per_line)
    total_text_height = len(lines) * font.getbbox("Ay")[3]  # Высота одной строки текста

    # Корректируем размер шрифта, чтобы текст уместился в выделенную область
    while total_text_height > max_height and font_size > 1:
        font_size -= 1
        font = try_set_custom_font(font_path, font_size)
        avg_char_width = sum(
            font.getbbox(char)[2] for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") / 52
        characters_per_line = int(max_width / avg_char_width)
        lines = textwrap.wrap(text, width=characters_per_line)
        total_text_height = len(lines) * font.getbbox("Ay")[3]

    return font, lines


def place_text_on_image(image_size, text, num, font_path="", initial_font_size=1000, save_path="", bg_color="white",
                        text_color="black", name_prefix=""):
    image = Image.new('RGB', image_size, bg_color)
    draw = ImageDraw.Draw(image)

    font, lines = calculate_text_parameters(font_path, text, image_size, initial_font_size=initial_font_size)

    margin = int(min(image_size) * 0.1)
    y = margin
    for line in lines:
        line_width = font.getbbox(line)[2]
        x = (image_size[0] - line_width) / 2
        draw.text((x, y), line, fill=text_color, font=font)
        y += font.getbbox("Ay")[3]  # Добавляем высоту строки к Y
    output_image_path = os.path.join(save_path, f"{name_prefix}_{num}.png")
    image.save(output_image_path)

# ls = ['3 одинаковых цвета подряд + 10 очков', '3 подряд идущих числа, друг за другом + 10 очков', 'В последовательности 6 различных цветов + 10 очков', 'Только четные числа + 20 очков', 'На позиции 7 число фиолетового цвета +  5 очков', 'Пять одинаковых чисел +30 очков.', 'Четыре подряд идущих числа разных цветов +15 очков.', 'Число 20 на последней позиции +5 очков.', 'Три тайла с номерами, формирующими арифметическую прогрессию подря (например, 2, 4, 6) +10 очков.', 'Пять последовательных чисел, идущих подряд, без учета цвета +20 очков.', 'Три тайла одного цвета на позициях 1, 5, и 10 +15 очков.', 'Четыре тайла различных цветов подряд +10 очков.', 'Два тайла одинакового цвета на краях планшета +5 очков.', 'Только нечетные +25 очков.', 'Только четные +25 очков.', 'Число 1 на первой позиции +5 очков.', 'Четыре одинаковых числа разных цветов +25 очков.', 'Шесть последовательных чисел, идущих подряд, без учета цвета +25 очков.', 'На позиции 5 число зеленого цвета +5 очков.', 'Все числа в пределах от 10 до 20 +10 очков.', 'Все тайлы одного цвета  +40 очков.', 'Ни одного повторяющегося числа +10 очков.', 'Три тайла с числами, делящимися на 5, подряд +10 очков.', 'Три тайла, где каждое следующее число больше предыдущего на 2 (например, 3, 5, 7) +10 очков.', 'На позиции 3 число красного цвета +5 очков.', 'Четыре тайла с числами, делящимися на 3 +15 очков.', 'Четыре тайла с четными числами подряд +20 очков.', 'Два тайла одного цвета на позициях 2 и 9 +10 очков.', 'Семь разных чисел подряд +10 очков.', 'На позиции 4 число синего цвета +5 очков.', 'Пять тайлов одного цвета подряд +25 очков.', 'Два тайла с одинаковыми числами на соседних позициях +5 очков.', 'Число 10 на позиции 10 +20 очков.', 'Чередование чеиных и нечетных чиел +25 очков.', 'Все тайлы с числами, превышающими 6 +15 очков.', 'Три тайла одного цвета на нечетных позициях +10 очков.', 'Четыре тайла с нечетными числами подряд +20 очков.', 'На позиции 6 число желтого цвета +5 очков.', 'Последовательность из четырех тайлов, где числа идут через одно (например, 1, 3, 5, 7) +15 очков.', 'Все тайлы одного цвета, кроме одного +15 очков.', 'Четыре тайла с числами, формирующими геометрическую прогрессию (например, 1, 2, 4, 8) +25 очков.', 'Пять тайлов, номера которых являются простыми числами +20 очков.', 'На позиции 8 число оранжевого цвета +5 очков.', 'Полный набор тайлов с числами от 1 до 5 и от 16 до 20 +40 очков.', 'Число 5 на позиции 5 +5 очков.', 'Последовательность из пяти тайлов, где каждый тайл увеличивается на 3 по сравнению с предыдущим +25 очков.', 'Шесть тайлов подряд с числами, составляющими две тройки одинаковых чисел +25 очков.', 'На позиции 9 число желтого  цвета +5 очков.', 'Последовательность из трех тайлов, где каждое число кратно 4 +15 очков.', 'Любой тайл с цифрой 5 +2 очка.', 'Любой тайл с цифрой 3 +2 очка.', 'Любой тайл с цифрой 6 +2 очка.', 'Любой тайл с цифрой 8 +2 очка.', 'Три тайла подряд одного цвета +10 очков.', 'Два подряд идущих четных числа +10 очка.', 'Один тайл красного цвета между двумя зелеными +5 очка.', 'Любой тайл с числом 10 на четной позиции +5 очка.', 'Четыре тайла с числами, идущими подряд  +10 очков.', 'Любой тайл синего цвета на нечетной позиции +2 очка.', 'Два тайла с одинаковыми числами на расстоянии друг от друга +10 очков.', 'Любой тайл желтого цвета на позиции 5 +5 очков.', 'Три разных цвета подряд +7 очков.', 'Тайл с числом, делящимся на 4, +2 очка.', 'Два подряд идущих нечетных числа +5 очков.', 'Любой тайл зеленого цвета на позиции 10 +10 очков.', 'Любой тайл фиолетового цвета на позиции 1 +5 очков.', 'Тайл с числом 15 на любой позиции +5 очков.', 'Любой тайл оранжевого цвета между двумя тайлами синего цвета +10 очков.', 'Два тайла с числами, делящимися на 3, подряд +10 очков.', 'Любой тайл с числом, равным номеру позиции, на которой он расположен +2 очка.']
#
#
# # Пример использования
# for i in range(70):
# image_size = (900, 600)
# image = place_text_on_image(image_size,"1",1)
