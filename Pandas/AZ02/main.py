import pandas as pd
import random

# Фиксируем seed для повторяемости
random.seed(42)

students = ["Аня", "Боб", "Чарли", "Даша", "Ева", "Федор", "Глаша", "Денис", "Ира", "Женя"]
subjects = ["Математика", "Физика", "Химия", "История", "Английский"]

data = {"Ученик": students}
for subject in subjects:
    data[subject] = [random.randint(2, 5) for _ in range(len(students))]

df = pd.DataFrame(data)
print(df.head(3))

# Cредние
subject_means = df[subjects].mean()
print("\nСредняя оценка по каждому предмету:")
print(subject_means)

# Медианная
subject_median = df[subjects].median()
print("\nМедианная оценка по каждому предмету:")
print(subject_median)

# StD
subject_std = df[subjects].std().round(3)
print("\nСтандартное отклонение по каждому предмету:")
print(subject_std)

# Квантили и IQR для математики
Q1_math = df['Математика'].quantile(0.25)
Q3_math = df['Математика'].quantile(0.75)
IQR = Q3_math - Q1_math

print("\nКвантили и IQR для математики:")
print(f"  - Q1 (25%): {Q1_math}")
print(f"  - Q3 (75%): {Q3_math}")
print(f"  - IQR: {IQR}")