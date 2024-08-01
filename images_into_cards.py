from PIL import Image, ImageOps
import os
Image.MAX_IMAGE_PIXELS = None
import imghdr

def is_image(file_path):
    # Проверяем, существует ли файл
    if not os.path.isfile(file_path):
        return False

    # Проверяем MIME-тип файла
    image_type = imghdr.what(file_path)
    return image_type is not None

def resize_and_rotate_to_fit(image_path, target_width, target_height, cut=False):
    # Загрузка изображения
    img = Image.open(image_path)
    original_width, original_height = img.size

    # Определение, следует ли повернуть изображение
    rotate_image = (original_width > original_height) != (target_width > target_height)
    if rotate_image:
        img = img.rotate(90, expand=True)
        original_width, original_height = original_height, original_width
    if cut:
        # Изменение размера с обрезкой, чтобы изображение заполнило весь холст
        new_img = ImageOps.fit(img, (target_width, target_height), Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    else:
        # Расчет соотношения сторон для подгонки изображения под заданный размер
        ratio = min(target_width / original_width, target_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)

        # Изменение размера изображения
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)

        if resized_img.mode == 'RGB':
            print("mode rgb")
            # Convert RGB image to RGBA
            resized_img = resized_img.convert('RGBA')

        # Создание нового изображения с заданным размером
        new_img = Image.new('RGBA', (target_width, target_height),(255,255,255))
        # Вычисление позиции вставки измененного изображения
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        # Вставка изображения
        print("before_paste")
        new_img.paste(resized_img, (x_offset, y_offset), resized_img)
        new_img = new_img.convert("RGB")
        print("after_paste")
    return new_img


def resize_and_orient_images(folder_path, save_path, new_width_mm, new_height_mm, cut=False):
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        if is_image(image_path):
            img = resize_and_rotate_to_fit(image_path, new_width_mm * 10, new_height_mm * 10, cut=cut)
            img.save(os.path.join(save_path, filename))



