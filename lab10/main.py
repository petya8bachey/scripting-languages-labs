import os, shutil, logging, time, datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

SRC = Path.home() / ".ssh"
BACKUP_DIR = Path.home() / ".ssh_backups"

def backup():
    try:
        if not SRC.exists():
            raise FileNotFoundError(f"Директория {SRC} не найдена")
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        dest = BACKUP_DIR / datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        shutil.copytree(SRC, dest, dirs_exist_ok=True)
        logger.info(f"Успешный бэкап → {dest}")
    except Exception as e:
        logger.error(f"Ошибка: {e}")

if __name__ == "__main__":
    logger.info("Запуск бэкапа SSH (каждый час, Ctrl+C для остановки)")
    try:
        while True:
            backup()
            time.sleep(3600)  # 1 час
    except KeyboardInterrupt:
        logger.info("Скрипт остановлен")