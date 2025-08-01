import io
import os
from flask import Flask, request, jsonify
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn.functional as F

app = Flask(__name__)

# --- Sabitler ve Ayarlar ---
MODEL_PATH = 'cat_breed_classifier.pth'
DATA_DIR = os.path.join('dataset', 'images', 'train')

# Sınıf isimlerini dinamik olarak eğitim klasöründen al
try:
    CLASS_NAMES = sorted([d.name for d in os.scandir(DATA_DIR) if d.is_dir()])
    NUM_CLASSES = len(CLASS_NAMES)
    print(f"Sınıflar bulundu: {CLASS_NAMES}")
except FileNotFoundError:
    print(f"HATA: Eğitim verisi klasörü bulunamadı: '{DATA_DIR}'")
    CLASS_NAMES = []
    NUM_CLASSES = 0

# --- Modeli Tanımla ve Yükle ---
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model():
    # Modeli tanımla (ResNet34)
    model = models.resnet34(weights=None) # Önce boş başlat
    if NUM_CLASSES > 0:
        num_ftrs = model.fc.in_features
        model.fc = torch.nn.Linear(num_ftrs, NUM_CLASSES)
    else:
        print("UYARI: Sınıflar bulunamadığı için modelin son katmanı ayarlanamadı.")

    # Kayıtlı model ağırlıklarını yükle
    try:
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        print(f"Model ağırlıkları başarıyla yüklendi: '{MODEL_PATH}'")
    except FileNotFoundError:
        print(f"UYARI: Model dosyası bulunamadı: '{MODEL_PATH}'. Sunucu boş modelle çalışacak.")
    except RuntimeError as e:
        print(f"HATA: Model yüklenirken mimari uyuşmazlığı oldu. Sınıf sayısı veya model tipi yanlış olabilir. {e}")

    model.to(device)
    model.eval()
    return model

model = load_model()

# --- Görüntü Dönüşümleri ---
def transform_image(image_bytes):
    my_transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return my_transforms(image).unsqueeze(0)

# --- API Uç Noktası ---
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'Lütfen bir dosya yükleyin'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi'}), 400

    try:
        img_bytes = file.read()
        tensor = transform_image(img_bytes)
        tensor = tensor.to(device)

        with torch.no_grad():
            outputs = model(tensor)
            probabilities = F.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
            predicted_class = CLASS_NAMES[predicted_idx.item()]
            confidence_score = confidence.item()

        # Güven skorunu saf ondalık sayı olarak gönder (String değil, doğrudan sayı)
        return jsonify({
            'prediction': predicted_class,
            'confidence': f'{confidence_score:.4f}'
        })

    except Exception as e:
        return jsonify({'error': f'Tahmin sırasında bir hata oluştu: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Flask server... Go to http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
