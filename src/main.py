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
    
    reader = easyocr.Reader(['en', 'ch_sim'], verbose=False)  # Specify the language(s) and set verbose to False

    ocr_username = reader.readtext(upreprocessed_path)
    ocr_damage = reader.readtext(dpreprocessed_path)
    ocr_boss = reader.readtext(bpreprocessed_path)
    
    # EasyOCR returns a list of tuples, each containing the coordinates of the text
    # and the text itself. We extract just the text and join it into a single string.
    ocr_username_lines = [' '.join(result[1] for result in ocr_username)]
    ocr_damage_lines = [' '.join(result[1] for result in ocr_damage)]
    ocr_boss_lines = [' '.join(result[1] for result in ocr_boss)]
    
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
