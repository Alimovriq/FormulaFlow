import sys

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QApplication
from ui.MainWindow_ui import Ui_MainWindow
from chem.gui import ChemistryTab, PeriodTableTab


class MainWindow(QMainWindow):
    """
    Главное окно приложения.
    """

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        chemistry_tab = self.ui.chemestry_operations
        if chemistry_tab.layout() is None:
            chemistry_tab.setLayout(QVBoxLayout())

        self.chemistry_widget = ChemistryTab()
        chemistry_tab.layout().addWidget(self.chemistry_widget)

        periodic_table_tab = self.ui.periodic_table
        if periodic_table_tab.layout() is None:
            periodic_table_tab.setLayout(QVBoxLayout())
        self.periodic_table_widget = PeriodTableTab()
        periodic_table_tab.layout().addWidget(self.periodic_table_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
