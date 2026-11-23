"""Registro sencillo de gastos personales desde la terminal."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
import json


@dataclass(frozen=True)
class Gasto:
    descripcion: str
    monto: Decimal
    fecha: date
    categoria: str


CATEGORIAS = ["Comida", "Transporte", "Vivienda", "Entretenimiento", "Salud", "Otros"]


def convertir_monto(valor: str) -> Decimal:
    """Convierte texto a un monto decimal positivo."""
    try:
        monto = Decimal(valor)
    except InvalidOperation as error:
        raise ValueError("El monto debe ser un número válido.") from error

    if not monto.is_finite() or monto <= 0:
        raise ValueError("El monto debe ser un número mayor que cero.")
    return monto


def guardar_gastos(gastos: list[Gasto], archivo: str = "gastos.json") -> None:
    """Guarda la lista de gastos en un archivo JSON."""
    gastos_dict = [
        {
            "descripcion": gasto.descripcion,
            "monto": str(gasto.monto),
            "fecha": gasto.fecha.isoformat(),
            "categoria": gasto.categoria,
        }
        for gasto in gastos
    ]
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(gastos_dict, f, indent=2, ensure_ascii=False)


def cargar_gastos(archivo: str = "gastos.json") -> list[Gasto]:
    """Carga la lista de gastos desde un archivo JSON."""
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            gastos_dict = json.load(f)
        return [
            Gasto(
                descripcion=g["descripcion"],
                monto=Decimal(g["monto"]),
                fecha=date.fromisoformat(g["fecha"]),
                categoria=g["categoria"],
            )
            for g in gastos_dict
        ]
    except FileNotFoundError:
        return []


def agregar_gasto(gastos: list[Gasto], descripcion: str, monto: Decimal, categoria: str) -> Gasto:
    """Valida y agrega un gasto a la lista."""
    descripcion = descripcion.strip()
    if not descripcion:
        raise ValueError("La descripción no puede estar vacía.")
    if not monto.is_finite() or monto <= 0:
        raise ValueError("El monto debe ser un número mayor que cero.")
    if categoria not in CATEGORIAS:
        raise ValueError(f"Categoría inválida. Las categorías válidas son: {', '.join(CATEGORIAS)}")

    gasto = Gasto(descripcion=descripcion, monto=monto, fecha=date.today(), categoria=categoria)
    gastos.append(gasto)
    return gasto


def calcular_total(gastos: list[Gasto]) -> Decimal:
    """Calcula el total de los gastos registrados."""
    return sum((gasto.monto for gasto in gastos), start=Decimal("0"))


def main() -> None:
    gastos = cargar_gastos()
    print("Control de gastos personales")
    print(f"Cargados {len(gastos)} gastos existentes.\n")
    print("Ingresa una descripción vacía para terminar.\n")

    while True:
        descripcion = input("Descripción del gasto: ").strip()
        if not descripcion:
            break

        print(f"Categorías disponibles: {', '.join(CATEGORIAS)}")
        categoria = input("Categoría: ").strip()

        try:
            monto = convertir_monto(input("Monto: "))
            agregar_gasto(gastos, descripcion, monto, categoria)
        except ValueError as error:
            print(f"Error: {error}\n")
            continue

        print("Gasto registrado.\n")

    if gastos:
        print("\nGastos registrados:")
        for gasto in gastos:
            print(f"- {gasto.descripcion}: ${gasto.monto:.2f} | {gasto.fecha} | {gasto.categoria}")
    else:
        print("\nNo se registraron gastos.")

    print(f"Total: ${calcular_total(gastos):.2f}")

    guardar = input("\n¿Deseas guardar los gastos? (s/n): ").strip().lower()
    if guardar == "s":
        guardar_gastos(gastos)
        print("Gastos guardados en 'gastos.json'.")


if __name__ == "__main__":
    main()
