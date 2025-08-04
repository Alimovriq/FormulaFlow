from chempy import Substance
from periodictable import elements


def parse_formula(formula: str) -> dict:
    """
    Разбирает формулу на элементы с их массовой долей
    formula: - химическая формула
    """

    substance = Substance.from_formula(formula)
    composition = {}
    total_mass = substance.mass

    for atomic_number, atom_count in substance.composition.items():
        # Элемент по атомному номеру
        elem = elements[atomic_number]

        # Массовая доля
        mass_percent = (atom_count * elem.mass) / total_mass * 100
        composition[elem.symbol] = (atom_count, mass_percent)

    return composition


def calculate_molar_mass(formula: str) -> str :
    """
    Вычисляет молярную массу в g/mol.
    formula: - химическая формула
    """

    mass = Substance.from_formula(formula).mass
    return f"Молярная масса {formula} = {mass:.2f}"


def grams_to_moles(formula: str, grams: int | float) -> int | float:
    """
    Конвертация граммов в моли
    """

    molar_mass = Substance.from_formula(formula).mass
    return grams / molar_mass