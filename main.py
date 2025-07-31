import sys

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QApplication
from ui.MainWindow_ui import Ui_MainWindow
from chem.gui import ChemistryTab, PeriodicTableTab
# from diagram.editor import DiagramEditor


class MainWindow(QMainWindow):
    """
    Главное окно приложения.
    """

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # # Вкладки
        # 1. Химические вычисления
        chemistry_tab = self.ui.chemestry_operations
        if chemistry_tab.layout() is None:
            chemistry_tab.setLayout(QVBoxLayout())

        self.chemistry_widget = ChemistryTab()
        chemistry_tab.layout().addWidget(self.chemistry_widget)

        # self.ui.tabWidget.addTab(ChemistryTab(), "Расчет формул")
        # self.tabs = QTabWidget()
        # self.tabs.addTab(ChemistryTab(), "Расчет формул")
        # self.tabs.addTab(PeriodicTableTab(), "Таблица Менделеева")
        # # self.tabs.addTab(DiagramEditor(), "Схемы")
        #
        # self.setCentralWidget(self.tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
