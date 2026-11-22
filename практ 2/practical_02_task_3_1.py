"""Порівняння list comprehension та generator expression."""

import sys
import timeit


def memory_comparison():
    """Порівняння використання пам'яті."""
    sizes = [1_000, 10_000, 100_000, 1_000_000]

    print("=" * 60)
    print(f"{'N':>12} | {'list (байт)':>14} | {'gen (байт)':>12} | {'Ratio':>8}")
    print("-" * 60)

    for n in sizes:
        data_list = [x ** 2 for x in range(n)]
        data_gen = (x ** 2 for x in range(n))

        list_size = sys.getsizeof(data_list)
        gen_size = sys.getsizeof(data_gen)

        print(f"{n:>12,} | {list_size:>14,} | {gen_size:>12,} | {list_size / gen_size:>7.0f}×")

    print("=" * 60)
    print("Примітка: sys.getsizeof() для списку враховує лише масив посилань,\n"
          "без самих об'єктів int, тож реальна різниця ще більша.")


def performance_comparison():
    """Порівняння продуктивності: sum через list vs generator."""
    n = 500_000
    runs = 5

    time_list = timeit.timeit(
        lambda: sum([x ** 2 for x in range(n)]),
        number=runs,
    )

    time_gen = timeit.timeit(
        lambda: sum(x ** 2 for x in range(n)),
        number=runs,
    )

    print(f"\nsum() для {n:,} елементів ({runs} запусків):")
    print(f"  list comprehension:   всього {time_list:.4f} с, "
          f"середнє {time_list / runs:.4f} с")
    print(f"  generator expression: всього {time_gen:.4f} с, "
          f"середнє {time_gen / runs:.4f} с")
    faster = "list" if time_list < time_gen else "generator"
    print(f"  Швидше: {faster}")


def practical_usage():
    """Практичні приклади використання generator expression."""
    words = [
        "Python", "ітератор", "генератор", "yield", "comprehension",
        "дані", "пам'ять", "ефективність", "конвеєр", "ліниві",
        "обчислення", "протокол", "об'єкт", "клас", "функція",
    ]

    # Найдовше слово: max() + generator expression
    max_len, longest = max((len(w), w) for w in words)
    print(f"Найдовше слово: '{longest}' ({max_len} символів)")

    # Чи всі слова непорожні — all() + gen expr
    all_nonempty = all(len(w) > 0 for w in words)
    print(f"Всі слова непорожні: {all_nonempty}")

    # Чи є слово довше 15 символів — any() + gen expr
    has_long = any(len(w) > 15 for w in words)
    print(f"Є слово > 15 символів: {has_long}")

    # CSV-рядок — ",".join() + gen expr
    csv_line = ",".join(w.lower() for w in words)
    print(f"CSV: {csv_line}")

    # Сума довжин усіх слів — sum() + gen expr
    total_length = sum(len(w) for w in words)
    print(f"Сума довжин: {total_length}")

    # Словник {слово: довжина} через dict comprehension
    word_lengths = {w: len(w) for w in words}
    print(f"Довжини: {word_lengths}")

    numbers = range(1, 101)

    # Сума квадратів парних чисел від 1 до 100 — sum() + gen expr з if
    even_squares_sum = sum(x ** 2 for x in numbers if x % 2 == 0)
    print(f"\nСума квадратів парних від 1 до 100: {even_squares_sum}")


def conclusions():
    """Висновки: коли доцільно використовувати кожен підхід."""
    print("""
1. Generator expression займає сталий обсяг пам'яті (~200 байт) незалежно
   від кількості елементів, бо значення обчислюються ліниво, по одному.
   Розмір списку росте лінійно з N.

2. Generator expression доцільний, коли:
   - дані проходять один раз (sum, max, min, any, all, join);
   - обсяг даних великий або нескінченний (файли, потоки, мережа);
   - потрібна рання зупинка (any/all/break обривають обчислення);
   - будується конвеєр обробки без проміжних колекцій.

3. List comprehension доцільний, коли:
   - результат потрібно обходити кілька разів;
   - потрібен доступ за індексом, len(), зрізи, сортування на місці;
   - даних небагато, а важлива швидкість: на малих і середніх N
     список часто трохи швидший, бо немає накладних витрат на
     відновлення кадру генератора при кожному next().

4. Генератор одноразовий: після вичерпання повторний обхід поверне
   порожню послідовність — це треба враховувати при проєктуванні.
""")


def main():
    print(">>> Порівняння використання пам'яті <<<\n")
    memory_comparison()

    print("\n>>> Порівняння продуктивності <<<")
    performance_comparison()

    print("\n>>> Практичне використання generator expression <<<\n")
    practical_usage()

    print("\n>>> Висновки <<<")
    conclusions()


if __name__ == "__main__":
    main()
