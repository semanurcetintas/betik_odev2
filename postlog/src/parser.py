import re
from datetime import datetime
import os
from typing import List, Optional, TypeVar
from .models import LogRecord


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
INPUT_FILE = os.path.join(ROOT_DIR, "data", "app.log")


LOG_PATTERN = re.compile(
    r"^"
    r"\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s"  # Tarih-Saat
    r"(?P<level>INFO|WARNING|ERROR)\s"  # Seviye
    r"\(user_id=(?P<user_id>\d+),\s"  # user_id
    r"post_id=(?P<post_id>\d+)\):\s"  # post_id
    r"(?P<message>.*)"  # Mesaj metni
    r"$"
)


def parse_log_line(line: str) -> Optional[LogRecord]:
    line = line.strip()
    if not line:
        return None

    match = LOG_PATTERN.match(line)

    if not match:
        return None

    try:
        data = match.groupdict()
        timestamp_obj = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")

        user_id_int = int(data["user_id"])
        post_id_int = int(data["post_id"])

        return LogRecord(
            timestamp=timestamp_obj,
            level=data["level"],
            user_id=user_id_int,
            post_id=post_id_int,
            message=data["message"]
        )

    except ValueError as e:
        print(f" Ayrıştırma Hata (Değer Dönüşümü): {e} - Satır: {line[:80]}...")
        return None

    except Exception as e:
        print(f"Beklenmedik Hata: {e} - Satır: {line[:80]}...")
        return None


def parse_app_log_file(filepath: str = INPUT_FILE) -> List[LogRecord]:

    if not os.path.exists(filepath):
        print(f"Hata: Log dosyası bulunamadı: {filepath}. Lütfen önce log_generator.py'yi çalıştırın.")
        return []

    parsed_records: List[LogRecord] = []

    print(f"-> {filepath} dosyasındaki loglar ayrıştırılıyor...")

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            record = parse_log_line(line)
            if record:
                parsed_records.append(record)

    print(f"Başarılı: Toplam {len(parsed_records)} adet LogRecord nesnesi oluşturuldu.")
    return parsed_records


if __name__ == "__main__":

    all_records = parse_app_log_file()

    print("\n--- İlk 5 Kayıt Kontrol ---")
    for i, record in enumerate(all_records[:5]):
        print(f"{i + 1}. Kayıt: {record}")
        print(f"   -> Hata mı? {record.is_error}")

    print(f"\nToplam kayıt sayısı: {len(all_records)}")