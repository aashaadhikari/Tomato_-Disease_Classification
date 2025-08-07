#!/usr/bin/env python3
"""
Test script for plant detection functionality
"""

import cv2
import numpy as np
import os
from PIL import Image

def is_plant_image(image_path):
    """
    Basic plant detection using color analysis and edge detection.
    This is a simple heuristic - for production, you'd want a dedicated plant detection model.
    """
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            return False
        
        # Convert to different color spaces
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Define green color range (plants are typically green)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        
        # Create mask for green regions
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Calculate percentage of green pixels
        total_pixels = image.shape[0] * image.shape[1]
        green_pixels = cv2.countNonZero(green_mask)
        green_percentage = (green_pixels / total_pixels) * 100
        
        # Edge detection to find leaf-like structures
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Calculate edge density
        edge_pixels = cv2.countNonZero(edges)
        edge_percentage = (edge_pixels / total_pixels) * 100
        
        # Simple heuristic: if there's significant green color and some edges, it might be a plant
        is_likely_plant = green_percentage > 15 and edge_percentage > 2
        
        print(f"Image: {image_path}")
        print(f"  Green percentage: {green_percentage:.2f}%")
        print(f"  Edge percentage: {edge_percentage:.2f}%")
        print(f"  Is likely plant: {is_likely_plant}")
        print()
        
        return is_likely_plant
        
    except Exception as e:
        print(f"Error in plant detection: {e}")
        return False

def test_plant_detection():
    """Test the plant detection with sample images"""
    
    # Test with some sample images if they exist
    test_images = [
        "static/uploads/test_plant.jpg",
        "static/uploads/test_non_plant.jpg",
        "static/uploads/sample_leaf.jpg"
    ]
    
    print("Testing plant detection functionality...")
    print("=" * 50)
    
    for image_path in test_images:
        if os.path.exists(image_path):
            result = is_plant_image(image_path)
            print(f"Result for {image_path}: {'PLANT' if result else 'NOT PLANT'}")
        else:
            print(f"Test image not found: {image_path}")
    
    print("\n" + "=" * 50)
    print("Plant detection test completed!")
    print("\nNote: This is a basic heuristic-based detection.")
    print("For production use, consider training a dedicated plant detection model.")

if __name__ == "__main__":
    test_plant_detection() 