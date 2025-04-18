from PyQt5 import QtWidgets

from integration.adaptive import handle_improper_integral
from integration.functions import FUNCTIONS

from gui.plot_widget import PlotCanvas


class IntegrationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Численное интегрирование")
        self.setGeometry(100, 100, 500, 400)
        self.setup_ui()

    def setup_ui(self):
        widget = QtWidgets.QWidget()

        # Основной вертикальный лейаут
        main_layout = QtWidgets.QVBoxLayout()

        # Лейаут формы
        form_layout = QtWidgets.QFormLayout()

        self.func_combo = QtWidgets.QComboBox()
        for fname in FUNCTIONS.keys():
            self.func_combo.addItem(fname)
        form_layout.addRow("Функция:", self.func_combo)

        self.a_input = QtWidgets.QLineEdit()
        self.b_input = QtWidgets.QLineEdit()
        form_layout.addRow("Нижний предел (a):", self.a_input)
        form_layout.addRow("Верхний предел (b):", self.b_input)

        self.tol_input = QtWidgets.QLineEdit()
        self.tol_input.setPlaceholderText("например, 0.01")
        form_layout.addRow("Точность:", self.tol_input)

        self.method_combo = QtWidgets.QComboBox()
        self.method_combo.addItem("Прямоугольники (левые)")
        self.method_combo.addItem("Прямоугольники (правые)")
        self.method_combo.addItem("Прямоугольники (средние)")
        self.method_combo.addItem("Трапеции")
        self.method_combo.addItem("Симпсона")
        form_layout.addRow("Метод:", self.method_combo)

        self.calc_button = QtWidgets.QPushButton("Вычислить интеграл")
        self.calc_button.clicked.connect(self.calculate_integral)
        form_layout.addRow(self.calc_button)

        self.result_text = QtWidgets.QTextEdit()
        self.result_text.setReadOnly(True)
        form_layout.addRow("Результат:", self.result_text)

        # Добавляем форму в основной лейаут
        main_layout.addLayout(form_layout)

        # Добавляем график в основной лейаут
        self.plot_canvas = PlotCanvas(self)
        self.plot_canvas.setMinimumHeight(300)  # Сделать график высоким
        main_layout.addWidget(self.plot_canvas)

        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def calculate_integral(self):
        func_name = self.func_combo.currentText()
        f = FUNCTIONS[func_name]
        try:
            a = float(self.a_input.text().replace(",", "."))
            b = float(self.b_input.text().replace(",", "."))
        except ValueError:
            self.result_text.setText("Ошибка: введите корректные пределы!")
            return

        try:
            tol = float(self.tol_input.text().replace(",", "."))
        except ValueError:
            self.result_text.setText("Ошибка: введите корректную точность!")
            return

        method_index = self.method_combo.currentIndex()
        if method_index == 0:
            method, variant = "rectangle", "left"
        elif method_index == 1:
            method, variant = "rectangle", "right"
        elif method_index == 2:
            method, variant = "rectangle", "middle"
        elif method_index == 3:
            method, variant = "trapezoidal", "left"
        elif method_index == 4:
            method, variant = "simpson", "left"
        else:
            self.result_text.setText("Ошибка: неизвестный метод интегрирования")
            return

        try:
            integral, n_final = handle_improper_integral(f, a, b, tol, method, variant)
        except Exception as ex:
            self.result_text.setText(str(ex))
            return

        result_str = f"Интеграл: {integral}\n"
        result_str += f"Использовано разбиений: {n_final}\n" if n_final is not None else "В случае симметричного разрыва разбиение не применялось (интеграл равен 0)\n"
        self.result_text.setText(result_str)

        self.plot_canvas.plot_function(f, a, b)
