import pytesseract
from PIL import Image

def extract_text_from_images(image_paths, lang="spa"):
    """
    Uses OCR to extract text
    """
    results = []

    for i, img_path in enumerate(image_paths):
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img, lang=lang)
        results.append((i+1, text))

    return results
