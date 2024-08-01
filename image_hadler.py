import os
from PIL import Image, ImageEnhance
from images_into_cards import is_image


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


def image_handler(folder_path, save_path, brightness_level, contrast_level, saturation_level, compression_level,
                  operation):
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        if is_image(image_path):
            img = image_setting(image_path, brightness_level, contrast_level, saturation_level, operation)
            quality = 95
            if compression_level:
                quality = int(compression_level * (-10 / 11) + 96)  # Scale between 5 and 95
                img.save(os.path.join(save_path, filename), quality=quality, optimize=True)
            img.save(os.path.join(save_path, filename), quality=quality)

# image_handler("folder", "save_folder", 1, 0, 0, 0, "-")
