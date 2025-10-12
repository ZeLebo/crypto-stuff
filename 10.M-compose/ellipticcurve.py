from utils import is_prime, mod_inverse
from ecpoint import ECPoint

class EllipticCurve:
    def __init__(self, A, B, P):
        if not is_prime(P):
            raise ValueError(f"Module {P} is not prime")
        self.A = A
        self.B = B
        self.P = P
        self.infinity_point = ECPoint(None, None, True)

        discriminant = (4 * A ** 3 + 27 * B**2) % P
        if discriminant == 0:
            print(f"Crivaya is singular")

    def is_on_curve(self, point):
        if point.is_infinity:
            return True
        lhs = (point.y ** 2) % self.P
        rhs = (point.x ** 3 + self.A * point.x + self.B) % self.P
        return lhs == rhs
    
    def find_all_points(self):
        points = [self.infinity_point]
        for x in range(self.P):
            rhs = (x ** 3 + self.A * x + self.B) % self.P
            for y in range(self.P):
                lhs = (y**2) % self.P
                if lhs == rhs:
                    points.append(ECPoint(x, y))
        points.sort(key=lambda p : (p.x, p.y) if not p.is_infinity else (-1, -1))
        return points
    
    def add_points(self, P1, P2):
        if P1.is_infinity:
            return P2
        if P2.is_infinity:
            return P1
        
        s = 0
        
        if P1.x == P2.x:
            if P1.y == 0:
                return self.infinity_point
            
            numerator = (3 * P1.x ** 2 + self.A) % self.P
            denominator = (2 * P1.y) % self.P
            s = (numerator * mod_inverse(denominator, self.P)) % self.P
        else:
            numerator = (P2.y - P1.y) % self.P
            denominator = (P2.x - P1.x) % self.P

            if denominator == 0:
                return self.infinity_point

            s = (numerator * mod_inverse(denominator, self.P)) % self.P

        x3 = (s**2 - P1.x - P2.x) % self.P
        y3 = (s * (P1.x - x3) - P1.y) % self.P

        return ECPoint(x3, y3)
    
    def scalar_multiply(self, k, P_start):
        """
        M-кратная козиция точки P
        """
        if k == 0 or P_start.is_infinity:
            return self.infinity_point
        if k < 0:
            k = k * -1
            P_start = -P_start

        R = self.infinity_point
        current_P = P_start

        while k > 0:
            if k & 1:
                R = self.add_points(R, current_P)
            current_P = self.add_points(current_P, current_P)
            k >>= 1

        return R

    def print_group_addition_table(self):
        """Выводит таблицу группового закона (сложения) для точек на кривой."""
        all_points = self.find_all_points()

        print(f"ДЕМОНСТРАЦИЯ ГРУППОВОГО ЗАКОНА КРИВАЯ Y^2 = X^3 + {self.A}X + {self.B} НАД ПОЛЕМ F_{self.P}")
        print(f"Все найденные точки ({len(all_points)}): {all_points}")

        point_str_len = max(len(str(p)) for p in all_points)
        formatted_points_header = [f"{str(p):<{point_str_len}s}" for p in all_points]

        header_line = "+" + "|" + "".join(fp for fp in formatted_points_header)
        print(header_line)
        print("-" * len(header_line))

        for p_row in all_points:
            row_str = f"{str(p_row):<{point_str_len}s}|"
            for p_col in all_points:
                result_point = self.add_points(p_row, p_col)
                row_str += f"{str(result_point):<{point_str_len}s}"
            print(row_str)

        print("\nСумма любых точек из группы принадлежит группе.")
        print("Для каждого элемента есть обратный, сумма которых равна нулевому элементу (O).")
        print("Например:")
        if len(all_points) > 1:
            P_example = all_points[1]
            neg_P_example = -P_example
            # (x, -y mod P)
            found_neg_P = None
            for p in all_points:
                if p.x == neg_P_example.x and (p.y % self.P) == (neg_P_example.y % self.P):
                    found_neg_P = p
                    break
            
            if found_neg_P:
                print(f"{P_example} + {found_neg_P} = {self.add_points(P_example, found_neg_P)}")
            else:
                print(f"Обратная точка для {P_example} ({neg_P_example}) не найдена в списке точек (возможна ошибка в реализации).")
        else:
            print("На кривой недостаточно точек для примера обратного элемента.")

    def print_generator_table(self):
        """Выводит таблицу M-кратной композиции точек и отмечает генераторы."""
        all_points = self.find_all_points()
        group_order = len(all_points)

        print(f"ПОНЯТИЕ ГЕНЕРАТОРА В ГРУППЕ ТОЧЕК НА ЭЛЛИПТИЧЕСКОЙ КРИВОЙ Y^2 = X^3 + {self.A}X + {self.B} НАД ПОЛЕМ F_{self.P}")
        print(f"Все найденные точки ({group_order}): {all_points}")

        point_str_len = max(len(str(p)) for p in all_points)
        formatted_kP_headers = [f"[{k}]P" for k in range(1, group_order + 1)]
        max_kP_len = max(len(h) for h in formatted_kP_headers)

        header_line = "P" + " |" + "".join(f"{h:<{max_kP_len}s}" for h in formatted_kP_headers)
        print(header_line)
        print("-" * len(header_line))

        generators = []

        for P_start in all_points:
            if P_start.is_infinity:
                row_str = f"{str(P_start):<{point_str_len}s}|"
                for _ in range(1, group_order + 1):
                    row_str += f"{str(self.infinity_point):<{max_kP_len}s}"
                print(row_str)
                continue
            
            generated_points = []
            current_sum = self.infinity_point
            for k_val in range(1, group_order + 1):
                current_sum = self.add_points(current_sum, P_start)
                generated_points.append(current_sum)

            order = 0
            for k_val, res_point in enumerate(generated_points, 1):
                if res_point == self.infinity_point:
                    order = k_val
                    break
            if order == 0:
                order = group_order

            row_str = f"{str(P_start):<{point_str_len}s}|"
            for res_point in generated_points:
                row_str += f"{str(res_point):<{max_kP_len}s}"
            
            if order == group_order:
                generators.append(P_start)
                row_str += f" (Генератор)"

            print(row_str)

        print("\n" + "="*50)
        if generators:
            print(f"Точки, генерирующие группу (Генераторы): {generators}.")
            print(f"Их порядок равен числу элементов группы ({group_order}).")
        else:
            print("Генераторы не найдены.")