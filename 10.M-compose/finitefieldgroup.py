from utils import is_prime

class FiniteFieldGroup:
    def __init__(self, P):
        if not is_prime(P):
            raise ValueError(f"P={P} должно быть простым числом для создания FiniteFieldGroup.")
        self.P = P
        self.elements = list(range(1, P)) # Элементы группы Z_P^*
        self.group_order = P - 1

    def print_multiplication_table(self):
        """Выводит таблицу умножения для остатков по модулю P."""
        print(f"ДЕМОНСТРАЦИЯ ГРУППОВОГО ЗАКОНА ДЛЯ УМНОЖЕНИЯ ОСТАТКОВ ПО МОДУЛЮ P={self.P}")

        header_elements = self.elements
        print("*" + " |" + "".join(f"{x:3d}" for x in header_elements))
        print("-" * (4 + self.group_order * 3))

        for i in header_elements:
            row_str = f"{i:3d}|"
            for j in header_elements:
                result = (i * j) % self.P
                row_str += f"{result:3d}"
            print(row_str)

    def get_element_order(self, a):
        """Вычисляет порядок элемента 'a' в группе."""
        if a not in self.elements:
            raise ValueError(f"Элемент {a} не принадлежит группе Z_{self.P}^*.")
        
        k = 1
        current_val = a
        while current_val != 1:
            current_val = (current_val * a) % self.P
            k += 1
        return k

    def print_element_orders_table(self):
        """Выводит таблицу порядков элементов и отмечает генераторы."""
        print(f"ПОНЯТИЕ ГЕНЕРАТОРА В ГРУППЕ ВЫЧЕТОВ ПО МОДУЛЮ P={self.P}")

        elements = self.elements
        generators = []

        # Заголовок таблицы
        header_powers = [f"a^{k}" for k in range(1, self.P)]
        print("a |" + "".join(f"{h:5s}" for h in header_powers) + " |Порядок")
        print("-" * (4 + self.group_order * 5 + 9))

        for a in elements:
            row_str = f"{a:2d} |"
            current_power_val = a
            powers_list = []
            for _ in range(1, self.P):
                powers_list.append(current_power_val)
                current_power_val = (current_power_val * a) % self.P

            for val in powers_list:
                row_str += f"{val:5d}"
            
            order = self.get_element_order(a)
            row_str += f" |{order:5d}"

            if order == self.group_order:
                generators.append(a)
                row_str += " (Генератор)"

            print(row_str)

        print("\n" + "="*50)
        if generators:
            print(f"Генераторы группы: {generators}. Их порядок равен числу элементов группы ({self.group_order}).")
        else:
            print("Генераторы не найдены.")