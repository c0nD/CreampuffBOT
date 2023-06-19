import cv2
from display import display
import image_preprocessor as pi
import numpy as np

def isolate_damage(path):
    
    img = cv2.imread(path)
    img = pi.remove_possible_padding(img)
    
    print("Image Loaded: ", img is not None)
    
    cv2.imwrite('CreampuffBOT/temp/damage.jpg', img)
    img = pi.crop_right(img)  # right quarter
    img = pi.crop_center(img)  # top/bottom 1/6
    img = pi.isolate_yellow(img)
    img = pi.grayscale(img)
    img = pi.binarize(img)
    img = pi.noise_removal(img)
    img = pi.sharpen_image(img)
    
    
    # Save & display image
    cv2.imwrite('CreampuffBOT/temp/damage.jpg', img)
    #display('CreampuffBOT/temp/damage.jpg')
    
    
def isolate_username(path):
    
    img = cv2.imread(path)
    img = pi.remove_possible_padding(img)
    
    img = pi.crop_left(img)
    img = pi.crop_center(img)
    img = pi.isolate_white_a(img)
    img = pi.grayscale(img)
    img = pi.binarize(img)
    img = pi.noise_removal(img)
    img = pi.add_padding(img, left=100, right=100)
    img = pi.thick_font(img)
    img = pi.gaussian_blur(img)
    img = pi.sharpen_image(img)
    
    # Save & display image
    cv2.imwrite('CreampuffBOT/temp/username.jpg', img)
    #display('CreampuffBOT/temp/username.jpg')
    
    
def isolate_boss(path):
    
    img = cv2.imread(path)
    img = pi.remove_possible_padding(img)
    img = pi.crop_center(img)
    
    img = pi.isolate_red(img)
    img = pi.grayscale(img)
    img = pi.binarize(img)
    img = pi.noise_removal(img)
    img = pi.add_padding(img, left=100, right=50)
    
    # Save & display image
    cv2.imwrite('CreampuffBOT/temp/boss.jpg', img)
    #display('CreampuffBOT/temp/boss.jpg')
    
    
def crop_boss(path):
    img = cv2.imread(path)
    img = pi.crop_boss(img)
    cv2.imwrite('CreampuffBOT/temp/boss.jpg', img)
    
    
def isolate_level(path, boss_path):

    # Load the image
    img = cv2.imread(path)
    img = pi.remove_possible_padding(img)
    
    # Load the boss image
    boss_img = cv2.imread(boss_path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale

    # Preprocess original image to isolate white pixels
    img_white = pi.crop_center(img)
    img_white = pi.isolate_white_b(img_white)
    img_white = pi.grayscale(img_white)
    img_white = pi.binarize(img_white)
    img_white = pi.noise_removal(img_white)

    # Find contours in the boss image
    contours, _ = cv2.findContours(boss_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an empty mask to store our final result
    mask = np.zeros_like(img_white)

    for contour in contours:
        # Compute the bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Extend the bounding box to the right
        x_start = x + w
        x_end = x_start + 60  # Extend more to the right to ensure all text is included

        # Increase the height of the bounding box to ensure all text is included
        y -= 10  # Shift the box up a bit
        h += 25  # Increase the total height a bit

        # Ensure we don't go beyond the image boundaries
        y = max(0, y)
        h = min(img_white.shape[0] - y, h)

        # Define the region of interest (ROI) on the white image
        roi = img_white[y:y+h, x_start:x_end]

        # Add the ROI to our final mask
        mask[y:y+h, x_start:x_end] = roi

    # Add padding
    mask = pi.add_padding(mask, left=100, right=50)
    mask = pi.crop_level(mask)
    mask = pi.noise_removal(mask)

    # Save & display image
    cv2.imwrite('CreampuffBOT/temp/level.jpg', mask)
    #display('CreampuffBOT/temp/level.jpg')


def isolate_kills(path):
    
    img = cv2.imread(path)
    img = pi.remove_possible_padding(img)
    img = pi.isolate_green(img)
    
    img = pi.crop_kills(img)
    img = pi.grayscale(img)
    img = pi.binarize(img)
    img = pi.noise_removal(img)
    img = pi.add_padding(img, left=100, right=50)
    
    # Save & display image
    cv2.imwrite('CreampuffBOT/temp/kills.jpg', img)
    #display('CreampuffBOT/temp/kills.jpg')