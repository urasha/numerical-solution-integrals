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
            y = np.vectorize(func)(x)

        self.ax.clear()
        self.ax.set_facecolor('#f7f7f7')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        self.ax.plot(x, y, label='f(x)', color='#3366cc', linewidth=2)
        self.ax.axvline(x=a, color='#e53935', linestyle='--', linewidth=1.5, label='a')
        self.ax.axvline(x=b, color='#43a047', linestyle='--', linewidth=1.5, label='b')

        self.ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        self.ax.legend(frameon=False, fontsize=10)

        self.ax.set_title('График функции с пределами интегрирования', fontsize=12, fontweight='bold')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('f(x)')

        self.canvas.draw()
