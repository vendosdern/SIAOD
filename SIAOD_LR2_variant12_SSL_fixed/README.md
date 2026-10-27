# СИАОД — ЛР № 2 (macOS), вариант 12

**Тесля Владислав Германович, БВТ2502.** Seed = 42.

Эта версия решает ошибку `curl: (60) SSL certificate problem`. Скрипт **не делает сетевых запросов к GitHub** и не отключает защиту SSL. Код подруги используется с её разрешения, официальный генератор — преподавателя. Для первого запуска скачай эти два файла через браузер:

1. [Код лабораторной №2](https://github.com/KatyaDolgova/SiAOD_labs/blob/main/lab02/lab02-recursion-structures-starter.py) — нажми `...` у файла / кнопку **Download raw file** (рядом с Raw). Получится `lab02-recursion-structures-starter.py`.
2. [Генератор преподавателя](https://github.com/mel0d1an/data-structures-and-algorithms/blob/main/scripts/generate_data.py) — аналогично **Download raw file**, получится `generate_data.py`.

Оставь файлы в папке **Загрузки (Downloads)**. Если Chrome переименует копию в `...(1).py`, скрипт тоже её найдёт. Не скачивай HTML-страницу вместо исходного Python-файла.

Распакуй архив, открой Терминал, перейди в эту папку и выполни:

```bash
zsh ./run_mac.command
```

Скрипт сам перенесёт оба файла из Downloads в нужные папки, найдёт Python с `numpy` и `matplotlib` либо попытается установить библиотеки, запустит официальный генератор варианта 12, затем код лабораторной, сохранит `results/run_log.txt`, `lab02_append.png`, `lab02_front.png` и обновит `results/lab02_report.md` **твоими измерениями**. Исходные данные лежат в `data/generated`, их загружать в GitHub необязательно.

Если библиотеки уже поставились при первом запуске до ошибки `curl`, при повторном запуске они будут использованы из `.venv`.

После появления `=== Готово ===` загрузи `M1-intro-and-basic-structures/attachments/lab02-recursion-structures-starter.py`, `scripts/generate_data.py`, `results/lab02_report.md`, оба PNG и `results/run_log.txt` в GitHub. Не загружай `.venv`, `data/generated`, `__pycache__`.

**Важно:** до успешного запуска отчёт — черновик, а не подтверждённые замеры. Источник решения — [репозиторий К. Долговой](https://github.com/KatyaDolgova/SiAOD_labs/tree/main/lab02), использованный с разрешения автора.
