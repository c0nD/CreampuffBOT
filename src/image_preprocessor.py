import cv2
import numpy as np


def isolate_yellow(image):
    # Convert image from BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define lower and upper range for yellow color in HSV
    lower_yellow = np.array([27, 100, 100])
    upper_yellow = np.array([37, 255, 255])

    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image, image, mask=mask)
    
    return result


def isolate_red(image):
    # Convert image from BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define lower and upper range for red color in HSV (specific red is  (208,126,127).)
    # Isolating a 'salmon' like color
    lower_red = np.array([0, 85, 100])
    upper_red = np.array([7, 100, 250])
    
    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv_image, lower_red, upper_red)
    
    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image, image, mask=mask)
    
    return result


def isolate_white(image):
    # Convert image from BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define lower and upper range for white color in HSV
    lower_white = np.array([0, 0, 235])
    upper_white = np.array([180, 25, 255])

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv_image, lower_white, upper_white)

    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image, image, mask=mask)
    
    return result


def crop_right(image):
    width = image.shape[1]
    start_x = width * 5 // 8
    cropped_image = image[:, start_x:]
    return cropped_image


# obtain the second fifth of the image
def crop_left(image):
    width = image.shape[1]
    start_x = int(width * 350 / 1920)
    end_x = int(width * 560 / 1920)
    cropped_image = image[:, start_x:end_x]
    return cropped_image


# (return the center of the image, remove top and bottom 1/6)
def crop_center(image):
    height, width = image.shape[:2]
    start_y = height // 6
    end_y = height - start_y
    cropped_image = image[start_y:end_y, :]
    return cropped_image


def crop_boss(image):
    width = image.shape[1]
    start_x = int(width * 650 / 1920)
    end_x = int(width * 875 / 1920)
    cropped_image = image[:, start_x:end_x]
    return cropped_image


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Black and white
def binarize(image):
    return cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)[1]

def noise_removal(image):
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image
    
    
def thin_font(image):
    image = cv2.bitwise_not(image)    
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image


def thick_font(image):
    image = cv2.bitwise_not(image)    
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

    
def remove_border(image):
    countours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntSorted = sorted(countours, key=lambda x: cv2.contourArea(x))
    cnt = cntSorted[-1]  # largest bounding box
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y + h, x:x + w]
    return crop
    
    
def remove_largest_bounding_box(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt_sorted = sorted(contours, key=lambda x: cv2.contourArea(x))
    cnt = cnt_sorted[-1]  # largest bounding box
    x, y, w, h = cv2.boundingRect(cnt)
    
    # Create a mask with the same size as the input image and fill it with white color (255)
    mask = np.full(image.shape, 255, dtype=np.uint8)
    
    # Draw the largest bounding box as a filled rectangle on the mask with black color (0)
    cv2.rectangle(mask, (x, y), (x + w, y + h), (0), -1)
    
    # Apply the mask to the input image using bitwise_and
    result = cv2.bitwise_and(image, mask)
    return result


def remove_thin_borders(image, black_threshold=10, black_percentage=0.9):
    # Convert the image to grayscale if it's not already
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image.copy()
    
    height, width = gray_image.shape
    left, right = 0, width - 1
    
    # Find the left border
    for col in range(width):
        if np.sum(gray_image[:, col] < black_threshold) / height < black_percentage:
            left = col
            break
            
    # Find the right border
    for col in range(width - 1, 0, -1):
        if np.sum(gray_image[:, col] < black_threshold) / height < black_percentage:
            right = col
            break
            
    # Crop the image, removing the left and right borders
    cropped_image = image[:, left:right + 1]
    return cropped_image


def sharpen_image(image):
    # Define the sharpening kernel
    sharpening_kernel = np.array([[-1, -1, -1],
                                  [-1,  9, -1],
                                  [-1, -1, -1]])

    # Apply the kernel to the image using filter2D
    sharpened_image = cv2.filter2D(image, -1, sharpening_kernel)

    return sharpened_image


def add_padding(image, left=100, top=0, right=0, bottom=0):
    """Adds padding to an image."""
    return cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)



def thin_font(image):
    image = cv2.bitwise_not(image)    
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image


def thick_font(image):
    image = cv2.bitwise_not(image)    
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image