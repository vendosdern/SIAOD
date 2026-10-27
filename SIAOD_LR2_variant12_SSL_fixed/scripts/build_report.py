"""Формирование отчёта только после успешного реального запуска лабораторной.

Этот файл не подставляет чужие числа. Он вставляет в отчёт содержимое
журнала, полученное при выполнении приложения на текущем компьютере.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"


def main() -> None:
    log = (RESULTS / "run_log.txt").read_text(encoding="utf-8")
    if "self_check: OK" not in log:
        raise SystemExit("В журнале нет self_check: OK; отчёт не обновлён.")
    for filename in ("lab02_append.png", "lab02_front.png"):
        if not (RESULTS / filename).is_file():
            raise SystemExit(f"Нет {filename}; отчёт не обновлён.")
    template = (ROOT / "report_template.md").read_text(encoding="utf-8")
    session = datetime.now().astimezone().strftime("%d.%m.%Y %H:%M %Z")
    env = (f"macOS ({platform.platform()}), Python {sys.version.split()[0]}, "
           f"чип Apple M4 Pro (данные компьютера студента), запуск {session}")
    text = template.replace("{{STATUS}}", "**Тесты завершились успешно: `self_check: OK`.**")
    text = text.replace("{{ENV}}", env)
    # Журнал сохраняется отдельно; в отчёте приводим вывод реального запуска.
    text = text.replace("{{LOG}}", "```text\n" + log.rstrip() + "\n```")
    (RESULTS / "lab02_report.md").write_text(text, encoding="utf-8")
    print(f"Отчёт обновлён: {RESULTS / 'lab02_report.md'}")


if __name__ == "__main__":
    main()
