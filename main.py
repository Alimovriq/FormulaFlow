import sys

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QApplication
from chem.gui import ChemistryTab, PeriodicTableTab
# from diagram.editor import DiagramEditor


class MainWindow(QMainWindow):
    """
    Главное окно приложения.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FormulaFlow v1.0")
        self.setGeometry(100, 100, 1200, 900)

        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.addTab(ChemistryTab(), "Расчет формул")
        self.tabs.addTab(PeriodicTableTab(), "Таблица Менделеева")
        # self.tabs.addTab(DiagramEditor(), "Схемы")

        self.setCentralWidget(self.tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
