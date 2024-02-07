from PIL import Image
import os


def compress_images(source_folder, output_folder, compression_level):
    """
    Compress all JPEG and PNG images in the source folder with the specified compression level.

    :param source_folder: Path to the folder containing the images.
    :param output_folder: Path to the folder where the compressed images will be saved.
    :param compression_level: Compression level (1-10), where 10 is the highest compression.
    """
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Adjust compression level for Pillow
    quality = int((1 - (compression_level / 10)) * 95) + 5  # Scale between 5 and 95

    # Process each file in the source folder
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            with Image.open(os.path.join(source_folder, filename)) as img:
                # Set file format based on file extension
                file_format = 'JPEG' if filename.lower().endswith(('.jpg', '.jpeg')) else 'PNG'

                # Save the compressed image
                output_path = os.path.join(output_folder, filename)
                img.save(output_path, format=file_format, quality=quality, optimize=True)

    print(f"Images compressed and saved to {output_folder}")


# Example usage
# ompress_images('C:\\Users\\1\\PycharmProjects\\pythonProject\\blicumcards', 'C:\\Users\\1\\PycharmProjects\\pythonProject\\blicumcardsafter', 3)