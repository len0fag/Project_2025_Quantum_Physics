import time

class Search:
    def __init__(self, array):
        self.array = array

    def linear_search(self, target):
        for i in range(len(self.array)):
            if self.array[i] == target:
                return i
        return -1

# Создаем массив из 1 миллиона элементов
arr = list(range(1, 10**6 + 1))  # массив от 1 до 1 000 000
target = 999999  # ищем последний элемент

search = Search(arr)

# Измеряем время выполнения
start_time = time.time()
result = search.linear_search(target)
end_time = time.time()

# Вывод результата
if result != -1:
    print(f"Элемент {target} найден на индексе {result}.")
else:
    print(f"Элемент {target} не найден.")

# Вывод времени выполнения
print(f"Время выполнения: {(end_time - start_time) * 1000} миллисекунд.")
