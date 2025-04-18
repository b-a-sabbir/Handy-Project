from tkinter import Tk, filedialog, Button, Label
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
import os

def convert_images_to_pdf():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if file_paths:
        try:
            pdf = FPDF()
            for file_path in file_paths:
                image = Image.open(file_path)
                
                if image.mode == 'RGBA':
                    image = image.convert('RGB')

                # Watermark drawing
                watermark_text = "scanned by Sabbir"
                draw = ImageDraw.Draw(image)
                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except IOError:
                    font = ImageFont.load_default()

                text_width, text_height = draw.textbbox((0, 0), watermark_text, font=font)[2:]
                margin = 10
                x = (image.width - text_width) // 2
                y = image.height - text_height - margin
                draw.text((x, y), watermark_text, font=font, fill=(255, 0, 0))

                # Save temporarily for PDF insertion
                temp_path = os.path.join(os.getcwd(), "temp_image.jpg")
                image.save(temp_path)

                img_width, img_height = image.size
                pdf_width, pdf_height = 210, 297
                aspect_ratio = img_width / img_height
                if aspect_ratio > (pdf_width / pdf_height):
                    new_width = pdf_width
                    new_height = pdf_width / aspect_ratio
                else:
                    new_height = pdf_height
                    new_width = pdf_height * aspect_ratio

                pdf.add_page()
                pdf.image(temp_path, x=(pdf_width - new_width) / 2, y=(pdf_height - new_height) / 2, w=new_width, h=new_height)

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

root = Tk()
root.title("Image to PDF Converter")
Button(root, text="Select Images and Convert to PDF", command=convert_images_to_pdf).pack(pady=10)
label = Label(root, text="")
label.pack(pady=10)
root.mainloop()
