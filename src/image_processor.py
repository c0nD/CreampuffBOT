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
    #display('CreampuffBOT/temp/damage.jpg')
    
    
def isolate_username(path):
    
    img = cv2.imread(path)
    
    img = pi.crop_left(img)
    img = pi.crop_center(img)
    img = pi.isolate_white(img)
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
    
    img = pi.crop_boss(img)
    img = pi.crop_center(img)
    img = pi.isolate_red(img)
    img = pi.grayscale(img)
    img = pi.binarize(img)
    img = pi.noise_removal(img)
    img = pi.add_padding(img, left=100, right=50)
    
    # Save & display image
    cv2.imwrite('CreampuffBOT/temp/boss.jpg', img)
    #display('CreampuffBOT/temp/boss.jpg')