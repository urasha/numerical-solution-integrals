import sys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QTextEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class IntegrationThread(QThread):
    result_ready = pyqtSignal(float, int, str)
    error_occurred = pyqtSignal(str)

    def __init__(self, func, a, b, epsilon, method):
        super().__init__()
        self.func = func
        self.a = a
        self.b = b
        self.epsilon = epsilon
        self.method = method

    def run(self):
        try:
            result, n = compute_integral(self.func, self.a, self.b, self.epsilon, self.method)
            self.result_ready.emit(result, n, self.method)
        except Exception as e:
            self.error_occurred.emit(str(e))


class FunctionManager:
    functions = {
        "x²": lambda x: x ** 2,
        "sin(x)": math.sin,
        "e^x": math.exp,
        "1/x²": lambda x: 1 / x ** 2,
        "1/x": lambda x: 1 / x,
        "1/√x": lambda x: 1 / math.sqrt(x),
        "-3x³-5x²+4x-2": lambda x: -3 * x ** 3 - 5 * x ** 2 + 4 * x - 2,
        "10": lambda x: 10,
        "1/√(2x-x²)": lambda x: 1 / math.sqrt(2 * x - x ** 2)
    }

    @staticmethod
    def get_discontinuity_points(func_name):
        return {
            "1/x": [0],
            "1/x²": [0],
            "1/√x": [0],
            "1/√(2x-x²)": [0, 2]
        }.get(func_name, [])


def rectangle_rule(func, a, b, n, mode="middle"):
    h = (b - a) / n
    result = 0.0
    for i in range(n):
        if mode == "left":
            x = a + i * h
        elif mode == "right":
            x = a + (i + 1) * h
        else:
            x = a + (i + 0.5) * h
        try:
            result += func(x)
        except:
            return float('inf')
    return result * h


def trapezoid_rule(func, a, b, n):
    h = (b - a) / n
    result = (func(a) + func(b)) / 2
    for i in range(1, n):
        try:
            result += func(a + i * h)
        except:
            return float('inf')
    return result * h


def simpson_rule(func, a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    result = func(a) + func(b)
    for i in range(1, n):
        coef = 3 + (-1) ** (i + 1)
        try:
            result += coef * func(a + i * h)
        except:
            return float('inf')
    return result * h / 3


methods = {
    "Левые прямоугольники": lambda f, a, b, n: rectangle_rule(f, a, b, n, "left"),
    "Правые прямоугольники": lambda f, a, b, n: rectangle_rule(f, a, b, n, "right"),
    "Средние прямоугольники": lambda f, a, b, n: rectangle_rule(f, a, b, n, "middle"),
    "Трапеции": trapezoid_rule,
    "Симпсон": simpson_rule
}

runge_coef = {
    "Левые прямоугольники": 1,
    "Правые прямоугольники": 1,
    "Средние прямоугольники": 3,
    "Трапеции": 3,
    "Симпсон": 15
}


def compute_integral(func, a, b, epsilon, method_name):
    method = methods[method_name]
    coef = runge_coef[method_name]
    n = 4
    prev_result = method(func, a, b, n)

    for _ in range(20):
        n *= 2
        new_result = method(func, a, b, n)
        if abs(new_result - prev_result) < coef * epsilon:
            return new_result, n
        prev_result = new_result

    return prev_result, n


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.thread = None

    def setup_ui(self):
        self.setWindowTitle("Численное интегрирование")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Выбор функции
        self.func_combo = QComboBox()
        self.func_combo.addItems(FunctionManager.functions.keys())
        layout.addWidget(QLabel("Выберите функцию:"))
        layout.addWidget(self.func_combo)

        # Поля ввода
        self.a_input = QLineEdit()
        self.b_input = QLineEdit()
        self.epsilon_input = QLineEdit("1e-6")
        layout.addWidget(QLabel("Нижний предел (a):"))
        layout.addWidget(self.a_input)
        layout.addWidget(QLabel("Верхний предел (b):"))
        layout.addWidget(self.b_input)
        layout.addWidget(QLabel("Точность (ε):"))
        layout.addWidget(self.epsilon_input)

        # Выбор метода
        self.method_combo = QComboBox()
        self.method_combo.addItems(methods.keys())
        layout.addWidget(QLabel("Метод интегрирования:"))
        layout.addWidget(self.method_combo)

        # Кнопки
        self.calculate_btn = QPushButton("Вычислить")
        self.calculate_btn.clicked.connect(self.start_calculation)
        layout.addWidget(self.calculate_btn)

        # Результаты
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

    def start_calculation(self):
        try:
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            epsilon = float(self.epsilon_input.text().replace(",", "."))
            func_name = self.func_combo.currentText()
            method = self.method_combo.currentText()
            func = FunctionManager.functions[func_name]

            # Проверка особенностей
            breakpoints = self.get_breakpoints(func, a, b)
            if breakpoints:
                self.handle_discontinuities(func, a, b, epsilon, method, breakpoints)
            else:
                self.run_integration(func, a, b, epsilon, method)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def get_breakpoints(self, func, a, b):
        breakpoints = []
        n_check = 1000
        h = (b - a) / n_check
        for i in range(n_check + 1):
            x = a + i * h
            try:
                func(x)
            except:
                breakpoints.append(x)
        return sorted(list(set(breakpoints)))

    def handle_discontinuities(self, func, a, b, epsilon, method, breakpoints):
        eps = 1e-10
        total = 0.0
        points = sorted([a, b] + breakpoints)

        for i in range(len(points) - 1):
            left = points[i] + eps if points[i] in breakpoints else points[i]
            right = points[i + 1] - eps if points[i + 1] in breakpoints else points[i + 1]

            if left >= right:
                continue

            try:
                part_result, n = compute_integral(func, left, right, epsilon, method)
                total += part_result
            except:
                QMessageBox.critical(self, "Ошибка", "Интеграл не существует")
                return

        self.result_display.setText(
            f"Результат: {total:.6f}\nМетод: {method}\n" +
            f"Особенности обработаны в точках: {breakpoints}"
        )

    def run_integration(self, func, a, b, epsilon, method):
        if self.thread and self.thread.isRunning():
            self.thread.terminate()

        self.thread = IntegrationThread(func, a, b, epsilon, method)
        self.thread.result_ready.connect(self.show_result)
        self.thread.error_occurred.connect(lambda e: QMessageBox.critical(self, "Ошибка", e))
        self.thread.start()

    def show_result(self, result, n, method):
        self.result_display.setText(
            f"Результат: {result:.6f}\n"
            f"Разбиений: {n}\n"
            f"Метод: {method}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())