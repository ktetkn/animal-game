class Node:
    def __init__(self, value, is_question=False):
        self.value = value
        self.is_question = is_question
        self.left = None # сюда кладем нет
        self.right = None # сюда кладем да
        self.ask_count = 0
        self.success_count = 0

from stack_question import Stack
class GuessTheAnimal:
    def __init__(self):
        self.root = None
        self.history = Stack()
        self.depths = []

    def create_default_tree(self):
        self.root = Node( "Ваше животное умеет летать?", True)
        flying_question = Node("Живёт ли оно на фермах?", True)
        self.root.right = flying_question
        
        # летающие
        flying_question.left = Node("сокол")
        flying_question.right = Node("курочка")
        
        not_flying_question = Node("Оно живет в воде?", True)
        self.root.left = not_flying_question
        
        # водные
        water_question = Node("Это рыба?", True)
        not_flying_question.right = water_question
        
        water_question.left = Node("лягушка")
        water_question.right = Node("щука")
        
        # наземные
        land_question = Node("Это крупное животное?", True)
        not_flying_question.left = land_question
        
        land_question.left = Node("кошка")
        land_question.right = Node("слон")

    def play(self):
        current = self.root
        depth = 0
        while current:
            if current.is_question:
                current.ask_count += 1
                print()
                answer = input(f"{current.value} (да/нет/назад): ").lower()
                
                if answer == "назад":
                    if not self.history.is_empty():
                        current = self.history.pop()
                        depth -= 1
                    else:
                        print("Вы уже в начале истории вопросов.")
                    continue
                
                if answer in ["да", "д", "y", "yes", "1"]:
                    self.history.push(current)
                    depth += 1
                    current = current.right
                elif answer in ["нет", "н", "n", "no", "0"]:
                    self.history.push(current)
                    depth += 1
                    current = current.left
                else:
                    print("Некорректный ответ!")
                    current.ask_count -= 1 
            else:
                print()
                answer = input(f"Это {current.value}? (да/нет): ").lower()
                if answer in ["да", "д", "y", "yes", "1"]:
                    print("\nУра! Я угадал!\n")
                    current.success_count += 1  # засчита победы животному
                    while not self.history.is_empty(): # подсчёт глубины
                        parent_node = self.history.pop()
                        parent_node.success_count += 1
                        
                    self.depths.append(depth)
                    return
                elif answer in ["нет", "н", "n", "no", "0"]:
                    self.learn(current)
                    return 
                else:
                    print("Некорректный ответ!")

    def learn(self, node):
        old_animal = node.value
        new_animal = input("Какое животное вы загадали?\n").lower()
        question = input(f"Введите вопрос, который отличает {new_animal} от {old_animal}:\n")
        while True:
            answer = input(f"Для животного {new_animal} ответ (да/нет): ").lower()
            node.value = question
            node.is_question = True
            if answer in ["да", "д", "y", "yes", "1"]:
                node.left = Node(old_animal)
                node.right = Node(new_animal)
                break
            elif answer in ["нет", "н", "n", "no", "0"]:
                node.left = Node(new_animal)
                node.right = Node(old_animal)
                break
            else:
                print("Некорректный ответ!")
        node.ask_count = 1
        node.success_count = 1
        print("Спасибо! Теперь я знаю новое животное.\n")

    def print_tree(self, node=None, prefix="", is_left=None):
        if node is None and prefix == "":
            node = self.root
            if node is None:
                print("Дерево пустое")
                return
        # поддерево "да"
        if node.right:
            self.print_tree(node.right, prefix + ("    " if is_left == False else "    "), False)
            
        if is_left is None:
            marker = ""  # корень
        elif is_left:
            marker = "  Нет - "  # левый узел
        else:
            marker = "  Да - "  # правый узел

        stats = f" (Побед: {node.success_count})" if not node.is_question else ""
        print(f"{prefix}{marker}{node.value}{stats}")

        # поддерево "нет"
        if node.left:
            self.print_tree(node.left, prefix + ("    " if is_left == False else "    "), True)
    
    def collect_questions(self, node, questions_list):
        '''
        рекурсивно собирает все вопросы
        '''
        if node is None:
            return
        if node.is_question:
            questions_list.append(node)
        self.collect_questions(node.left, questions_list)
        self.collect_questions(node.right, questions_list)
    
    def get_most_informative_questions(self):
        '''
        сортирует и выводит вопросы по частоте успешных угадываний
        '''
        all_questions = []
        self.collect_questions(self.root, all_questions)
        
        sorted_questions = sorted(all_questions, key=lambda x: (x.success_count / x.ask_count if x.ask_count > 0 else 0, x.ask_count), reverse=True)
        print("\n   Наиболее эффективные вопросы:")
        for i, j in enumerate(sorted_questions, 1):
            rate = j.success_count / j.ask_count * 100 if j.ask_count > 0 else 0 # процент успешных угадываний
            print(f"{i}. {rate:.1f}% {j.value} (Побед: {j.success_count}, Был задан: {j.ask_count})")

    def get_average_depth_analysis(self):
        '''
        Анализирует глубину вопросов (среднее количество шагов до угадывания)
        '''
        if not self.depths:
            print("\nЧтобы узнать глубину вопросов, сыграйте хотя бы один победный раунд.")
            return
        
        # для хранения глубины вопросов используем префиксные суммы
        prefix_sums = []
        prefix_sums.append(self.depths[0])
        for i in range(1, len(self.depths)):
            prefix_sums.append(prefix_sums[i-1] + self.depths[i])

        print("\n   Глубина вопросов")
        print(f"Всего успешных игр: {len(self.depths)}")
        print(f"История глубин раундов: {self.depths}")
        
        # среднее за все время
        total_sum = prefix_sums[-1]
        overall_avg = round(total_sum / len(self.depths))
        print(f"Среднее количество шагов до угадывания: {overall_avg}")

        # среднее за последние 3 игры
        if len(self.depths) >= 3:
            last_3_games = self.depths[-3:]
            last_avg = round(sum(last_3_games) / 3)
            print(f"Среднее количество шагов до угадывания за последние 3 игры: {last_avg}")