import time
import qiskit
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import MCXGate
import numpy as np

# Создание оракула, который инвертирует фазу целевого состояния
def create_oracle(n, target_index):
    oracle = QuantumCircuit(n)
    oracle.z(target_index)  # Применяем Z-оператор к целевому состоянию
    return oracle

# Создание диффузора (оператора усиления амплитуды)
def create_diffuser(n):
    diffuser = QuantumCircuit(n)
    diffuser.h(range(n))  # Применяем Hadamard ко всем кубитам
    diffuser.x(range(n))  # Применяем X-оператор ко всем кубитам
    mcx = MCXGate(n-1)  # Многоконтрольное X (отражение относительно |s>)
    diffuser.append(mcx, range(n))
    diffuser.x(range(n))  # Обратное преобразование X
    diffuser.h(range(n))  # Обратное преобразование Hadamard
    return diffuser

# Основная функция алгоритма Гровера
def grover_search(n, target_index, iterations):
    qc = QuantumCircuit(n, n)
    qc.h(range(n))  # Применяем Hadamard к каждому кубиту для создания суперпозиции

    oracle = create_oracle(n, target_index)  # Создаем оракул
    diffuser = create_diffuser(n)  # Создаем диффузор

    # Повторяем алгоритм Гровера заданное количество итераций
    for _ in range(iterations):
        qc.append(oracle.to_gate(), range(n))  # Применяем оракул
        qc.append(diffuser.to_gate(), range(n))  # Применяем диффузор

    qc.measure(range(n), range(n))  # Измеряем все кубиты
    return qc

# Параметры задачи
num_qubits = 3  # Количество кубитов (8 элементов в массиве, так как 2^3 = 8)
target = 5  # Искомый индекс (целевое состояние)
iterations = int(np.pi/4 * np.sqrt(2**num_qubits))  # Оптимальное количество итераций

# Измерение времени выполнения
start_time = time.time()  # Запускаем таймер

# Запуск алгоритма Гровера
qc = grover_search(num_qubits, target, iterations)
simulator = Aer.get_backend('qasm_simulator')  # Используем классический симулятор
result = execute(qc, simulator, shots=1024).result()  # Запускаем симуляцию
counts = result.get_counts()

# Измеряем время окончания выполнения
end_time = time.time()

# Вывод результатов измерений
print("Результаты измерений:", counts)

# Вывод времени выполнения
print(f"Время выполнения: {end_time - start_time} секунд")
