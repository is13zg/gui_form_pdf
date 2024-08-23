import os
from PIL import Image, ImageEnhance
from images_into_cards import is_image
from PIL import ImageDraw, ImageFont
from text_to_cards import try_set_custom_font
import math


def image_setting(image_path, brightness_level, contrast_level, saturation_level, operation):
    # Открываем изображение
    image = Image.open(image_path)

    if brightness_level != 0:
        # Приводим уровень яркости к диапазону от 1 до 2, где 1 — без изменений, 2 — удвоенная яркость
        brightness_factor = 1 + (brightness_level / 100)
        # Создаем объект для изменения яркости
        enhancer = ImageEnhance.Brightness(image)
        # Применяем изменение яркости
        image = enhancer.enhance(brightness_factor)
    if contrast_level != 0:
        # Приводим уровень контрастности к диапазону от 1 до 2, где 1 — без изменений, 2 — максимальное повышение контрастности
        contrast_factor = 1 + (contrast_level / 100)
        # Создаем объект для изменения контрастности
        enhancer = ImageEnhance.Contrast(image)
        # Применяем изменение контрастности
        image = enhancer.enhance(contrast_factor)
    if saturation_level != 0:
        # Приводим уровень контрастности к диапазону от 1 до 2, где 1 — без изменений, 2 — максимальное повышение контрастности
        saturation_factor = 1 + (saturation_level / 100)
        # Создаем объект для изменения контрастности
        enhancer = ImageEnhance.Color(image)
        # Применяем изменение контрастности
        image = enhancer.enhance(saturation_factor)

    if operation == '90':
        image = image.rotate(90, expand=True)
    elif operation == '180':
        image = image.rotate(180, expand=True)
    elif operation == '270':
        image = image.rotate(270, expand=True)
    elif operation == 'отр. по гориз.':
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif operation == 'отр. по верт.':
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

    return image


def add_image_number(image, number, size_percentage, padding_percentage):
    draw = ImageDraw.Draw(image)

    # Размер изображения
    width, height = image.size

    # Размер номера в процентах от площади изображения
    font_size = int(math.sqrt(width * height) * size_percentage / 100)

    # Задаем шрифт и размер текста
    font = try_set_custom_font("", font_size)

    # Размер текста
    text = str(number)
    text_width, text_height = font.getbbox(text)[2] - font.getbbox(text)[0], font.getbbox(text)[3] - font.getbbox(text)[
        1]

    # Диаметр круга
    circle_diameter = max(text_width, text_height) + int(0.4 * font_size)

    # Позиция текста (правый верхний угол с отступом в процентах от размера изображения)
    padding = int(min(width, height) * padding_percentage / 100)
    position = (width - circle_diameter - padding, padding)

    # Позиция и размеры круга
    circle_position = [
        position[0], position[1] * 1.3,
                     position[0] + circle_diameter, position[1] * 1.3 + circle_diameter
    ]

    # Рисуем круг
    draw.ellipse(circle_position, fill="black")

    # Позиция текста внутри круга (центр круга)
    text_position = (
        position[0] + (circle_diameter - text_width) // 2,
        position[1] + (circle_diameter - text_height) // 2
    )

    # Добавляем текст (номер изображения)
    draw.text(text_position, text, fill="white", font=font)

    return image


def image_handler(folder_path, save_path, brightness_level, contrast_level, saturation_level, compression_level,
                  operation, numeration):
    for i, filename in enumerate(os.listdir(folder_path)):
        image_path = os.path.join(folder_path, filename)
        if is_image(image_path):
            img = image_setting(image_path, brightness_level, contrast_level, saturation_level, operation)
            quality = 95

            if numeration != "-":
                img = add_image_number(img, i + 1, 3 * float(numeration), 2 * float(numeration))

            if compression_level:
                quality = int(compression_level * (-10 / 11) + 96)  # Scale between 5 and 95
                img.save(os.path.join(save_path, filename), quality=quality, optimize=True)
            img.save(os.path.join(save_path, filename), quality=quality)

# image_handler("folder", "save_folder", 1, 0, 0, 0, "-")
