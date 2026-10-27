#!/bin/zsh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "=== СИАОД, ЛР №2, вариант 12, seed 42 ==="
python3 --version
python3 -c 'import sys; assert sys.version_info >= (3,10), "Нужен Python 3.10+"'

echo "Поиск исходных файлов (без curl и сетевых запросов)..."
python3 scripts/stage_downloads.py

# Сначала используем существующее окружение с библиотеками: оно уже могло
# установиться при первом запуске перед ошибкой curl.
PY=""
for CANDIDATE in "$ROOT/.venv/bin/python" "$HOME/Desktop/SIAOD_LR2_variant12_for_GitHub/.venv/bin/python" "$(command -v python3)"; do
  if [[ -x "$CANDIDATE" ]] && "$CANDIDATE" -c 'import numpy, matplotlib' 2>/dev/null; then
    PY="$CANDIDATE"
    break
  fi
done
if [[ -z "$PY" ]]; then
  echo "Библиотеки не обнаружены. Проверяю возможность установки в .venv..."
  if [[ ! -f "$ROOT/.venv/bin/python" ]]; then
    python3 -m venv .venv
  fi
  if ! "$ROOT/.venv/bin/python" -m pip install 'numpy>=1.26' 'matplotlib>=3.8'; then
    echo "ОШИБКА: pip не смог установить библиотеки. Возможно, та же проблема SSL."
    echo "Нужны numpy и matplotlib. Если они уже установлены для другого Python,"
    echo "активируй то окружение и повтори запуск. Не отключай проверку сертификатов."
    exit 1
  fi
  PY="$ROOT/.venv/bin/python"
fi

echo "Используем: $PY"
echo "Генерация массива операций варианта 12..."
"$PY" scripts/generate_data.py --variant 12 --only ops --out data/generated

echo "Проверки, замеры и построение графиков..."
"$PY" M1-intro-and-basic-structures/attachments/lab02-recursion-structures-starter.py \
    --variant 12 --data data/generated --out results \
    2>&1 | tee results/run_log.txt

echo "Запись реальных результатов в отчёт..."
"$PY" scripts/build_report.py
rm -f M1-intro-and-basic-structures/attachments/RUN_BEFORE_UPLOAD.txt

echo "=== Готово: проверка, графики и отчёт находятся в results/ ==="
