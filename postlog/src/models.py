from datetime import datetime
from typing import ClassVar


class LogRecord:
    VALID_LEVELS: ClassVar[set[str]] = {"INFO", "WARNING", "ERROR"}

    def __init__(self, timestamp: datetime, level: str, user_id: int, post_id: int, message: str):
        self.timestamp = timestamp
        self.level = level.upper()
        self.user_id = user_id
        self.post_id = post_id
        self.message = message


    def __repr__(self) -> str:
        return (
            f"LogRecord("
            f"timestamp={self.timestamp!r}, level='{self.level}', "
            f"user_id={self.user_id}, post_id={self.post_id}, "
            f"message='{self.message[:40]}...')"  # Mesajın ilk 40 karakteri gösterilir
        )

    def __str__(self) -> str:
        return (
            f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.level} "
            f"(user_id={self.user_id}, post_id={self.post_id}): {self.message}"
        )


    @property
    def is_error(self) -> bool:
        return self.level == "ERROR"



if __name__ == "__main__":
    record = LogRecord(
        timestamp=datetime(2025, 12, 11, 17, 30, 0),
        level="ERROR",
        user_id=45,
        post_id=99,
        message="A very long message indicating a severe issue occurred."
    )

    print(f"__repr__ çıktısı: {record!r}")
    print(f"__str__ çıktısı: {record}")
    print(f"@property is_error: {record.is_error}")

    info_record = LogRecord(datetime.now(), "INFO", 1, 1, "Successful request.")
    print(f"@property is_error (INFO): {info_record.is_error}")