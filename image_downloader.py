from icrawler.builtin import GoogleImageCrawler

def download_cat_images(breeds, max_num, root_dir):
    """
    Downloads a specified number of large-sized images for a list of cat breeds.

    Args:
        breeds (list): A list of cat breed names (keywords for searching).
        max_num (int): The maximum number of images to download for each breed.
        root_dir (str): The root directory to save the images.
    """
    for breed in breeds:
        print(f'Downloading {max_num} large images for: {breed}')
        # The storage path will be root_dir/breed_name
        storage_path = f'{root_dir}/{breed.replace(" ", "_")}'
        google_crawler = GoogleImageCrawler(
            parser_threads=2,
            downloader_threads=4,
            storage={'root_dir': storage_path}
        )
        
        # Define search filters
        filters = {
            'size': 'medium',  # Download large images
            'type': 'photo'   # Search for photos
        }

        try:
            google_crawler.crawl(keyword=breed, max_num=max_num, filters=filters)
            print(f'Finished downloading for: {breed}\n')
        except Exception as e:
            print(f'An error occurred while downloading for {breed}: {e}\n')

if __name__ == "__main__":
    # The root directory for all downloaded images
    main_download_dir = 'indirilen_gorseller'

    # List of cat breeds to download
    cat_breeds = [
        "Siamese cat",
        "British Shorthair cat",
        "Maine Coon cat",
        "Persian cat",
        "American Curl cat"
    ]

    # Number of images to download for each breed
    images_per_breed = 300

    download_cat_images(
        breeds=cat_breeds, 
        max_num=images_per_breed, 
        root_dir=main_download_dir
    )

    print(f"All image downloads are complete. Check the '{main_download_dir}' directory.")

