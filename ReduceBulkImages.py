import os
from PIL import Image


def compress_single_image(img, output_path, target_size_bytes):
    quality = 95

    while quality > 10:
        img.save(
            output_path,
            "JPEG",
            quality=quality,
            optimize=True
        )

        if os.path.getsize(output_path) <= target_size_bytes:
            return

        quality -= 5

    width, height = img.size

    while True:
        width = int(width * 0.9)
        height = int(height * 0.9)

        img_resized = img.resize(
            (width, height),
            Image.Resampling.LANCZOS
        )

        img_resized.save(
            output_path,
            "JPEG",
            quality=50,
            optimize=True
        )

        if os.path.getsize(output_path) <= target_size_bytes:
            return

        if width < 100 or height < 100:
            return


def batch_process_images(root_input, root_output, target_size_kb=150):
    target_size_bytes = target_size_kb * 1024

    valid_extensions = (
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp",
        ".tiff"
    )

    for current_root, dirs, files in os.walk(root_input):

        relative_path = os.path.relpath(
            current_root,
            root_input
        )

        output_folder = os.path.join(
            root_output,
            relative_path
        )

        os.makedirs(output_folder, exist_ok=True)

        image_counter = 1

        for filename in files:

            if not filename.lower().endswith(valid_extensions):
                continue

            input_path = os.path.join(
                current_root,
                filename
            )

            output_filename = f"{image_counter}.jpg"

            output_path = os.path.join(
                output_folder,
                output_filename
            )

            try:
                with Image.open(input_path) as img:
                    img_rgb = img.convert("RGB")

                    compress_single_image(
                        img_rgb,
                        output_path,
                        target_size_bytes
                    )

                final_size = (
                    os.path.getsize(output_path) / 1024
                )

                print(
                    f"{input_path} -> "
                    f"{output_path} "
                    f"({final_size:.1f} KB)"
                )

                image_counter += 1

            except Exception as e:
                print(
                    f"Error processing "
                    f"{input_path}: {e}"
                )


batch_process_images(
    "/Users/arvin.fuentes/PyCharmMiscProject/shirts",
    "/Users/arvin.fuentes/PyCharmMiscProject/compressed_shirts",
    target_size_kb=150
)