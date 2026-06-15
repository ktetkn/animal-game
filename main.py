# Импортируем функции из других модулей
from guess_the_animal import (GuessTheAnimal)

def get_user_choice():
    # Получение выбора пользователя с обработкой ошибок
    while True:
        try:
            choice = input("Пожалуйста, сделайте выбор: ").strip()
            if not choice:
                print("Ошибка: Введите число!")
                continue
                
            choice_int = int(choice)
            
            if choice_int < 0 or choice_int > 2:
                print("Ошибка: Введите число от 0 до 2!")
                continue
    
            return choice_int
            
        except ValueError:
            print("Ошибка: Введите корректное число!")
        except KeyboardInterrupt:
            print("Программа прервана пользователем.")
            return 0

def execute_function(choice, game):
    # Выполнение выбранной функции
    if choice == 0:
            print("Завершение работы...\n")
            return False
    elif choice == 1:
        print("Отлично! Начнём игру:")
        game.play()
    elif choice == 2:
        while True:
            print("\n     Статистика по играм:\n")
            game.print_tree()
            game.get_most_informative_questions()
            game.get_average_depth_analysis()
            input("\nНажмите enter чтобы вернуться в главное меню")
            break
        
    else:
            print("Ошибка: такого выбора нет!")
    return True

def main():
    '''
    Основная функиця
    '''
    print("Добро пожаловать в игру «Угадай животное»!\n")
    # Запускаем игру
    game = GuessTheAnimal()
    game.create_default_tree()
    # Основной цикл программы
    continue_program = True
    while continue_program:
        print("Хотите сыграть?\n1 - Да\n2 - Узнать статистику\n0 - Нет\n")
        choice = get_user_choice()
        continue_program = execute_function(choice, game)
    print("Возвращайтесь ещё!")

if __name__ == "__main__":
    main()