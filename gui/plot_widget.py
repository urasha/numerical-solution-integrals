import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class PlotCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_function(self, func, a, b):
        x = np.linspace(a - (b - a) * 0.1, b + (b - a) * 0.1, 1000)
        try:
            y = func(x)
        except Exception:
            y = np.vectorize(func)(x)  # For functions not supporting array input

        self.ax.clear()
        self.ax.plot(x, y, label='f(x)')
        self.ax.axvline(x=a, color='red', linestyle='--', label='a')
        self.ax.axvline(x=b, color='green', linestyle='--', label='b')
        self.ax.legend()
        self.ax.set_title('График функции с пределами интегрирования')
        self.canvas.draw()