from ellipticcurve import EllipticCurve
from finitefieldgroup import FiniteFieldGroup


def main():
    # --- Часть 1 & 2: Группа остатков по модулю (умножение) ---
    print("\n" + "="*80)
    print("--- ЧАСТЬ 1 & 2: ГРУППА ОСТАТКОВ ПО МОДУЛЮ (УМНОЖЕНИЕ) ---")
    print("="*80 + "\n")

    P_input = int(input("Введите простое число P для группы остатков (например, 7): "))
    try:
        group = FiniteFieldGroup(P_input)
        print("\n" + "-"*50)
        group.print_multiplication_table()
        print("\n" + "-"*50)
        group.print_element_orders_table()
    except ValueError as e:
        print(f"Ошибка: {e}")

    # --- Часть 3: Эллиптические кривые ---
    print("\n" + "="*80)
    print("--- ЧАСТЬ 3: ЭЛЛИПТИЧЕСКИЕ КРИВЫЕ ---")
    print("="*80 + "\n")

    EC_P = 7
    EC_A = 1
    EC_B = 3
    print(f"Используем эллиптическую кривую Y^2 = X^3 + {EC_A}X + {EC_B} mod {EC_P}")

    try:
        curve = EllipticCurve(EC_A, EC_B, EC_P)

        # Демонстрация группового закона (таблица сложения)
        print("\n" + "-"*50)
        curve.print_group_addition_table()

        # Демонстрация порядка элемента и генераторов
        print("\n" + "-"*50)
        curve.print_generator_table()

        # Тестирование M-кратной композиции
        print("\n" + "-"*50)
        print("--- Тестирование M-кратной композиции (scalar_multiply) ---")
        points_on_curve = curve.find_all_points()
        if len(points_on_curve) > 1:
            test_point = points_on_curve[1] # Берем первую не бесконечную точку, например (4,1)
            print(f"Тестовая точка: {test_point}")

            # Проверяем на отрицательный скаляр также
            test_scalars = list(range(1, len(points_on_curve) + 2)) + [-1, -2]
            for m_val in test_scalars:
                result_mP = curve.scalar_multiply(m_val, test_point)
                print(f"{m_val} * {test_point} = {result_mP}")
        else:
            print("На кривой недостаточно точек для тестирования M-кратной композиции.")
    except ValueError as e:
        print(f"Ошибка при инициализации эллиптической кривой: {e}")

if __name__ == '__main__':
    main()