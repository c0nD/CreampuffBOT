import easyocr
import image_processor as ip
import os
from hit import Hit
import pandas as pd
import numpy as np
import cv2


def process_image(image_path, verbose=False):
    
    ip.isolate_damage(image_path)
    ip.isolate_username(image_path)
    ip.isolate_boss(image_path)
    ip.isolate_level(image_path, 'CreampuffBOT/temp/boss.jpg')
    ip.isolate_kills(image_path)
    ip.crop_boss('CreampuffBOT/temp/boss.jpg')  # correcting to actual boss name after isolating level

    
    temp_dir = "CreampuffBOT/temp/"
    upreprocessed_path = os.path.join(temp_dir, "username.jpg")
    dpreprocessed_path = os.path.join(temp_dir, "damage.jpg")
    bpreprocessed_path = os.path.join(temp_dir, "boss.jpg")
    lpreprocessed_path = os.path.join(temp_dir, "level.jpg")
    kpreprocessed_path = os.path.join(temp_dir, "kills.jpg")
    
    
    os.makedirs(temp_dir, exist_ok=True)
    
    reader = easyocr.Reader(['en', 'ch_sim'], verbose=False)  # you can change the languages according to your requirement
    
    ocr_username = reader.readtext(upreprocessed_path)
    ocr_damage = reader.readtext(dpreprocessed_path)
    ocr_boss = reader.readtext(bpreprocessed_path)
    ocr_level = reader.readtext(lpreprocessed_path)
    ocr_kills = process_kills_image(kpreprocessed_path)
    
# Create hits from OCR data and kill data
    hits = [Hit(u[1], d[1], b[1], l[1], k) for u, d, b, l, k in zip(ocr_username, ocr_damage, ocr_boss, ocr_level, ocr_kills)]    
    if verbose:
        for hit in hits:
            print(hit.serialize())
    return hits


def process_kills_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape

    # Calculate the pixel ranges for each region
    top_start = int(height * (280 / 1170))
    top_end = int(height * (480 / 1170))
    middle_start = int(height * (510 / 1170))
    middle_end = int(height * (740 / 1170))
    bottom_start = int(height * (770 / 1170))

    # Extract the regions from the image
    top = img[top_start:top_end, 0:width]
    middle = img[middle_start:middle_end, 0:width]
    bottom = img[bottom_start:height, 0:width]

    # Initialize the OCR reader
    reader = easyocr.Reader(['en'], verbose=False)

    # Read text from each region
    top_text = reader.readtext(top)
    middle_text = reader.readtext(middle)
    bottom_text = reader.readtext(bottom)

    target_words = ['enemy', 'defeated!']
    top_found = any(any(word.lower() in text[1].lower() for word in target_words) for text in top_text)
    middle_found = any(any(word.lower() in text[1].lower() for word in target_words) for text in middle_text)
    bottom_found = any(any(word.lower() in text[1].lower() for word in target_words) for text in bottom_text)

    return [top_found, middle_found, bottom_found]


def main():
    all_hits = []

    # Set this to True to process all images in directory, or False to process a single image
    process_all_images = True  # Change this to False to process single im

    path = "CreampuffBOT/imgs"
    if process_all_images:
        # Process all images in the directory
        for img_file in os.listdir(path):
            img_path = os.path.join(path, img_file)
            hits = process_image(img_path, verbose=False)
            all_hits.extend(hits)  # add hits to master list
            print("Hit count: ", len(hits))
    else:
        # Process a single image
        image_file = "IMG_7202.png"  # specify the file name here
        img_path = os.path.join(path, image_file)
        hits = process_image(img_path, verbose=False)
        all_hits.extend(hits)

    # You now have a list of all Hit objects in all_hits
    # Creating a pandas dataframe
    df = pd.DataFrame([(hit.username, hit.damage, hit.boss, hit.level, hit.kills) for hit in all_hits], 
                      columns=["Username", "Damage", "Boss", "Level", "Killed"])

    # Creating output directory if it doesn't exist
    output_dir = 'CreampuffBOT/out'
    os.makedirs(output_dir, exist_ok=True)
    
    # Saving the dataframe to a csv file
    df.to_csv(os.path.join(output_dir, 'output.csv'), index=False)
    print("Finished processing images")


if __name__ == "__main__":
    main()
