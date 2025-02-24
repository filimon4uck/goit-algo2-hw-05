import time
import re
from hyperloglog import HyperLogLog
import json


def load_log(path_file):
    ip_addresses = []
    with open(path_file, "r", encoding="utf-8") as file:
        for line in file:
            try:
                log_data = json.loads(line.strip())
                ip = log_data.get("remote_addr")
                if ip:
                    ip_addresses.append(ip)
            except json.JSONDecodeError:
                print(f"Помилка декодування JSON у рядку: {line.strip()}")
    return ip_addresses


def exact_count(ip_addresses):
    unique_ip_addresses = set(ip_addresses)
    return len(unique_ip_addresses)


def approximate_count(ip_addresses):
    hll = HyperLogLog(0.01)
    for ip in ip_addresses:
        hll.add(ip)
    return len(hll)


def compare_methods(file_path):
    print(f"Завантаження даних: {file_path}")
    ip_addresses = load_log(file_path)

    if not ip_addresses:
        print("Не знайдено жодних IP-адрес у файлі.")
        return

    print(f"Завантажено {len(ip_addresses)} IP-адрес")

    # Точний підрахунок
    start_time = time.time()
    exact_result = exact_count(ip_addresses)
    exact_time = time.time() - start_time

    # Наближений підрахунок
    start_time = time.time()
    approximate_result = approximate_count(ip_addresses)
    approximate_time = time.time() - start_time

    # Виведення результатів
    print("\nРезультати порівняння:")
    print(f"{'':<35}{'Точний підрахунок':<25}{'HyperLogLog':<25}")
    print(f"{'Унікальні елементи':<35}{exact_result:<25}{approximate_result:<25}")
    print(f"{'Час виконання (сек.)':<35}{exact_time:<25.6f}{approximate_time:<25.6f}")


if __name__ == "__main__":
    log_file = "lms-stage-access.log"
    compare_methods(log_file)
