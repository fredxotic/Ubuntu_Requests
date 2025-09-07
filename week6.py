import os
import requests
import urllib.parse
from requests.exceptions import RequestException

def download_image(url):
    # 1. Define the directory and create it if it doesn't exist
    output_dir = "Fetched_Images"
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Directory '{output_dir}' ensured to exist.")
    except OSError as e:
        print(f"Error creating directory: {e}")
        return

    # 2. Extract a filename from the URL or generate a generic one
    try:
        path = urllib.parse.urlparse(url).path
        filename = os.path.basename(path)
        if not filename or '.' not in filename:
            # Generate a generic filename if the URL doesn't have one
            print("Could not find a valid filename in the URL. Generating one...")
            filename = "downloaded_image.jpg"
            
        filepath = os.path.join(output_dir, filename)
    except Exception as e:
        print(f"Could not parse URL or generate filename: {e}")
        return

    print(f"Attempting to download from {url}...")

    # 3. Handle the request and potential errors
    try:
        response = requests.get(url, stream=True) 
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Image successfully downloaded and saved as '{filepath}'")

    except RequestException as e:
        print(f"An error occurred during the request: {e}")
    except IOError as e:
        print(f"An I/O error occurred while saving the file: {e}")

if __name__ == "__main__":
    image_url = input("Please enter the URL of the image you want to download: ").strip()
    if image_url:
        download_image(image_url)
    else:
        print("No URL provided. Exiting.")
