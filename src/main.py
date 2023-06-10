import easyocr
import image_processor as ip
import os
from hit import Hit
import pandas as pd
from PIL import Image

def process_image(image_path, verbose=False):
    ip.isolate_damage(image_path)
    ip.isolate_username(image_path)
    ip.isolate_boss(image_path)
    
    temp_dir = "CreampuffBOT/temp/"
    upreprocessed_path = os.path.join(temp_dir, "username.jpg")
    dpreprocessed_path = os.path.join(temp_dir, "damage.jpg")
    bpreprocessed_path = os.path.join(temp_dir, "boss.jpg")
    
    os.makedirs(temp_dir, exist_ok=True)
    
    reader = easyocr.Reader(['en', 'ch_sim'])  # you can change the languages according to your requirement
    
    ocr_username = reader.readtext(upreprocessed_path)
    ocr_damage = reader.readtext(dpreprocessed_path)
    ocr_boss = reader.readtext(bpreprocessed_path)

    hits = [Hit(u[1], d[1], b[1]) for u, d, b in zip(ocr_username, ocr_damage, ocr_boss)]
    
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
            hits = process_image(img_path, verbose=False)
            all_hits.extend(hits)  # add hits to master list
            print("Hit count: ", len(hits))
    else:
        # Process a single image
        image_file = "damage1.jpg"  # specify the file name here
        img_path = os.path.join(path, image_file)
        hits = process_image(img_path, verbose=False)
        all_hits.extend(hits)

    # You now have a list of all Hit objects in all_hits
    # Creating a pandas dataframe
    df = pd.DataFrame([(hit.username, hit.damage, hit.boss) for hit in all_hits], 
                      columns=["Username", "Damage", "Boss"])

    # Sorting dataframe by boss and username
    df_sorted = df.sort_values(by=['Boss', 'Username'])

    # Creating output directory if it doesn't exist
    output_dir = 'CreampuffBOT/out'
    os.makedirs(output_dir, exist_ok=True)
    
    # Saving the dataframe to a csv file
    df_sorted.to_csv(os.path.join(output_dir, 'output.csv'), index=False)


if __name__ == "__main__":
    main()
