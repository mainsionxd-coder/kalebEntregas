"""Aplicación web de control de gastos personales."""

from flask import Flask, jsonify, render_template, request

from control_gastos import (
    CATEGORIAS,
    Gasto,
    agregar_gasto,
    calcular_total,
    convertir_monto,
)

APP_VERSION = "1.2.0"

app = Flask(__name__)
gastos_registrados: list[Gasto] = []


@app.after_request
def configurar_respuesta(response):
    """Añade cabeceras de seguridad ligera y registra cada petición."""
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    print(
        f"{request.method} {request.path} -> {response.status_code}",
        flush=True,
    )
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    descripcion = ""
    monto = ""
    status_code = 200

    if request.method == "POST":
        descripcion = request.form.get("descripcion", "")
        monto = request.form.get("monto", "").strip()
        categoria = request.form.get("categoria", "").strip() or "Otros"

        try:
            monto_decimal = convertir_monto(monto)
            agregar_gasto(
                gastos_registrados,
                descripcion,
                monto_decimal,
                categoria,
            )
        except ValueError as error_detectado:
            error = str(error_detectado)
            status_code = 400

    return (
        render_template(
            "index.html",
            version=APP_VERSION,
            gastos=gastos_registrados,
            gastos_count=len(gastos_registrados),
            total=calcular_total(gastos_registrados),
            categorias=CATEGORIAS,
            error=error,
            descripcion=descripcion,
            monto=monto,
        ),
        status_code,
    )


@app.route("/limpiar", methods=["POST"])
def limpiar():
    gastos_registrados.clear()
    return render_template(
        "index.html",
        version=APP_VERSION,
        gastos=gastos_registrados,
        gastos_count=len(gastos_registrados),
        total=calcular_total(gastos_registrados),
        categorias=CATEGORIAS,
        error=None,
        descripcion="",
        monto="",
        mensaje="Lista de gastos reiniciada.",
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "version": APP_VERSION,
            "gastos_count": len(gastos_registrados),
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
