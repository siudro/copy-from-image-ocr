# تثبيت المكتبات المطلوبة
# pip install Pillow pytesseract pyautogui playsound pyperclip pynput

import pyautogui
import pytesseract
from PIL import Image
import numpy as np
import cv2
from playsound import playsound
import pyperclip  # إضافة المكتبة
import time  # تأكد من استيراد مكتبة time
from pynput import mouse  # استيراد مكتبة pynput

# إعداد Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # تأكد من تعديل المسار حسب تثبيت Tesseract

# متغيرات لتخزين إحداثيات الماوس
start_x = start_y = end_x = end_y = None

def on_click(x, y, button, pressed):
    global start_x, start_y, end_x, end_y
    if button == mouse.Button.right:  # إذا تم الضغط على زر الفأرة الأيمن
        if pressed:
            start_x, start_y = x, y  # حفظ الإحداثيات عند الضغط
        else:
            end_x, end_y = x, y  # حفظ الإحداثيات عند الإفلات
            if start_x is not None and start_y is not None and end_x is not None and end_y is not None:
                take_screenshot_and_recognize_text(start_x, start_y, end_x, end_y)

def take_screenshot_and_recognize_text(x1, y1, x2, y2):
    image_path = take_screenshot(x1, y1, x2, y2)
    text = recognize_text(image_path)
    
    if text.strip():
        pyperclip.copy(text)
        print("تم نسخ النص:", text)
        playsound('C:/Users/LENOVO/Downloads/copy text from snippet/shocked-sound-effect.mp3') # تأكد من وجود ملف الصوت في المسار الصحيح    else:
        print("لم يتم التعرف على أي نص.")

def take_screenshot(x1, y1, x2, y2):
    # التقاط لقطة شاشة
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    screenshot.save("screenshot.png")
    return "screenshot.png"

def recognize_text(image_path):
    # التعرف على النص في الصورة
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img, lang='ara')
    return text

def main():
    print("اضغط مع الاستمرار على زر الفأرة الأيمن لبدء التقاط لقطة الشاشة.")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()  # بدء الاستماع لأحداث الماوس

if __name__ == "__main__":
    main()
