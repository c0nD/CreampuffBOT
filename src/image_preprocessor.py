import cv2
import numpy as np
import easyocr


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
    # Define lower and upper range for salmon-like color in BGR
    # For salmon color (RGB: 250, 128, 114), BGR would be (114, 128, 250)
    lower_red = np.array([100, 130, 200]) # Lower threshold
    upper_red = np.array([180, 160, 255]) # Upper threshold
    
    # Threshold the BGR image to get only salmon-like colors
    mask = cv2.inRange(image, lower_red, upper_red)
    
    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image, image, mask=mask)
    
    return result


def isolate_white_a(image):
    # Convert image from BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define lower and upper range for white color in HSV
    lower_white = np.array([0, 0, 235])
    upper_white = np.array([190, 25, 255])

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv_image, lower_white, upper_white)

    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image, image, mask=mask)
    
    return result


def isolate_white_b(image):
    # Convert image from BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper range for white color in HSV
    lower_white = np.array([0, 0, 225]) # pure white
    upper_white = np.array([170, 5, 255]) # pure white

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv_image, lower_white, upper_white)

    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image, image, mask=mask)

    return result


def isolate_green(image):
    # Convert image from BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper range for green color in HSV
    lower_green = np.array([30, 155, 200])
    upper_green = np.array([45, 220, 255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

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
    start_x = int(width * 340 / 1920)
    end_x = int(width * 650 / 1920)
    cropped_image = image[:, start_x:end_x]
    return cropped_image


# (return the center of the image, remove top and bottom 1/6)
def crop_center(image):
    height, width = image.shape[:2]
    start_y = height // 6
    end_y = height - start_y
    cropped_image = image[start_y:end_y, :]
    return cropped_image


def crop_kills(image):
    width = image.shape[1]
    start_x = 0
    end_x = int(width * 600 / 1920)
    cropped_image = image[:, start_x:end_x]
    return cropped_image


def crop_boss(image):
    width = image.shape[1]
    start_x = int(width * 650 / 1920)
    end_x = int(width * 875 / 1920)
    cropped_image = image[:, start_x:end_x]
    return cropped_image


def crop_level(image):
    width = image.shape[1]
    start_x = int(width * 600 / 1920)
    end_x = int(width * 1000 / 1920)
    cropped_image = image[:, start_x:end_x]
    return cropped_image


def remove_possible_padding(image):
    # Convert the image to grayscale if it's not already
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Threshold the grayscale image
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find the contours of the thresholded image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out very small contours based on the area
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]

    # If there are no contours left (image was mostly black)
    if len(contours) == 0:
        return image

    # Otherwise, find bounding box that fits around all contours
    x_min = min([cv2.boundingRect(cnt)[0] for cnt in contours])
    y_min = min([cv2.boundingRect(cnt)[1] for cnt in contours])
    x_max = max([cv2.boundingRect(cnt)[0] + cv2.boundingRect(cnt)[2] for cnt in contours])
    y_max = max([cv2.boundingRect(cnt)[1] + cv2.boundingRect(cnt)[3] for cnt in contours])

    # Crop the original image to this bounding box
    new_img = image[y_min:y_max, x_min:x_max]

    return new_img


def extend_mask_to_right(mask, extend_pixels=50):
    # Create an array of zeros (black) the same size as the mask
    extension = np.zeros(mask.shape, dtype=np.uint8)

    # Set the rightmost 'extend_pixels' columns of 'extension' to be white
    extension[:, -extend_pixels:] = 255

    # Combine the original mask and the extension using a bitwise OR operation
    extended_mask = cv2.bitwise_or(mask, extension)

    return extended_mask



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


def dilate_image(img, kernel_size=2):
    """Dilate image to separate characters."""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated_img = cv2.dilate(img, kernel, iterations=1)
    return dilated_img


def close_image(img, kernel_size=1):
    """Close image to fill in gaps."""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    closed_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return closed_img


def gaussian_blur(img, kernel_size=5):
    """Apply a Gaussian blur to an image."""
    blurred_img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    return blurred_img


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


def resize_image(img, width, height):
    # Calculate the target aspect ratio
    target_aspect = width / height
    # Calculate the aspect ratio of the input image
    img_aspect = img.shape[1] / img.shape[0]

    # If the input image's aspect ratio is greater than the target's,
    # that means it is wider. In this case, resize based on width.
    if img_aspect > target_aspect:
        img_resized = cv2.resize(img, (width, int(width / img_aspect)))
    else:
        # Otherwise, the input image is taller, so resize based on height.
        img_resized = cv2.resize(img, (int(height * img_aspect), height))
    
    # Calculate the color to use for padding. We'll use the mean color of the image.
    pad_color = 0
    
    # Get the size of the resized image
    y_resized, x_resized, _ = img_resized.shape
    
    # Create a new, blank image with the target size and fill it with the pad color
    img_target = np.full((height, width, 3), pad_color, dtype=np.uint8)
    
    # Compute x and y offsets to center the resized image
    y_offset = (height - y_resized) // 2
    x_offset = (width - x_resized) // 2
    
    # Insert the resized image into the center of the target image
    img_target[y_offset:y_offset+y_resized, x_offset:x_offset+x_resized] = img_resized
    
    return img_target
