import time
from pynput import keyboard
from colorama import init
from locator import Locator

# Инициализация colorama для цветного текста в терминале
init()

# Глобальная переменная для доступа к объекту locator внутри колбэков
locator = None

def on_press(key):
    try:
        if key == keyboard.Key.down:
            locator.next_para(1)
            locator.load_para()
            locator.display_para()
            time.sleep(0.2)  # задержка для предотвращения повторных срабатываний

        elif key == keyboard.Key.up:
            locator.next_para(-1)
            locator.load_para()
            locator.display_para()
            time.sleep(0.2)

        elif key == keyboard.Key.left:
            locator.next_link(-1)
            locator.display_para()
            time.sleep(0.2)

        elif key == keyboard.Key.right:
            locator.next_link(1)
            locator.display_para()
            time.sleep(0.2)

        elif key == keyboard.Key.space:
            locator.go_link()
            locator.next_para(1)
            locator.load_para()
            locator.display_para()
            time.sleep(0.2)

        elif key == keyboard.Key.esc:
            locator.close()
            print("Выход из программы...")
            # Останавливаем слушатель, возвращая False
            return False
    except Exception as e:
        print("Ошибка в обработчике клавиатуры:", e)

def main():
    global locator
    url = 'https://en.wikipedia.org/wiki/Tau_Ceti'
    locator = Locator(url)

    if locator.max_para == 0:
        print("На странице не найдено параграфов.")
        return
    else:
        print('''
========================= ИНТЕРНЕТ НАВИГАЦИЯ В ТЕРМИНАЛЕ =====================
Управление:
Стрелки вверх / вниз   ->  вывод следующего / предыдущего параграфа
Стрелки вправо / влево ->  активация следующей / предыдущей ссылки
Пробел                 ->  переход по активной ссылке
ESC                    ->  выход из программы    
        ''')
        locator.next_para(1)
        locator.load_para()
        locator.display_para()

    # Запускаем слушатель клавиатуры
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    main()