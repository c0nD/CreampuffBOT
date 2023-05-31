import cv2
from display import display
import image_preprocessor as pi

def isolate_damage(path):
    
    
    img = cv2.imread(path)
    
    print("Image Loaded: ", img is not None)
    
    img = pi.crop_right(img)  # right quarter
    img = pi.crop_center(img)  # top/bottom 1/6
    img = pi.isolate_yellow(img)
    img = pi.grayscale(img)
    img = pi.binarize(img)
    img = pi.noise_removal(img)
    img = pi.sharpen_image(img)
    
    
    # Save & display image
    cv2.imwrite('CreampuffBOT/temp/damage.jpg', img)
    display('CreampuffBOT/temp/damage.jpg')
    