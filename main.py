import psutil
import csv
import threading
import time
from datetime import datetime

# Функция для записи метрик в файл CSV
def save_metrics():
    next_save_time = time.time() + 60  # Начинаем с сохранения через 60 секунд
    while not stop_requested.is_set():
        current_time = time.time()

        if current_time >= next_save_time:
            next_save_time = current_time + 60  # Обновляем время для следующего сохранения

            # Получаем данные CPU и температуру процессора
            cpu_percent = psutil.cpu_percent()
            count_process = len(list((psutil.process_iter())))

            # Текущее время
            formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Записываем данные в файл
            with open('metrics.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([formatted_time, 'CPU Usage (%)', cpu_percent])
                writer.writerow([formatted_time, 'Count process', count_process])

    print("Сбор метрик остановлен.")

# Флаг для запроса остановки
stop_requested = threading.Event()

# Запускаем поток для сохранения метрик
metrics_thread = threading.Thread(target=save_metrics)
metrics_thread.start()

# Ожидаем ввода команды "stop" для остановки сбора метрик
while True:
    command = input("Введите 'stop' для остановки сбора метрик: ")
    if command.lower() == 'stop':
        stop_requested.set()
        break

# Ждем завершения потока сохранения метрик
metrics_thread.join()