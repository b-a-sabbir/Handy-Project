from tkinter import Tk, filedialog, Button, Label
from PIL import Image
from fpdf import FPDF
import os

def convert_images_to_pdf():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if file_paths:
        try:
            # Sort the file paths based on filename
            file_paths = sorted(file_paths, key=lambda x: os.path.basename(x))

            pdf = FPDF()
            pdf.set_auto_page_break(False)

            for file_path in file_paths:
                image = Image.open(file_path)

                if image.mode == 'RGBA':
                    image = image.convert('RGB')

                img_width, img_height = image.size
                pdf_width, pdf_height = 210, 297  # A4 in mm

                aspect_ratio = img_width / img_height
                if aspect_ratio > (pdf_width / pdf_height):
                    new_width = pdf_width
                    new_height = pdf_width / aspect_ratio
                else:
                    new_height = pdf_height
                    new_width = pdf_height * aspect_ratio

                x_offset = (pdf_width - new_width) / 2
                y_offset = (pdf_height - new_height) / 2

                pdf.add_page()
                pdf.image(file_path, x=x_offset, y=y_offset, w=new_width, h=new_height)

                # Watermark
                pdf.set_font("Arial", size=10)
                watermark_text = "scanned by Sabbir"
                pdf.set_text_color(150, 150, 150)
                text_width = pdf.get_string_width(watermark_text)
                x_watermark = (pdf_width - text_width) / 2
                y_watermark = pdf_height - 10

                pdf.text(x_watermark, y_watermark, watermark_text)

            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if save_path:
                pdf.output(save_path)
                label.config(text=f"Conversion successful! Saved at: {save_path}")
            else:
                label.config(text="Save cancelled.")
        except Exception as e:
            label.config(text=f"Error: {str(e)}")
    else:
        label.config(text="No files selected.")

# GUI
root = Tk()
root.title("Image to PDF Converter")

Button(root, text="Select Images and Convert to PDF", command=convert_images_to_pdf).pack(pady=10)
label = Label(root, text="")
label.pack(pady=10)

root.mainloop()
