"""Ітерабельний контейнер StudentGroup з окремим ітератором."""

from collections import namedtuple

Student = namedtuple("Student", ["name", "grade"])


class StudentGroupIterator:
    """Ітератор для обходу StudentGroup."""

    def __init__(self, students: list[Student]):
        self._students = students
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> Student:
        # Повернути наступного студента або raise StopIteration
        if self._index >= len(self._students):
            raise StopIteration
        student = self._students[self._index]
        self._index += 1
        return student


class StudentGroup:
    """Ітерабельний контейнер студентів з підтримкою багаторазового обходу."""

    def __init__(self, group_name: str):
        self._group_name = group_name
        self._students: list[Student] = []

    def add_student(self, name: str, grade: int) -> None:
        """Додає студента до групи."""
        self._students.append(Student(name, grade))

    def __iter__(self):
        # Повертаємо НОВИЙ ітератор при кожному виклику —
        # це дозволяє багаторазовий і незалежний обхід
        return StudentGroupIterator(self._students)

    def __len__(self) -> int:
        return len(self._students)

    def top_students(self, n: int = 3):
        """Повертає ітератор по n найкращих студентах."""
        ranked = sorted(self._students, key=lambda s: s.grade, reverse=True)
        return StudentGroupIterator(ranked[:n])


def main():
    group = StudentGroup("КІ-21")
    group.add_student("Олена", 95)
    group.add_student("Іван", 78)
    group.add_student("Марія", 92)
    group.add_student("Петро", 85)
    group.add_student("Анна", 88)

    print(f"Група {group._group_name}, студентів: {len(group)}")

    # Перший обхід
    print("\nПерший обхід:")
    for student in group:
        print(f"  {student.name}: {student.grade}")

    # Другий обхід — працює повторно (на відміну від одноразового ітератора)
    print("\nДругий обхід:")
    for student in group:
        print(f"  {student.name}: {student.grade}")

    # Два незалежних ітератори працюють одночасно (вкладений цикл)
    print("\nВсі пари студентів:")
    for s1 in group:
        for s2 in group:
            if s1.name < s2.name:
                print(f"  {s1.name} та {s2.name}")

    # Явна демонстрація незалежності ітераторів
    it1, it2 = iter(group), iter(group)
    print(f"\nit1 is it2: {it1 is it2}")
    print(f"next(it1) = {next(it1).name}, next(it1) = {next(it1).name}, "
          f"next(it2) = {next(it2).name}")

    # Топ-3 студентів за оцінкою
    print("\nТоп-3 студенти:")
    top = group.top_students(3)
    print(f"  (тип результату: {type(top).__name__})")
    for student in top:
        print(f"  {student.name}: {student.grade}")


if __name__ == "__main__":
    main()
