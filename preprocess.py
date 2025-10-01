import fitz  # PyMuPDF
import subprocess
import requests
import os


def download_and_preprocess_pdf(pdf_url, output_dir="pages", dpi=300):
    """
    Downloads a PDF, preprocess the images and retruns the routes
    """

    # Create temp dir
    pdf_dir = "temp_pdf"
    os.makedirs(pdf_dir, exist_ok=True)

    # Download PDF
    pdf_name = os.path.basename(pdf_url)
    pdf_path = os.path.join(pdf_dir, pdf_name)
    response = requests.get(pdf_url)
    with open(pdf_path, "wb") as f:
        f.write(response.content)

    # Pages Dir
    os.makedirs(output_dir, exist_ok=True)

    # Open PDF
    doc = fitz.open(pdf_path)
    image_paths = []

    for i, page in enumerate(doc):

        # Render page
        pix = page.get_pixmap(dpi=dpi)
        raw_img = f"{output_dir}/page_{i+1}_raw.png"
        clean_img = f"{output_dir}/page_{i+1}.png"

        # Store Raw Image
        with open(raw_img, "wb") as img_file:
            img_file.write(pix.tobytes("png"))

        # Preprocess with ImageMagick
        subprocess.run([
            "magick", raw_img,
            "-colorspace", "Gray",
            "-density", str(dpi),
            "-level", "0%,100%,1.2",
            "-normalize",
            "-threshold", "50%",
            clean_img
        ])

        print(f"✅ Preprocessed image: {clean_img}")
        
        image_paths.append(clean_img)
    
    os.remove(pdf_path)
    
    return image_paths
