import argparse
import sys
import os

try:
    from .fetcher import fetch_posts, save_posts_to_file, API_URL, OUTPUT_FILE as RAW_POSTS_FILE
except ImportError as e:
    print(f"Modül yükleme hatası: fetcher.py dosyasını kontrol edin. Detay: {e}")
    sys.exit(1)

try:
    from .log_generator import generate_and_save_logs, INPUT_FILE as LOG_GEN_INPUT
except ImportError as e:
    print(f"Modül yükleme hatası: log_generator.py dosyasını kontrol edin. Detay: {e}")
    sys.exit(1)

try:
    from .report import generate_report, JSON_OUTPUT_FILE, CSV_OUTPUT_FILE
except ImportError as e:
    print(f"Modül yükleme hatası: report.py dosyasını kontrol edin. Detay: {e}")
    sys.exit(1)


def handle_fetch(args):
    print("--- 1. FETCH Komutu Başlatıldı ---")
    posts_data = fetch_posts()
    if posts_data:
        save_posts_to_file(posts_data, RAW_POSTS_FILE)
        print(f"Veri {os.path.basename(RAW_POSTS_FILE)} dosyasına kaydedildi.")
    else:
        print("API'den veri alınamadı.")
    print("--- FETCH Komutu Tamamlandı ---")


def handle_generate(args):
    print("--- 2. GENERATE Komutu Başlatıldı ---")
    generate_and_save_logs()
    print("Log dosyası app.log olarak oluşturuldu.")
    print("--- GENERATE Komutu Tamamlandı ---")


def handle_analyze(args):
    print("--- 3. ANALYZE Komutu Başlatıldı ---")
    generate_report()
    print(f"Raporlar {os.path.basename(CSV_OUTPUT_FILE)} ve {os.path.basename(JSON_OUTPUT_FILE)} olarak üretildi.")
    print("--- ANALYZE Komutu Tamamlandı ---")


def main():
    parser = argparse.ArgumentParser(
        description="Betik ödev projesi komut satırı aracı."
    )

    # Aynı anda yalnızca bir tanesinin kullanılmasını zorunlu kılıyoruz
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '--fetch',
        action='store_true',
        help="API'den postları çeker ve raw_posts.json dosyasını günceller."
    )

    group.add_argument(
        '--generate',
        action='store_true',
        help="raw_posts.json dosyasından sentetik log üretir ve app.log dosyasını oluşturur."
    )

    group.add_argument(
        '--analyze',
        action='store_true',
        help="app.log dosyasını çözümler ve raporları üretir."
    )

    args = parser.parse_args()

    if args.fetch:
        handle_fetch(args)
    elif args.generate:
        handle_generate(args)
    elif args.analyze:
        handle_analyze(args)


if __name__ == "__main__":
    main()
