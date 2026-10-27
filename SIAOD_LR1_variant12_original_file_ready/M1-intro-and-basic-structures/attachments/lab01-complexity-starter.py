#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 1. Анализ временной сложности элементарных алгоритмов.

Исходная заготовка преподавателя: реализованы четыре алгоритма и дополнены
репрезентативные тесты. Каркас загрузки данных, бенчмаркинга и графиков
сохранён из исходного файла.

Данные варианта генерируются из корня репозитория преподавателя:
    python scripts/generate_data.py --variant 12 --only arrays

Запуск из корня личного репозитория, в котором есть data/generated:
    python M1-intro-and-basic-structures/attachments/lab01-complexity-starter.py \
        --variant 12 --out results

При другом расположении данных добавьте: --data /путь/к/data/generated
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Параметры эксперимента — из заготовки преподавателя
# ---------------------------------------------------------------------------

SIZES = (1_000, 3_000, 10_000, 30_000, 100_000)
# Для O(n²) не используем n=100000; 500 — префикс массива из 1000 чисел.
QUADRATIC_SIZES = (500, 1_000, 3_000, 10_000, 30_000)
EXPONENTS = (10**3, 10**4, 10**5, 10**6, 10**7)
POW_MOD = 1_000_000_007  # модуль ограничивает размер промежуточных чисел
POW_BASE = 3
REPEATS = 5              # прогрев + 5 замеров; берём медиану
POW_CALLS = 20_000       # короткие операции измеряем одной пачкой

# ---------------------------------------------------------------------------
# 1. Алгоритмы — реализация заданий в исходной заготовке
# ---------------------------------------------------------------------------


def array_sum(a: list[int]) -> int:
    """Сумма элементов массива: Θ(n), инвариант — сумма префикса."""
    result = 0
    for value in a:
        result += value
    return result


def array_max(a: list[int]) -> int:
    """Максимум непустого массива: Θ(n), максимум просмотренного префикса."""
    if not a:
        raise ValueError("Максимум пустого массива не определён")
    result = a[0]
    for value in a:
        if value > result:
            result = value
    return result


def count_equal_pairs(a: list[int]) -> int:
    """Число равных пар i < j (двойной цикл): Θ(n²)."""
    count = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] == a[j]:
                count += 1
    return count


def binary_pow(x: int, n: int, mod: int | None = None) -> int:
    """Бинарное возведение в неотрицательную степень: Θ(log(n+1)).

    Инвариант: result * x**n равно исходной степени (по mod, если задан).
    """
    if n < 0:
        raise ValueError("Показатель степени должен быть неотрицательным")
    if mod is not None and mod <= 0:
        raise ValueError("Модуль должен быть положительным")

    result = 1
    if mod is not None:
        result %= mod
        x %= mod

    while n > 0:
        if n % 2 == 1:
            result *= x
            if mod is not None:
                result %= mod
        n //= 2
        if n > 0:
            x *= x
            if mod is not None:
                x %= mod
    return result

# ---------------------------------------------------------------------------
# 2. Данные варианта: поиск каталога и загрузка — каркас преподавателя
# ---------------------------------------------------------------------------


def find_data_dir(explicit: Path | None) -> Path:
    """Каталог с данными варианта: --data либо data/generated рядом с работой."""
    if explicit is not None:
        if not explicit.is_dir():
            raise SystemExit(f"Каталог не найден: {explicit}")
        return explicit
    candidates = []
    for base in (Path.cwd(), Path(__file__).resolve().parent):
        for parent in (base, *base.parents):
            candidates.append(parent / "data" / "generated")
    for path in candidates:
        if path.is_dir():
            return path
    raise SystemExit(
        "Не найден каталог data/generated с данными варианта.\n"
        "Сгенерируйте данные из корня репозитория курса:\n"
        "    python scripts/generate_data.py --variant 12 --only arrays\n"
        "или укажите каталог явно: --data <путь>")


def check_variant(data_dir: Path, variant: int) -> None:
    """Сверить номер варианта с паспортом данных (manifest.json)."""
    manifest_path = data_dir / "manifest.json"
    if not manifest_path.is_file():
        print(f"ВНИМАНИЕ: в {data_dir} нет manifest.json — "
              f"не могу проверить, что данные относятся к варианту {variant}.")
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    actual = manifest.get("variant")
    if actual != variant:
        raise SystemExit(
            f"Данные в {data_dir} сгенерированы для варианта {actual}, "
            f"а работа запущена с --variant {variant}.\n"
            f"Перегенерируйте данные: "
            f"python scripts/generate_data.py --variant {variant} --only arrays")
    print(f"Данные варианта {variant} (seed={manifest.get('seed')}) из {data_dir}")


def load_array(data_dir: Path, kind: str, n: int, limit: int | None = None) -> list[int]:
    """Загрузить массив arrays_<kind>_<n>.txt; limit ограничивает длину."""
    path = data_dir / f"arrays_{kind}_{n}.txt"
    if not path.is_file():
        raise SystemExit(
            f"Не найден файл данных: {path}\n"
            f"Сгенерируйте его: python scripts/generate_data.py "
            f"--variant <ваш вариант> --only arrays")
    values = [int(line) for line in path.read_text(encoding="utf-8").split()]
    return values[:limit] if limit is not None else values

# ---------------------------------------------------------------------------
# 3. Тесты и верификация — расширение тестов из заготовки преподавателя
# ---------------------------------------------------------------------------


def self_check() -> None:
    """Граничные случаи и сравнение с эталоном sum, max, pow."""
    assert array_sum([]) == 0
    assert array_sum([7]) == 7
    assert array_sum([-2, 2, -1]) == -1
    assert array_max([3, 1, 2]) == 3
    assert array_max([5]) == 5
    assert array_max([-10, -3, -7]) == -3
    try:
        array_max([])
    except ValueError:
        pass
    else:
        raise AssertionError("Максимум пустого массива должен вызывать ValueError")

    assert count_equal_pairs([]) == 0
    assert count_equal_pairs([8]) == 0
    assert count_equal_pairs([1, 2, 3, 4]) == 0
    assert count_equal_pairs([5, 5, 5]) == 3
    assert count_equal_pairs([1, 2, 1, 1, 2]) == 4
    assert binary_pow(2, 0) == 1
    assert binary_pow(2, 10) == 1024
    assert binary_pow(2, 10, mod=1000) == 24
    assert binary_pow(9, 0, mod=1) == 0

    rng = random.Random(42)
    for _ in range(200):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(0, 60))]
        original = a[:]
        assert array_sum(a) == sum(a)
        if a:
            assert array_max(a) == max(a)
        # Эталон для подсчёта пар: число пар по частотам значений.
        frequencies: dict[int, int] = {}
        for value in a:
            frequencies[value] = frequencies.get(value, 0) + 1
        expected = sum(f * (f - 1) // 2 for f in frequencies.values())
        assert count_equal_pairs(a) == expected
        assert a == original  # ни один алгоритм не меняет входной список

    for _ in range(200):
        x, n = rng.randint(-50, 50), rng.randint(0, 64)
        assert binary_pow(x, n) == x**n
        assert binary_pow(x, n, mod=POW_MOD) == pow(x, n, POW_MOD)
    print("self_check: OK")

# ---------------------------------------------------------------------------
# 4. Бенчмарк — каркас преподавателя (прогрев, 5 повторов, медиана)
# ---------------------------------------------------------------------------


def bench(call) -> float:
    """Медиана времени выполнения call() по REPEATS запускам, с прогревом."""
    call()  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        call()
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def log_log_slope(points: list[tuple[int, float]]) -> float:
    """Наклон прямой в осях (log n, log t) — оценка показателя степени."""
    xs = [math.log10(n) for n, _ in points]
    ys = [math.log10(t) for _, t in points]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            / sum((x - mx) ** 2 for x in xs))


def run_benchmarks(data_dir: Path) -> dict[str, list[tuple[int, float]]]:
    """Замеры на данных варианта. Возвращает {алгоритм: [(n, t), ...]}."""
    results: dict[str, list[tuple[int, float]]] = {}
    random_arrays = {n: load_array(data_dir, "random", n) for n in SIZES}
    for name, fn in (("array_sum", array_sum), ("array_max", array_max)):
        points = []
        print(f"\n{name}:")
        for n in SIZES:
            a = random_arrays[n]
            t = bench(lambda: fn(a))
            points.append((n, t))
            print(f"  n={n:>7}  t={t:.6f} c")
        results[name] = points

    print("\ncount_equal_pairs:")
    points = []
    for n in QUADRATIC_SIZES:
        file_n = n if n in SIZES else min(s for s in SIZES if s >= n)
        a = load_array(data_dir, "dups", file_n, limit=n)
        t = bench(lambda: count_equal_pairs(a))
        points.append((n, t))
        print(f"  n={n:>7}  t={t:.6f} c")
    results["count_equal_pairs"] = points

    print(f"\nbinary_pow (по {POW_CALLS} вызовов на точку, по модулю {POW_MOD}):")
    points = []
    for e in EXPONENTS:
        def batch(e: int = e) -> None:
            for _ in range(POW_CALLS):
                binary_pow(POW_BASE, e, mod=POW_MOD)
        t = bench(batch) / POW_CALLS
        points.append((e, t))
        print(f"  n={e:>9}  log2(n)={math.log2(e):5.1f}  t={t:.9f} c")
    results["binary_pow"] = points
    return results

# ---------------------------------------------------------------------------
# 5. Графики — каркас преподавателя
# ---------------------------------------------------------------------------


def plot_results(results: dict[str, list[tuple[int, float]]], out_dir: Path) -> None:
    """Log-log для степенных алгоритмов и t(log₂ n) для бинарной степени."""
    try:
        import matplotlib
        matplotlib.use("Agg")  # сохранение в файл без графической оболочки
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nmatplotlib не установлен — графики пропущены "
              "(pip install -r requirements.txt)")
        return

    power_law = ("array_sum", "array_max", "count_equal_pairs")
    fig, ax = plt.subplots(figsize=(7, 5))
    for name in power_law:
        points = results[name]
        ns = [n for n, _ in points]
        ts = [t for _, t in points]
        ax.plot(ns, ts, marker="o", label=f"{name} (наклон ≈ {log_log_slope(points):.2f})")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("размер входа n")
    ax.set_ylabel("время, с")
    ax.set_title("Время работы в осях log-log")
    ax.grid(True, which="both", linewidth=0.3)
    ax.legend()
    fig.tight_layout()
    loglog_path = out_dir / "lab01_loglog.png"
    fig.savefig(loglog_path, dpi=150)
    plt.close(fig)

    points = results["binary_pow"]
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    ax2.plot([math.log2(n) for n, _ in points], [t for _, t in points], marker="o")
    ax2.set_xlabel("log₂ n (число бит показателя)")
    ax2.set_ylabel("время одного вызова, с")
    ax2.set_title("Бинарное возведение в степень: t(log₂ n)")
    ax2.grid(True, linewidth=0.3)
    fig2.tight_layout()
    pow_path = out_dir / "lab01_binary_pow.png"
    fig2.savefig(pow_path, dpi=150)
    plt.close(fig2)
    print(f"\nГрафики сохранены:\n  {loglog_path}\n  {pow_path}")

# ---------------------------------------------------------------------------
# 6. Запуск — исходный интерфейс --variant / --data / --out
# ---------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    ap.add_argument("--data", type=Path, default=None,
                    help="каталог с данными варианта (по умолчанию ищется data/generated)")
    ap.add_argument("--out", type=Path, default=Path.cwd(),
                    help="каталог для графиков (по умолчанию текущий)")
    args = ap.parse_args()
    data_dir = find_data_dir(args.data)
    check_variant(data_dir, args.variant)

    self_check()
    results = run_benchmarks(data_dir)

    print("\nНаклон в осях log-log (оценка показателя степени):")
    for name in ("array_sum", "array_max", "count_equal_pairs"):
        print(f"  {name:20s} {log_log_slope(results[name]):.3f}")
    args.out.mkdir(parents=True, exist_ok=True)
    plot_results(results, args.out)


if __name__ == "__main__":
    main()
