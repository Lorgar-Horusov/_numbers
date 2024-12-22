import math


class CodesEquallyTree:
    def __init__(self):
        self._polynomials = {
            1: ["X^1+1"],
            2: ["X^2+X+1"],
            3: ["X^3+X+1", "X^3+X^2+1"],
            4: ["X^4+X+1", "X^4+X^3+1", "X^4+X^3+X^2+X+1"],
            5: ["X^5+X^2+1", "X^5+X^3+1", "X^5+X^3+X^2+X+1", "X^5+X^4+X^2+X+1", "X^5+X^4+X^3+X+1", "X^5+X^4+X^3+X^2+1"],
            6: ["X^6+X+1"],
            7: ["X^7+X^3+1"],
            8: ["X^8+X^4+X^3+X^2+1"],
            9: ["X^9+X^4+1"],
            10: ["X^10+X^3+1"]
        }

    @staticmethod
    def calculate_m(k=None, n=None):
        if k is not None:
            m = math.ceil(math.log2((k + 1) + math.ceil(math.log2(k + 1))))
        elif n is not None:
            m = 0
            while True:
                if math.ceil(math.log2(n + 1)) == m:
                    break
                m += 1
        else:
            raise ValueError("Необходимо указать либо k, либо n")

        return m

    def select_polynomial(self, m, d):
        if m in self._polynomials:
            candidates = [poly for poly in self._polynomials[m] if self.count_non_zero_terms(poly) >= d]
            if candidates:
                selected_polynomial = min(candidates, key=self.count_non_zero_terms)
                return selected_polynomial
        return None

    @staticmethod
    def count_non_zero_terms(polynomial):
        return polynomial.count('X') + polynomial.count('1')

    def polynomial_to_binary_string(self, poly):
        terms = poly.replace('-', '+-').split('+')
        max_degree = 0
        binary_rep = {}

        for term in terms:
            if term:
                if 'X' in term:
                    if '^' in term:
                        degree = int(term.split('^')[1])
                    else:
                        degree = 1
                else:
                    degree = 0
                binary_rep[degree] = 1

                max_degree = max(max_degree, degree)

        binary_str = ''.join(str(binary_rep.get(i, 0)) for i in range(max_degree, -1, -1))

        return binary_str

    def binary_multiply(self, gx, m):
        # Умножаем gx на x^m через сдвиг влево
        gx = int(gx, 2) if isinstance(gx, str) else gx  # Убедимся, что gx — это число
        result = gx << m  # Сдвиг влево на m битов
        return bin(result)[2:]  # Возвращаем двоичное представление

    def binary_divide(self, gx, px):
        gx = int(gx, 2)  # Преобразуем в целые числа
        px = int(px, 2)

        qx = 0  # Частное
        while gx.bit_length() >= px.bit_length():  # Пока остаток можно делить
            shift = gx.bit_length() - px.bit_length()  # Определяем сдвиг
            qx ^= (1 << shift)  # Добавляем 1 в частное на нужную позицию
            gx ^= (px << shift)  # Вычитаем делитель сдвинутый влево

        # Преобразуем остаток и частное в двоичную строку
        qx_binary = bin(qx)[2:]
        gx_binary = bin(gx)[2:]

        # Дополняем остаток до нужной длины
        remainder_length = len(str(px)) - 1 # Длина остатка, обычно это степень многочлена
        gx_binary = gx_binary.zfill(remainder_length)  # Дополняем остаток до нужной длины

        return qx_binary, gx_binary  # Возвращаем частное и остаток в двоичной форме


    def binary_multiply_with_xor(self, px_binary, qx_binary):
        # Преобразуем двоичные строки в целые числа
        px_binary_int = int(px_binary, 2)
        qx_binary_int = int(qx_binary, 2)

        # Начинаем обычное умножение в столбик
        result = 0
        shift = 0

        while qx_binary_int > 0:
            # Если младший бит qx_binary_int равен 1, добавляем px_binary_int с текущим сдвигом
            if qx_binary_int & 1:
                result ^= px_binary_int << shift  # XOR вместо сложения

            # Переходим к следующему биту qx_binary_int
            qx_binary_int >>= 1
            shift += 1

        # Преобразуем результат обратно в двоичную строку
        return bin(result)[2:]  # Возвращаем без префикса '0b'

    def construct_cyclic_code(self, gx, m, px):
        # Вычисление G(x) * x^m
        gx_xm_binary = self.binary_multiply(gx, m)

        # Деление G(x)x^m на P(x), получение Q(x) и R(x)
        qx_binary, rx_binary = self.binary_divide(gx_xm_binary, px)

        # Формирование F(x) = G(x)x^m XOR R(x)
        # Здесь мы используем XOR для вычисления F(x) после сдвига
        fx_binary = bin(int(gx_xm_binary, 2) ^ int(rx_binary, 2))[2:]

        # Проверка F(x) через P(x) * Q(x)
        # Ensure px is passed as binary string
        px_binary = bin(int(px, 2))[2:]

        px_binary_int = int(px_binary, 2)  # px_binary should now be a string
        qx_binary_int = int(qx_binary, 2)
        pq_binary = self.binary_multiply_with_xor(px_binary, qx_binary)

        # Сохраняем результаты в словарь
        result = {
            "Gx_xm_binary": gx_xm_binary,
            "Qx_binary": qx_binary,
            "Rx_binary": rx_binary,
            "Fx_binary": fx_binary,
            "PQ_binary": pq_binary,
        }

        return result


class HammingCodes:
    def __init__(self):
        pass

    def calculate_m(self, *args):
        if len(args) != 4:
            raise ValueError("HammingCodes requires exactly 4 arguments.")
        k4, k3, k2, k1 = args
        m1 = k4 ^ k3 ^ k1
        m2 = k4 ^ k2 ^ k1
        m3 = k3 ^ k2 ^ k1
        return [m1, m2, m3]

    def complectate_mk(self, k: list, m: list):
        m1, m2, m3 = m
        k4, k3, k2, k1 = k
        mk = [m1, m2, k4, m3, k3, k2, k1]
        return mk

    def find_errors(self, k_original: list, mk_test: list):
        k_original = [int(bit) for bit in k_original]
        calculated_m_orig = self.calculate_m(*k_original)
        mk_orig = self.complectate_mk(k_original, calculated_m_orig)
        mtest1, m2test, k4test, m3test, k3test, k2test, k1test = mk_test
        ktest = [k1test, k2test, k3test, k4test]
        calculated_m = self.calculate_m(*ktest)
        print(mk_orig)
        print(mk_test)
        # Сравниваем рассчитанные значения m с переданными
        errors = []
        for i, j in enumerate(mk_orig):
            print(i, j)
            if j != mk_test[i]:
                errors.append(i+1)
        return errors


class CodesEquallyFour:
    def __init__(self):
        self._polynomials = {
            1: ["X^1+1"],
            2: ["X^2+X+1"],
            3: ["X^3+X+1", "X^3+X^2+1"],
            4: ["X^4+X+1", "X^4+X^3+1", "X^4+X^3+X^2+X+1"],
            5: ["X^5+X^2+1", "X^5+X^3+1", "X^5+X^3+X^2+X+1", "X^5+X^4+X^2+X+1", "X^5+X^4+X^3+X+1", "X^5+X^4+X^3+X^2+1"],
            6: ["X^6+X+1"],
            7: ["X^7+X^3+1"],
            8: ["X^8+X^4+X^3+X^2+1"],
            9: ["X^9+X^4+1"],
            10: ["X^10+X^3+1"]
        }

    @staticmethod
    def calculate_m(k=None, n=None):
        if k is not None:
            m = 1 + math.ceil(math.log2((k + 1) + math.ceil(math.log2(k + 1))))
        elif n is not None:
            m = 0
            while True:
                if math.ceil(math.log2(n + 1)) == m:
                    break
                m += 1
        else:
            raise ValueError("Необходимо указать либо k, либо n")

        return m

    def select_polynomial(self, m, d):
        if m in self._polynomials:
            candidates = [poly for poly in self._polynomials[m] if self.count_non_zero_terms(poly) >= d]
            if candidates:
                selected_polynomial = min(candidates, key=self.count_non_zero_terms)
                return selected_polynomial
        return None

    @staticmethod
    def count_non_zero_terms(polynomial):
        return polynomial.count('X') + polynomial.count('1')


if __name__ == "__main__":
    ecc = CodesEquallyTree()

    gx = "1100"  # Пример G(x)
    k = len(gx)
    print(f"Значение k: {k}")

    m = ecc.calculate_m(k=k)
    print(f"Значение m: {m}")

    d = 3  # Минимальное кодовое расстояние
    selected_polynomial = ecc.select_polynomial(m, d)
    print(f"Выбранный многочлен P(x): {selected_polynomial}")

    px_binary = ecc.polynomial_to_binary_string(selected_polynomial)
    print(f"P(x) в двоичной форме: {px_binary}")

    # Вызываем метод и сохраняем все результаты
    results = ecc.construct_cyclic_code(gx, m, px_binary)

    # Теперь данные доступны в словаре results
    Gx_xm_binary = results["Gx_xm_binary"]
    Qx_binary = results["Qx_binary"]
    Rx_binary = results["Rx_binary"]
    Fx_binary = results["Fx_binary"]
    PQ_binary = results["PQ_binary"]

    print(f"G(x) * x^m: {Gx_xm_binary}")
    print(f"Частное Q(x): {Qx_binary}")
    print(f"Остаток R(x): {Rx_binary}")
    print(f"F(x): {Fx_binary}")
    print(f"P(x) * Q(x): {PQ_binary}")
    print("-----")

    # Пример использования
    hamming = HammingCodes()
    k_values = [1, 1, 0, 0]  # k4, k3, k2, k1
    m_values = hamming.calculate_m(*k_values)
    mk = hamming.complectate_mk(k_values, m_values)

    # Проверка на ошибки
    mk_test = [1, 1, 1, 1, 1, 0, 0]  # Пример тестового значения
    error_positions = hamming.find_errors(k_values, mk_test)
    print(error_positions)

    if error_positions:
        print(f"Ошибки найдены на позициях: {error_positions}")
        print(f'оригинал {mk}')
        print(f'тест {mk_test}')
    else:
        print("Ошибок не найдено.")

