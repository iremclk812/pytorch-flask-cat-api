import os
import shutil
import glob

def adjust_train_val_split(breed_name, target_train_count):
    """Adjusts the number of images in the training set for a specific breed."""
    dataset_root = 'dataset'
    train_dir = os.path.join(dataset_root, 'images', 'train', breed_name)
    val_dir = os.path.join(dataset_root, 'images', 'val', breed_name)

    if not os.path.exists(train_dir):
        print(f"Hata: Eğitim klasörü bulunamadı: {train_dir}")
        return

    # Get all images in the training directory
    train_images = sorted(glob.glob(os.path.join(train_dir, '*')))
    current_train_count = len(train_images)

    if current_train_count <= target_train_count:
        print(f"'{breed_name}' için zaten {target_train_count} veya daha az resim var. İşlem yapılmadı.")
        return

    # Calculate how many images to move
    num_to_move = current_train_count - target_train_count
    images_to_move = train_images[-num_to_move:]

    print(f"'{breed_name}' için {num_to_move} resim train'den val'e taşınıyor...")
    for img_path in images_to_move:
        shutil.move(img_path, os.path.join(val_dir, os.path.basename(img_path)))
    
    print(f"Taşıma tamamlandı. '{breed_name}' için yeni train sayısı: {len(os.listdir(train_dir))}, yeni val sayısı: {len(os.listdir(val_dir))}")

if __name__ == '__main__':
    breeds_to_adjust = {
        "British_Shorthair_cat": 51,
        "Persian_cat": 51
    }

    for breed, count in breeds_to_adjust.items():
        adjust_train_val_split(breed, count)
