import periodictable.core
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QTextEdit, QHBoxLayout)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from periodictable import elements

from chem.core import parse_formula, calculate_molar_mass
from chem.constants import CATEGORY_COLORS, ELEMENT_POSITIONS


class ChemistryTab(QWidget):
    """
    Класс для вкладки вычисления химических показателей
    """

    def __init__(self) -> None:

        super().__init__()
        self.formula_input = QLineEdit(placeholderText="Введите формулу (H2SO4)")
        self.calculate_btn = QPushButton("Рассчитать")
        self.result_label = QLabel("Результат:")
        self.result_area = QTextEdit(readOnly=True)

        # Кнопки расчетов
        self.mass_btn = QPushButton("Молярная масса")
        self.composition_btn = QPushButton("Состав")
        # self.balance_btn = QPushButton("Балансировка")

        self.setup_ui()

    def setup_ui(self) -> None:

        layout = QVBoxLayout()

        # Верхняя панель
        top_layout = QHBoxLayout()
        # top_layout.addWidget(QLabel("Формула:"))
        top_layout.addWidget(self.formula_input)
        top_layout.addWidget(self.calculate_btn)

        # Панель кнопок
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.mass_btn)
        btn_layout.addWidget(self.composition_btn)
        # btn_layout.addWidget(self.balance_btn)

        layout.addLayout(top_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.result_area)

        # Кнопки
        # self.mass_btn.clicked.connect(self.calculate)
        # self.composition_btn.clicked.connect(self.calculate)
        # self.balance_btn.clicked.connect(self.balance_equation)
        self.calculate_btn.clicked.connect(self.calculate)

        self.setLayout(layout)

    def calculate(self) -> None:
        """
        Высчитывает малярную массу и ее состав.
        Биндится на кнопку "рассчитать"
        """

        formula = self.formula_input.text().strip()
        if not formula:
            self.result_area.setHtml(
                f"<font color='red'>Необходимо ввести формулу</font>")

        try:
            mass = calculate_molar_mass(formula)
            composition = parse_formula(formula)
        except Exception as err:
            self.result_area.setHtml(f"<font color='red'>{err}</font>")
            return

        # Форматируем вывод
        result_html = [
            f"<b>Формула:</b> {formula}",
            f"<b>Молярная масса:</b> {mass} g/mol",
            "<br><b>Состав:</b>"
        ]

        for elem, (count, percent) in composition.items():
            result_html.append(
                f"- {elem}: {count} атом(a/ов) → {percent:.2f}%"
            )

        self.result_area.setHtml("<br>".join(result_html))


class PeriodicTableTab(QWidget):
    """
    Периодическая таблица Менделеева.
    """

    def __init__(self) -> None:

        super().__init__()
        self.table = None
        self.legend = None
        self.init_ui()

    def init_ui(self) -> None:

        layout = QVBoxLayout()

        # Таблица: 10 строк x 18 столбцов
        self.table = QTableWidget(9, 18)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        # Размеры ячеек
        for col in range(18):
            self.table.setColumnWidth(col, 60)
        for row in range(9):
            self.table.setRowHeight(row, 60)

        # Заполняем таблицу
        for elem in elements:
            elem: periodictable.core.Element
            if elem.number in ELEMENT_POSITIONS:
                row, col = ELEMENT_POSITIONS[elem.number]
                item = QTableWidgetItem(f"{elem.symbol}\n{elem.number}")
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(QFont("Arial", 10, QFont.Bold))
                category = self.get_element_category(elem)

                if category in CATEGORY_COLORS:
                    item.setBackground(CATEGORY_COLORS[category])
                    item.setForeground(QColor(0, 0, 0))

                self.table.setItem(row, col, item)

        self.legend = self.create_legend()
        layout.addWidget(self.legend)
        layout.addWidget(self.table)
        self.setLayout(layout)

    @staticmethod
    def create_legend() -> QLabel:
        """
        Создает легенду цветов для таблицы Менделеева
        """

        legend_html = """
        <div style="
            background: white;
            padding: 10px;
            border-radius: 5px;
            font-family: Arial;
            font-size: 12px;
        ">
            <h3 style="margin-top: 0; text-align: center;">Легенда</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 5px;">
                <div style="background-color: rgb(255, 182, 193); padding: 5px; border-radius: 3px;">Щелочные металлы</div>
                <div style="background-color: rgb(255, 228, 181); padding: 5px; border-radius: 3px;">Щелочноземельные</div>
                <div style="background-color: rgb(179, 229, 252); padding: 5px; border-radius: 3px;">Переходные металлы</div>
                <div style="background-color: rgb(220, 220, 220); padding: 5px; border-radius: 3px;">Металлы</div>
                <div style="background-color: rgb(144, 238, 144); padding: 5px; border-radius: 3px;">Неметаллы</div>
                <div style="background-color: rgb(255, 255, 153); padding: 5px; border-radius: 3px;">Полуметаллы</div>
                <div style="background-color: rgb(255, 215, 0); padding: 5px; border-radius: 3px;">Галогены</div>
                <div style="background-color: rgb(173, 216, 230); padding: 5px; border-radius: 3px;">Инертные газы</div>
                <div style="background-color: rgb(255, 160, 122); padding: 5px; border-radius: 3px;">Лантаноиды</div>
                <div style="background-color: rgb(255, 105, 180); padding: 5px; border-radius: 3px;">Актиноиды</div>
            </div>
        </div>
        """

        legend = QLabel(legend_html)
        legend.setTextFormat(Qt.RichText)
        legend.setAlignment(Qt.AlignCenter)
        return legend

    @staticmethod
    def get_element_category(elem):
        """
        Возвращает тип химического элемента
        elem:
        """
        if 57 <= elem.number <= 71: return "lanthanide"
        if 89 <= elem.number <= 103: return "actinide"
        if elem.number in [1, 6, 7, 8, 15, 16, 34]: return "nonmetal"
        if elem.number in [9, 17, 35, 53, 85, 117]: return "halogen"
        if elem.number in [2, 10, 18, 36, 54, 86, 118]: return "noble"
        if elem.number in [3, 11, 19, 37, 55, 87]: return "alkali"
        if elem.number in [4, 12, 20, 38, 56, 88]: return "alkaline"
        if 21 <= elem.number <= 30: return "transition"
        if 39 <= elem.number <= 48: return "transition"
        if 72 <= elem.number <= 80: return "transition"
        if 104 <= elem.number <= 112: return "transition"
        return "metal"
