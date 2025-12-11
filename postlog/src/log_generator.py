import json
import random
import datetime
import os
from typing import Dict, List, Any

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
INPUT_FILE = os.path.join(ROOT_DIR, "data", "raw_posts.json")
OUTPUT_FILE = os.path.join(ROOT_DIR, "data", "app.log")


LOG_LEVELS = ["INFO", "WARNING", "ERROR"]


def generate_log_line(post: Dict[str, Any]) -> str:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_level = random.choice(LOG_LEVELS)
    user_id = post.get("userId", "N/A")
    post_id = post.get("id", "N/A")

    message = post.get("body", post.get("title", "No message content"))
    message = message.replace('\n', ' ')

    log_line = (
        f"[{timestamp}] {log_level} "
        f"(user_id={user_id}, post_id={post_id}): {message}"
    )

    return log_line


def generate_and_save_logs():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            posts: List[Dict[str, Any]] = json.load(f)

    except FileNotFoundError:
        print(f" Hata: {INPUT_FILE} dosyası bulunamadı. Lütfen önce fetcher.py'yi çalıştırın.")
        return
    except json.JSONDecodeError:
        print(f"Hata: {INPUT_FILE} dosyası geçerli bir JSON formatında değil.")
        return
    except Exception as e:
        print(f"Hata: Dosya okuma sırasında beklenmedik bir hata oluştu: {e}")
        return


    log_lines: List[str] = []

    print(f"-> {len(posts)} adet post kaydından log satırları üretiliyor...")
    for post in posts:
        log_line = generate_log_line(post)
        log_lines.append(log_line)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(log_lines) + '\n')

        print(f"Başarılı: Toplam {len(log_lines)} adet log satırı {OUTPUT_FILE} dosyasına kaydedildi.")

    except IOError as e:
        print(f" Hata: Log dosyasına yazma hatası oluştu: {e}")


if __name__ == "__main__":
    generate_and_save_logs()