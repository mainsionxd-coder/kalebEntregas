"""Prueba local de carga sobre el endpoint /health."""

import concurrent.futures
import sys
import time
import urllib.request


def medir_solicitud(url: str) -> float:
    inicio = time.perf_counter()
    with urllib.request.urlopen(url, timeout=10) as respuesta:
        respuesta.read()
        if respuesta.status != 200:
            raise RuntimeError(f"Respuesta HTTP inesperada: {respuesta.status}")
    return (time.perf_counter() - inicio) * 1000


def main() -> None:
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000/health"

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        tiempos = list(executor.map(medir_solicitud, [url] * 50))

    print(f"URL: {url}")
    print("Solicitudes: 50")
    print(f"Tiempo promedio: {sum(tiempos) / len(tiempos):.2f} ms")
    print(f"Tiempo mínimo: {min(tiempos):.2f} ms")
    print(f"Tiempo máximo: {max(tiempos):.2f} ms")


if __name__ == "__main__":
    main()
