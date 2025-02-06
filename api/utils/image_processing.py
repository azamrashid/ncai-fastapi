from PIL import Image
import numpy as np

def preprocess_image(image_path: str, target_size: tuple):
    image = Image.open(image_path).convert("RGB")
    image = image.resize(target_size)
    return np.array(image)