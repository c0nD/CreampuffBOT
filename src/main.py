import cv2
import pytesseract
from PIL import Image
import image_processor as ip
import os
from hit import Hit

def process_image(image_path, verbose=False):
    ip.isolate_damage(image_path)
    ip.isolate_username(image_path)
    ip.isolate_boss(image_path)
    
    temp_dir = "CreampuffBOT/temp/"
    upreprocessed_path = os.path.join(temp_dir, "username.jpg")
    dpreprocessed_path = os.path.join(temp_dir, "damage.jpg")
    bpreprocessed_path = os.path.join(temp_dir, "boss.jpg")
    
    os.makedirs(temp_dir, exist_ok=True)
    
    config = (
    "--user-words CreampuffBOT/ocr/words.txt "
    "--psm 6 "
    "-c tessdict_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_#"
    )
    ocr_username = pytesseract.image_to_string(Image.open(upreprocessed_path), config=config)
    ocr_damage = pytesseract.image_to_string(Image.open(dpreprocessed_path), config=config)
    ocr_boss = pytesseract.image_to_string(Image.open(bpreprocessed_path), config=config)
    
    hits = [Hit(u, d, b) for u, d, b in zip(ocr_username.splitlines(), ocr_damage.splitlines(), ocr_boss.splitlines())]
    
    if verbose:
        for hit in hits:
            print(hit.serialize())
    return hits

def main():
    img_folder = "CreampuffBOT/imgs"
    all_hits = []

    # Process all images in the img_folder
    for img_file in os.listdir(img_folder):
        img_path = os.path.join(img_folder, img_file)
        hits = process_image(img_path, verbose=True)
        all_hits.extend(hits)  # add hits to master list


if __name__ == "__main__":
    main()
