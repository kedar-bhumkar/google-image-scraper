# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
#Import libraries
import os
import argparse        
import random
import string
from datetime import datetime

from GoogleImageScraper import GoogleImageScraper
from patch import webdriver_executable


def worker_thread(search_key, custom_url=None):
    image_scraper = GoogleImageScraper(
        webdriver_path, 
        image_path, 
        search_key, 
        number_of_images, 
        headless, 
        min_resolution, 
        max_resolution, 
        max_missed,
        custom_url)
    print("Processing search key:", search_key)
    image_urls = image_scraper.find_image_urls()
    print("Found", len(image_urls), "images for", search_key)
    image_scraper.save_images(image_urls, keep_filenames)
    print("Completed processing for:", search_key)
    #Release resources
    del image_scraper

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Google Image Scraper')
    parser.add_argument('--url', type=str, help='Custom URL to scrape images from')
    parser.add_argument('--search_keys', type=str, help='Comma-separated list of search keys (e.g., "cat,dog,bird")')
    parser.add_argument('--number_of_images', type=int, help='Number of images to scrape')
    args = parser.parse_args()

    #Define file path
    print("Starting Google Image Scraper...")
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    print("WebDriver path:", webdriver_path)
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))
    print("Image path:", image_path)
    
    #Parse search keys from command line or use default
    if args.search_keys:
        search_keys = [key.strip() for key in args.search_keys.split(',')]
        search_keys = list(set(search_keys))  # Remove duplicates
    else:
        #Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        temp_key = f"temp-{timestamp}-{random_suffix}"
        search_keys = [temp_key]

    #Parameters
    number_of_images = args.number_of_images or 50                # Desired number of images
    headless = False                    # True = No Chrome GUI
    min_resolution = (0, 0)             # Minimum desired image resolution
    max_resolution = (9999, 9999)       # Maximum desired image resolution
    max_missed = 10                     # Max number of failed images before exit
    keep_filenames = False              # Keep original URL image filenames

    #Run each search_key sequentially (synchronous)
    print("Processing search keys sequentially...")
    for search_key in search_keys:
        print(f"\n--- Processing: {search_key} ---")
        worker_thread(search_key, args.url)
    
    print("\nAll search keys processed successfully!")
