import cv2
import pytesseract
from PIL import Image
import image_processor as ip
import os

def process_image(image_path, verbose=False):
    ip.isolate_damage(image_path)
    ip.isolate_username(image_path)
    
    temp_dir = "CreampuffBOT/temp/"
    upreprocessed_path = os.path.join(temp_dir, "username.jpg")
    dpreprocessed_path = os.path.join(temp_dir, "damage.jpg")
    os.makedirs(temp_dir, exist_ok=True)
    
    config = (
    "--user-words CreampuffBOT/ocr/words.txt "
    "--psm 6 "
    "-c tessdict_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_#"
    )
    ocr_username = pytesseract.image_to_string(Image.open(upreprocessed_path), config=config)
    ocr_damage = pytesseract.image_to_string(Image.open(dpreprocessed_path), config=config)
    
    if verbose:
        print("OCR Username:\n", ocr_username)
        print("OCR Damage:\n", ocr_damage)
        
    return ocr_username, ocr_damage


def main():
    path = "CreampuffBOT/src/damage1.jpg"
    process_image(path, verbose=True)
    

if __name__ == "__main__":
    main()