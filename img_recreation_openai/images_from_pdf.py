import fitz  # PyMuPDF
import os

def extract_images_from_pdf(pdf_path, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Open the provided PDF
    pdf_document = fitz.open(pdf_path)
    
    # Loop through each page in the PDF
    image_count = 0
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # Load each page
        image_list = page.get_images(full=True)  # Get images on the page
        
        # Loop through images on the current page
        for img_index, img in enumerate(image_list):
            xref = img[0]  # xref of the image
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]  # Get image bytes
            
            # Save the image as a PNG file
            image_filename = os.path.join(output_folder, f"image_{image_count + 1}.png")
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
                print(f"Saved: {image_filename}")
            
            image_count += 1

    print(f"Extracted {image_count} images from the PDF.")

# Example usage
pdf_file = "AI _Engineer.pdf"  # Change to your PDF file path
output_dir = "extracted_images"
extract_images_from_pdf(pdf_file, output_dir)
