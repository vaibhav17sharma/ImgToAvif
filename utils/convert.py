from PIL import Image
import os
import pillow_avif  # Ensure AVIF plugin is registered

print("Starting PNG to AVIF batch conversion...")

for filename in os.listdir("."):
    if filename.lower().endswith(".png"):
        avif_name = filename.rsplit(".", 1)[0] + ".avif"
        print(f"Converting {filename} → {avif_name}")

        with Image.open(filename) as img:
            img.save(avif_name, "AVIF")

print("Done!")
