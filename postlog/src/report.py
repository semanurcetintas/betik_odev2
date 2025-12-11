import os
import json
import csv
from collections import defaultdict
from typing import List, Dict, Any
from .models import LogRecord
from .parser import parse_app_log_file


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
REPORTS_DIR = os.path.join(ROOT_DIR, "reports")
CSV_OUTPUT_FILE = os.path.join(REPORTS_DIR, "summary.csv")
JSON_OUTPUT_FILE = os.path.join(REPORTS_DIR, "summary.json")


def analyze_logs(records: List[LogRecord]) -> Dict[str, Any]:
    total_logs = len(records)
    counts_by_level = defaultdict(int)
    stats_by_user = defaultdict(lambda: {"total": 0, "errors": 0})
    error_messages_list = []

    for record in records:

        counts_by_level[record.level] += 1

        user_key = str(record.user_id)
        stats_by_user[user_key]["total"] += 1

        if record.is_error:

            stats_by_user[user_key]["errors"] += 1

            error_messages_list.append({
                "message": record.message,
                "length": len(record.message)
            })

    error_messages_list.sort(key=lambda x: x["length"], reverse=True)


    top_5_error_messages = [item["message"] for item in error_messages_list[:5]]


    report_data = {
        "total_logs": total_logs,
        "by_level": dict(counts_by_level),
        "by_user": dict(stats_by_user),
        "top_5_error_messages": top_5_error_messages
    }

    return report_data


def save_as_csv(data: Dict[str, Any], filepath: str) -> None:
    csv_data = data["by_level"]

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['level', 'count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for level, count in csv_data.items():
                writer.writerow({'level': level, 'count': count})

        print(f" Başarılı: Seviye bazında istatistikler {filepath} dosyasına kaydedildi.")

    except IOError as e:
        print(f" Hata: CSV dosyasına yazma hatası oluştu: {e}")


def save_as_json(data: Dict[str, Any], filepath: str) -> None:

    try:
        with open(filepath, 'w', encoding='utf-8') as f:

            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f" Başarılı: Tüm istatistikler {filepath} dosyasına kaydedildi.")

    except IOError as e:
        print(f" Hata: JSON dosyasına yazma hatası oluştu: {e}")


def generate_report():
    log_records = parse_app_log_file()

    if not log_records:
        print("Analiz edilecek log kaydı bulunamadı. Raporlama sonlandırılıyor.")
        return

    print("\n-> Log kayıtları analiz ediliyor...")
    report_data = analyze_logs(log_records)
    print(" Analiz Tamamlandı.")


    os.makedirs(REPORTS_DIR, exist_ok=True)


    save_as_csv(report_data, CSV_OUTPUT_FILE)

    save_as_json(report_data, JSON_OUTPUT_FILE)

    print("\n--- Analiz Özeti ---")
    print(f"Toplam Log Sayısı: {report_data['total_logs']}")
    print(f"Seviye Bazında: {report_data['by_level']}")
    print(
        f"En Uzun 5 Hata Mesajı (İlk 1): {report_data['top_5_error_messages'][0] if report_data['top_5_error_messages'] else 'Yok'}")



if __name__ == "__main__":
    generate_report()