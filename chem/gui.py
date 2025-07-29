import periodictable.core
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QTextEdit, QHBoxLayout, QGridLayout)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from periodictable import elements

from chem.core import parse_formula, calculate_molar_mass
from chem.constants import CATEGORY_COLORS, ELEMENT_POSITIONS, ELEMENTS_RU


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

        self.element_search = QLineEdit(placeholderText="Введите название (водород, железо)")
        self.search_btn = QPushButton("Найти символ")
        self.symbol_result_label = QLabel("Результат:")
        self.symbol_result_area = QTextEdit(readOnly=True)

        # Кнопки расчетов
        self.mass_btn = QPushButton("Молярная масса")
        self.composition_btn = QPushButton("Состав")
        # self.balance_btn = QPushButton("Балансировка")

        self.setup_ui()

    def setup_ui(self) -> None:

        layout = QGridLayout()

        layout.addWidget(QLabel("Поиск элемента"), 0, 0)
        layout.addWidget(self.element_search, 0, 1)
        layout.addWidget(self.search_btn, 0, 2)
        layout.addWidget(self.symbol_result_area, 2, 0, 1, 4)

        layout.addWidget(QLabel("Расчет формулы:"), 3, 0)
        layout.addWidget(self.formula_input, 3, 1)
        layout.addWidget(self.calculate_btn, 3, 2)
        layout.addWidget(self.result_area, 4, 0, 1, 4)

        self.setLayout(layout)
        self.search_btn.clicked.connect(self.find_symbol)
        self.calculate_btn.clicked.connect(self.calculate)

    def calculate(self) -> None:
        """
        Высчитывает малярную массу и ее состав.
        Биндится на кнопку "рассчитать"
        """

        formula = self.formula_input.text().strip()
        print(f"FORMULA, {formula}")
        if not formula:
            self.result_area.setHtml(
                f"<font color='red'>Необходимо ввести формулу</font>")
        else:
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

    def show_similar_names(self, name: str) -> None:
        """
        Ищет схожие элементы
        """
        similar = [k for k in ELEMENTS_RU if name in k or k.startswith(name[:3])]
        if similar:
            self.symbol_result_area.setText(
                "Возможные варианты:\n" +
                "\n".join(f"{k} → {ELEMENTS_RU[k]}" for k in similar)
            )

    def find_symbol(self) -> None:
        """
        Поиск химических элементов по названиям на русском языке
        """
        name = self.element_search.text().strip().lower()

        if name in ELEMENTS_RU:
            symbol = ELEMENTS_RU[name]
            # elem = elements[symbol]  # Получаем данные элемента

            self.symbol_result_area.setText(
                f"<b>{symbol}</b><br>"
                # f"Атомный номер: {elem.number}<br>"
                # f"Атомная масса: {elem.mass:.2f}"
            )
        else:
            self.symbol_result_area.setText("Не найдено")
            self.show_similar_names(name)


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
