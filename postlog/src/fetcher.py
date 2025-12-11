import requests
import json
import os
from typing import List, Dict, Any


API_URL = "https://jsonplaceholder.typicode.com/posts"
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw_posts.json")


def fetch_posts(limit: int = 100) -> List[Dict[str, Any]]:
    print(f"-> {API_URL} adresinden {limit} adet post çekiliyor...")
    TIMEOUT_SECONDS = 10

    try:
        response = requests.get(API_URL, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()

    except requests.exceptions.Timeout:
        print(
            f" Hata: API'ye bağlanırken zaman aşımı ({TIMEOUT_SECONDS} saniye) oluştu. İnternet bağlantınızı kontrol edin.")
        return []

    except requests.exceptions.HTTPError as err:
        print(f"Hata: HTTP isteği başarısız oldu. Durum Kodu: {response.status_code}")
        print(f"Detay: {err}")
        return []

    except requests.exceptions.RequestException as e:
        print(f" Hata: İstek sırasında beklenmedik bir hata oluştu: {e}")
        return []

    try:
        data = response.json()

        if not isinstance(data, list):
            print("Hata: API'den beklenen JSON listesi yerine farklı bir format geldi.")
            return []

        limited_data = data[:limit]

        print(f"Başarılı: {len(data)} kayıttan ilk {len(limited_data)} tanesi alındı.")
        return limited_data

    except json.JSONDecodeError:
        print("Hata: API'den gelen yanıt geçerli bir JSON formatında değil.")
        return []


def save_posts_to_file(data: List[Dict[str, Any]], filepath: str) -> None:
    if not data:
        print(" Kaydedilecek veri bulunamadı.")
        return

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f" Başarılı: Veri, {filepath} dosyasına kaydedildi.")

    except IOError as e:
        print(f"Hata: Dosyaya yazma hatası oluştu: {e}")



if __name__ == "__main__":
    posts_data = fetch_posts(limit=100)
    save_posts_to_file(posts_data, OUTPUT_FILE)