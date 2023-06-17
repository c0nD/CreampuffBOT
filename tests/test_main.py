# test_main.py

import os
import sys
import pandas as pd
import unittest
import easyocr
from PIL import Image

# Add the parent directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import necessary modules
from src.image_processor import isolate_damage, isolate_username, isolate_boss
from src.hit import Hit

class TestMain(unittest.TestCase):

    def setUp(self):
        self.temp_dir = "tests/test_temp/"
        self.test_imgs_path = "tests/test_imgs/"
        self.output_path = "tests/test_out.csv"
        os.makedirs(self.temp_dir, exist_ok=True)
        self.reader = easyocr.Reader(['en', 'ch_sim'], verbose=False)  # you can change the languages according to your requirement

    def process_image(self, image_path, verbose=False):
        isolate_damage(image_path)
        isolate_username(image_path)
        isolate_boss(image_path)

        upreprocessed_path = os.path.join(self.temp_dir, "username.jpg")
        dpreprocessed_path = os.path.join(self.temp_dir, "damage.jpg")
        bpreprocessed_path = os.path.join(self.temp_dir, "boss.jpg")

        ocr_username = self.reader.readtext(upreprocessed_path)
        ocr_damage = self.reader.readtext(dpreprocessed_path)
        ocr_boss = self.reader.readtext(bpreprocessed_path)

        hits = [Hit(u[1], d[1], b[1]) for u, d, b in zip(ocr_username, ocr_damage, ocr_boss)]
    
        if verbose:
            for hit in hits:
                print(hit.serialize())
        return hits

    def test_process_image(self):
        all_hits = []
        # Process all images in the test directory
        for img_file in os.listdir(self.test_imgs_path):
            img_path = os.path.join(self.test_imgs_path, img_file)
            hits = self.process_image(img_path, verbose=False)
            all_hits.extend(hits)  # add hits to master list
            print("Hit count: ", len(hits))

        # You now have a list of all Hit objects in all_hits
        # Creating a pandas dataframe
        df = pd.DataFrame([(hit.username, hit.damage, hit.boss) for hit in all_hits], 
                          columns=["Username", "Damage", "Boss"])

        # Sorting dataframe by boss and username
        df_sorted = df.sort_values(by=['Boss', 'Username'])

        # Saving the dataframe to a csv file
        df_sorted.to_csv(os.path.join(self.temp_dir, 'test_output.csv'), index=False)

        # Compare output file with expected output file
        df_test = pd.read_csv(os.path.join(self.temp_dir, 'test_output.csv'))
        df_expected = pd.read_csv(self.output_path)

        pd.testing.assert_frame_equal(df_test, df_expected)

if __name__ == '__main__':
    unittest.main()
