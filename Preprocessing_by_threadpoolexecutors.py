import cv2
import numpy as np
import os
import time
from concurrent.futures import ThreadPoolExecutor

# Paths
input_path = os.path.expanduser("C:\\User\\Desktop\\image.jpg")
output_dir = os.path.expanduser("C:\\User\\Desktop\\Threadpool Executor Parts")  # Directory to save parts

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def sharpness_adjustment(image):
    """
    Adjusts the sharpness of the image to enhance details.
    """
    sharpening_kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])
    return cv2.filter2D(image, -1, sharpening_kernel)

def smoothing_denoising(image):
    """
    Applies a series of smoothing and denoising techniques to reduce noise while preserving edges.
    """
    gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)
    return cv2.bilateralFilter(gaussian_blur, d=9, sigmaColor=75, sigmaSpace=75)

def contrast_adjustment(image, factor=1.2):
    """
    Adjusts the contrast of the image to enhance visibility of features.
    """
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)

def split_image(image):
    """
    Splits the image into four equal parts.
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

def enhance_and_save(image_part, part_index, output_dir):
    """
    Enhances the given image part and saves it to the output directory.
    """
    image_part = contrast_adjustment(image_part)
    image_part = sharpness_adjustment(image_part)
    image_part = smoothing_denoising(image_part)
    output_path = os.path.join(output_dir, f"enhanced_part_{part_index + 1}.jpg")
    cv2.imwrite(output_path, image_part)
    print(f"Part {part_index + 1} enhanced and saved as {output_path}.")

if __name__ == "__main__":
    # Load the image
    image = cv2.imread(input_path)

    if image is None:
        print("Error: Could not open or find the image.")
    else:
        start_time = time.time()  # Start timing

        # Split the image into four parts
        image_parts = split_image(image)

        # Process the parts in parallel using threads
        with ThreadPoolExecutor(max_workers=4) as executor:
            workers = [
                executor.submit(enhance_and_save, part, i, output_dir)
                for i, part in enumerate(image_parts)
            ]

        # Wait for all threads to complete
        for worker in workers:
            worker.result()

        end_time = time.time()  # End timing

        # Calculate and display time taken
        elapsed_time = end_time - start_time
        print(f"Image split, enhanced, and parts saved in '{output_dir}'.")
        print(f"Time taken: {elapsed_time:.2f} seconds.")
