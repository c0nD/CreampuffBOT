import cv2
import numpy as np


def isolate_yellow(image):
    # Convert image from BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define lower and upper range for yellow color in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image, image, mask=mask)
    
    return result


def crop_right(image):
    width = image.shape[1]
    start_x = width * 3 // 4
    cropped_image = image[:, start_x:]
    return cropped_image


def crop_left(image):
    width = image.shape[1]
    start_x = width // 4
    cropped_image = image[:, start_x:]
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