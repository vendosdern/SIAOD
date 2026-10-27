"""Помещает в проект исходники, скачанные через браузер в ~/Downloads.

Без запросов в сеть и без отключения проверки TLS. При первом запуске нужно
скачать два исходных файла через кнопки Download raw file на GitHub.
"""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
DOWNLOADS = Path.home() / 'Downloads'
FILES = (
    (
        'lab02-recursion-structures-starter.py',
        ROOT / 'M1-intro-and-basic-structures' / 'attachments' / 'lab02-recursion-structures-starter.py',
        'https://github.com/KatyaDolgova/SiAOD_labs/blob/main/lab02/lab02-recursion-structures-starter.py',
        'def self_check(',
    ),
    (
        'generate_data.py',
        ROOT / 'scripts' / 'generate_data.py',
        'https://github.com/mel0d1an/data-structures-and-algorithms/blob/main/scripts/generate_data.py',
        'def main(',
    ),
)

def valid_python(path: Path, token: str) -> bool:
    try:
        raw = path.read_bytes()
        if len(raw) < 300 or b'<!DOCTYPE' in raw[:500] or b'<html' in raw[:500]:
            return False
        source = raw.decode('utf-8-sig')
        compile(source, str(path), 'exec')
        return token in source
    except (OSError, UnicodeError, SyntaxError):
        return False

def main() -> None:
    missing = []
    for name, target, url, token in FILES:
        if target.is_file() and valid_python(target, token):
            print('Есть:', target.relative_to(ROOT))
            continue
        # На macOS Chrome может создать "generate_data (1).py", если файл уже скачан.
        candidates = [DOWNLOADS / name]
        if DOWNLOADS.exists():
            candidates += sorted(DOWNLOADS.glob(name[:-3] + ' (*).py'),
                                 key=lambda x: x.stat().st_mtime, reverse=True)
        source = next((p for p in candidates if p.is_file() and valid_python(p, token)), None)
        if source is None:
            missing.append((name, url, target))
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        print('Скопирован:', source, '→', target.relative_to(ROOT))
    if missing:
        print('\nНЕ ХВАТАЕТ ИСХОДНЫХ ФАЙЛОВ. Открой ссылки в Chrome и нажми')
        print('кнопку "Download raw file" (скачать исходный файл):')
        for name, url, dest in missing:
            print('\nФайл:', name, '\nURL:', url)
            print('После скачивания ожидается в ~/Downloads или здесь:', dest)
        print('\nПовтори: zsh ./run_mac.command')
        sys.exit(1)

if __name__ == '__main__':
    main()
