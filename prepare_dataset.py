import os
import shutil
import glob

def create_dir_if_not_exists(path):
    """Creates a directory if it does not already exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def prepare_dataset(source_root, dest_root, val_split_count):
    """
    Organizes downloaded images into a dataset structure for model training.

    Args:
        source_root (str): The root directory of the downloaded images.
        dest_root (str): The root directory for the new dataset structure.
        val_split_count (int): The number of images per class for the validation set.
    """
    if not os.path.exists(source_root):
        print(f"Hata: Kaynak klasör '{source_root}' bulunamadı. Lütfen önce resimleri indirin.")
        return

    # Define and create the directory structure
    subdirs = ['images', 'labels']
    splits = ['train', 'val']
    for subdir in subdirs:
        for split in splits:
            create_dir_if_not_exists(os.path.join(dest_root, subdir, split))

    # Get the list of breed directories
    breed_dirs = [d for d in os.listdir(source_root) if os.path.isdir(os.path.join(source_root, d))]

    for breed in breed_dirs:
        print(f'Processing breed: {breed}')
        # Create breed subdirectories in the new structure
        for subdir in subdirs:
            for split in splits:
                create_dir_if_not_exists(os.path.join(dest_root, subdir, split, breed))

        # Get all images for the current breed
        image_paths = glob.glob(os.path.join(source_root, breed, '*'))
        image_paths.sort() # Sort to ensure consistency

        # Split images into training and validation sets
        train_count = len(image_paths) - val_split_count
        if train_count < 0:
            train_count = 0 # Ensure train_count is not negative
        
        train_images = image_paths[:train_count]
        val_images = image_paths[train_count:]

        # Move training images
        for img_path in train_images:
            shutil.move(img_path, os.path.join(dest_root, 'images', 'train', breed, os.path.basename(img_path)))
        
        # Move validation images
        for img_path in val_images:
            shutil.move(img_path, os.path.join(dest_root, 'images', 'val', breed, os.path.basename(img_path)))
        
        print(f'  - Moved {len(train_images)} images to train set.')
        print(f'  - Moved {len(val_images)} images to validation set.')

    print(f"\nVeri seti '{dest_root}' klasöründe başarıyla oluşturuldu.")
    # Clean up the now-empty source directory
    shutil.rmtree(source_root)
    print(f"Eski '{source_root}' klasörü temizlendi.")


if __name__ == '__main__':
    source_directory = 'indirilen_gorseller'
    dataset_directory = 'dataset'
    val_count = 4

    prepare_dataset(source_directory, dataset_directory, val_count)
