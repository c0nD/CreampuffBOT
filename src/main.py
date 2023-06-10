import cv2
import pytesseract
from PIL import Image
import image_processor as ip
import os
from hit import Hit
import easyocr

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
    "--oem 3 "
    "-l eng+kor+chi_sim "
    "--user-words CreampuffBOT/ocr/words.txt "
    "--psm 6 "
    "-c tessdict_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_#"
    )

    ocr_username = pytesseract.image_to_string(Image.open(upreprocessed_path), config=config)
    ocr_damage = pytesseract.image_to_string(Image.open(dpreprocessed_path), config=config)
    ocr_boss = pytesseract.image_to_string(Image.open(bpreprocessed_path), config=config)
    
    ocr_username_lines = ocr_username.splitlines()
    ocr_damage_lines = ocr_damage.splitlines()
    ocr_boss_lines = ocr_boss.splitlines()
    
    hits = [Hit(u, d, b) for u, d, b in zip(ocr_username_lines, ocr_damage_lines, ocr_boss_lines)]
    
    if verbose:
        for hit in hits:
            print(hit.serialize())
    return hits


def main():
    all_hits = []

    # Set this to True to process all images in directory, or False to process a single image
    process_all_images = True  # Change this to False to process single im

    path = "CreampuffBOT/imgs"
    if process_all_images:
        # Process all images in the directory
        for img_file in os.listdir(path):
            img_path = os.path.join(path, img_file)
            hits = process_image(img_path, verbose=True)
            all_hits.extend(hits)  # add hits to master list
    else:
        # Process a single image
        image_file = "damage1.jpg"  # specify the file name here
        img_path = os.path.join(path, image_file)
        hits = process_image(img_path, verbose=True)
        all_hits.extend(hits)

    # You now have a list of all Hit objects in all_hits

if __name__ == "__main__":
    main()
