import random
from colorama import Fore, Style, init
import sys

init(autoreset=True)

class DualOutput:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        # Удаляем цветовые коды для файла
        clean_message = message
        for code in [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Style.RESET_ALL]:
            clean_message = clean_message.replace(code, '')
        self.log.write(clean_message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

def full_detailed_simulation():
    # Перенаправляем вывод
    original_stdout = sys.stdout
    sys.stdout = DualOutput("prisoners_simulation.log")
    
    try:
        num_prisoners = 100
        max_attempts = 50
        
        # Генерация ящиков
        boxes = random.sample(range(1, num_prisoners + 1), num_prisoners)
        
        # Вывод ВСЕХ ящиков
        print(f"\n{Fore.YELLOW}▄ Полный список ящиков (номер: содержимое):{Style.RESET_ALL}")
        for i in range(0, num_prisoners, 10):
            chunk = boxes[i:i+10]
            print(' | '.join(f"{i+k+1:3d}: {Fore.CYAN}{chunk[k]:3d}{Style.RESET_ALL}" for k in range(len(chunk))))
        
        print(f"\n{Fore.MAGENTA}▄▄▄ Начало симуляции (100 заключённых, 50 попыток) ▄▄▄{Style.RESET_ALL}")
        stats = {
            "success": [],
            "fail_list": [],
            "max_length": 0,
            "min_length": float('inf'),
            "paths": {}
        }

        for prisoner in range(1, num_prisoners + 1):
            current_box = prisoner
            path = []
            found = False
            
            print(f"\n{Fore.BLUE}■ Заключённый {prisoner:3d}:{Style.RESET_ALL}")
            for attempt in range(1, max_attempts + 1):
                number_in_box = boxes[current_box - 1]
                path.append(f"{current_box}→{number_in_box}")
                
                print(f"Попытка {attempt:2d}: Ящик {current_box:3d} → {number_in_box:3d}", end="")
                
                if number_in_box == prisoner:
                    found = True
                    path_length = len(path)
                    stats["success"].append(path_length)
                    stats["max_length"] = max(stats["max_length"], path_length)
                    stats["min_length"] = min(stats["min_length"], path_length)
                    stats["paths"][prisoner] = path
                    print(f" {Fore.GREEN}★ НАЙДЕНО!{Style.RESET_ALL} (путь: {path_length} шагов)")
                    print(f"   Полный маршрут: {' → '.join(path)}")
                    break
                print()  # Перенос строки, если не найден
                current_box = number_in_box
            
            if not found:
                actual_box = boxes.index(prisoner) + 1
                stats["fail_list"].append((prisoner, actual_box))
                stats["paths"][prisoner] = path
                print(f"{Fore.RED}✖ ПРОВАЛ!{Style.RESET_ALL} (последний ящик: {current_box}→{number_in_box})")
                print(f"   Полный маршрут: {' → '.join(path)}")
                print(f"   {Fore.RED}Номер {prisoner} был в ящике {actual_box}{Style.RESET_ALL}")

        # Итоговая статистика
        print(f"\n{Fore.MAGENTA}▄▄▄ Итоговые результаты ▄▄▄{Style.RESET_ALL}")
        print(f"🔹 Успешных: {len(stats['success'])}/{num_prisoners}")
        print(f"🔹 Провалов: {len(stats['fail_list'])}/{num_prisoners}")
        
        if stats["fail_list"]:
            print(f"\n{Fore.RED}✖ Список неудачников:{Style.RESET_ALL}")
            for prisoner, actual_box in stats["fail_list"]:
                print(f"   • Закл. {prisoner:3d} — его номер был в ящике {actual_box:3d}")
        
        if stats["success"]:
            print(f"\n{Fore.GREEN}★ Статистика успешных попыток:{Style.RESET_ALL}")
            print(f"   Макс. длина пути: {stats['max_length']} шагов")
            print(f"   Мин. длина пути: {stats['min_length']} шагов")
            print(f"   Средняя длина: {sum(stats['success'])/len(stats['success']):.1f} шагов")

    finally:
        # Восстанавливаем стандартный вывод
        sys.stdout.log.close()
        sys.stdout = original_stdout
        print("\nРезультаты сохранены в prisoners_simulation.log")

# Запуск
full_detailed_simulation()