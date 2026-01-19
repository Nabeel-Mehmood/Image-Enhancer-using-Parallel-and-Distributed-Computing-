import cv2
import numpy as np
import os
import time
from multiprocessing import Pool, cpu_count

# Paths
input_path = os.path.expanduser("C:\\User\\Desktop\\image.jpg")
output_dir = os.path.expanduser("C:\\User\\Desktop\\Multi processing Parts")  # Directory for parts

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def sharpness_adjustment(image):
    sharpening_kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])
    return cv2.filter2D(image, -1, sharpening_kernel)

def smoothing_denoising(image):
    gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)
    return cv2.bilateralFilter(gaussian_blur, d=9, sigmaColor=75, sigmaSpace=75)

def contrast_adjustment(image, factor=1.2):
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)

def process_image_part(image_part):
    """
    Enhances an image part by applying contrast adjustment, sharpening, and smoothing.
    """
    image_part = contrast_adjustment(image_part)
    image_part = sharpness_adjustment(image_part)
    image_part = smoothing_denoising(image_part)
    return image_part

def split_image(image):
    """
    Splits the image into four parts.
    """
    h, w = image.shape[:2]
    mid_h, mid_w = h // 2, w // 2
    parts = [
        image[:mid_h, :mid_w],  # Top-left
        image[:mid_h, mid_w:],  # Top-right
        image[mid_h:, :mid_w],  # Bottom-left
        image[mid_h:, mid_w:],  # Bottom-right
    ]
    return parts

def save_part(image_part, index):
    """
    Saves the enhanced image part to the output directory.
    """
    output_path = os.path.join(output_dir, f"enhanced_part_{index + 1}.jpg")
    cv2.imwrite(output_path, image_part)
    print(f"Part {index + 1} saved as {output_path}.")

if __name__ == "__main__":
    # Load the image
    image = cv2.imread(input_path)

    if image is None:
        print("Error: Could not open or find the image.")
    else:
        start_time = time.time()  # Start timing

        # Split the image into four parts
        image_parts = split_image(image)

        # Process the parts in parallel
        with Pool(processes=cpu_count()) as pool:
            processed_parts = pool.map(process_image_part, image_parts)

        # Save each enhanced part separately
        for i, part in enumerate(processed_parts):
            save_part(part, i)

        end_time = time.time()  # End timing
        elapsed_time = end_time - start_time

        print(f"Enhanced image parts saved in {output_dir}.")
        print(f"Time taken: {elapsed_time:.2f} seconds.")
