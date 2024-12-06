from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image
from dotenv import load_dotenv
import os
import re

load_dotenv()

def natural_sort_key(text):
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

def convert_to_cmyk(image_path, output_path):
    """
    Converts an RGB image to CMYK and saves it.
    """
    with Image.open(image_path) as img:
        cmyk_image = img.convert('CMYK')  # تبدیل تصویر به CMYK
        cmyk_image.save(output_path, format='JPEG')  # ذخیره با فرمت CMYK JPEG

def images_to_pdf(image_folder, output_pdf_path, page_width, page_height, font_path, font_name, scale_factor=6.7):
    # ثبت فونت سفارشی
    pdfmetrics.registerFont(TTFont(font_name, font_path))

    image_files = [f for f in os.listdir(image_folder) if f.endswith('.png') or f.endswith('.jpg')]
    image_files.sort(key=natural_sort_key)

    c = canvas.Canvas(output_pdf_path, pagesize=(page_width, page_height))

    # تنظیم اطلاعات متادیتا PDF
    c.setTitle(os.getenv("PDF_TITLE"))
    c.setSubject(os.getenv("PDF_SUBJECT"))
    c.setAuthor(os.getenv("PDF_AUTHOR"))
    c.setCreator(os.getenv("PDF_CREATOR"))
    c.setProducer(os.getenv("PDF_PRODUCER"))

    temp_folder = os.path.join(image_folder, "temp_cmyk")
    os.makedirs(temp_folder, exist_ok=True)

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        cmyk_image_path = os.path.join(temp_folder, f"cmyk_{image_file}")

        # تبدیل تصویر به CMYK
        convert_to_cmyk(image_path, cmyk_image_path)

        # باز کردن تصویر CMYK
        with Image.open(cmyk_image_path) as img:
            image_width, image_height = img.size

            # اسکیل کردن تصویر (تقسیم بر scale_factor)
            scaled_width = image_width / scale_factor
            scaled_height = image_height / scale_factor

            # محاسبه موقعیت تصویر برای قرار گرفتن در وسط صفحه
            x = (page_width - scaled_width) / 2
            y = (page_height - scaled_height) / 2

            # اضافه کردن نام فایل به عنوان متن در بالای تصویر
            file_name_without_extension = os.path.splitext(image_file)[0]
            file_name_without_extension = file_name_without_extension.replace("_", " #")
            c.setFont(font_name, 12)
            text_width = c.stringWidth(file_name_without_extension, font_name, 12)
            text_x = (page_width - text_width) / 2
            c.drawString(text_x, y + scaled_height + 10, file_name_without_extension)

            # وارد کردن تصویر
            c.drawImage(cmyk_image_path, x, y, width=scaled_width, height=scaled_height)

            # شماره صفحه
            page_number = c.getPageNumber()
            c.setFont(font_name, 10)
            c.drawCentredString(page_width / 2, (3 * 2.83) + 16, f"Page {page_number}")

            # افزودن صفحه جدید
            c.showPage()

    # ذخیره کردن PDF
    c.save()

    # حذف فایل‌های موقت CMYK
    for temp_file in os.listdir(temp_folder):
        os.remove(os.path.join(temp_folder, temp_file))
    os.rmdir(temp_folder)
