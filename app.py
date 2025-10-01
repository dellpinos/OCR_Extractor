from preprocess import download_and_preprocess_pdf
from ocr import extract_text_from_images
import os
import random
import string

def cleanPagesDir(pages_dir):
    if os.path.exists(pages_dir):
        for f in os.listdir(pages_dir):
            file_path = os.path.join(pages_dir, f)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"No se pudo borrar {file_path}: {e}")
                    
def main():
    
    # Target URL (PDF format)
    pdf_url = "https://www.frlp.utn.edu.ar/sites/default/files/materias/sistemas/Plan2008/matematica_discreta_1150.pdf"
    
    # Output Format
    output_format = "txt"  # opciones: "txt" o "json"
    
    # Output directories
    output_dir = "ocr_outputs"
    pages_dir = "pages"

    os.makedirs(output_dir, exist_ok=True)
    cleanPagesDir(pages_dir)
    
    # Download and preprocess
    images = download_and_preprocess_pdf(pdf_url)

    # Extract
    text_results = extract_text_from_images(images, lang="spa") # Spanish 

    # Create unique name based on the URL
    pdf_name = os.path.splitext(os.path.basename(pdf_url))[0]
    token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    output_file = os.path.join(output_dir, f"ocr_{pdf_name}_{token}.{output_format}")
    
    # Store results
    if output_format == "txt":
        with open(output_file, "w", encoding="utf-8") as f:
            for page_num, text in text_results:
                f.write(f"--- Página {page_num} ---\n")
                f.write(text + "\n\n")

    elif output_format == "json":
        import json
        json.dump(
            [{"page": p, "text": t} for p, t in text_results],
            open(output_file, "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=2
        )

    cleanPagesDir(pages_dir)
    print(f"✅ OCR terminado. Archivo guardado en: {output_file}")


if __name__ == "__main__":
    main()
