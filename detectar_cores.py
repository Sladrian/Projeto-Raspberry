"""Protótipo de detecção de cores com Picamera2, sem acionar os servos.

As faixas de HSV são apenas um ponto de partida; calibre com as peças reais.
"""

import colorsys
import time
from collections import Counter

from picamera2 import Picamera2


LARGURA = 320
ALTURA = 240
PASSO_AMOSTRA = 8
SATURACAO_MINIMA = 0.35
BRILHO_MINIMO = 0.20
FRACAO_MINIMA = 0.10
QUADROS_ESTAVEIS = 3


def classificar_pixel(b: int, g: int, r: int) -> str | None:
    matiz, saturacao, brilho = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    if saturacao < SATURACAO_MINIMA or brilho < BRILHO_MINIMO:
        return None
    graus = matiz * 360
    if graus < 15 or graus >= 345:
        return "vermelho"
    if 75 <= graus <= 170:
        return "verde"
    if 190 <= graus <= 260:
        return "azul"
    return None


def detectar_cor(quadro) -> tuple[str | None, dict[str, float]]:
    """Analisa a área central; RGB888 do Picamera2 chega em ordem B, G, R."""
    altura, largura = quadro.shape[:2]
    x1, x2 = largura // 4, 3 * largura // 4
    y1, y2 = altura // 4, 3 * altura // 4
    contagem: Counter[str] = Counter()
    total = 0

    for y in range(y1, y2, PASSO_AMOSTRA):
        for x in range(x1, x2, PASSO_AMOSTRA):
            b, g, r = (int(c) for c in quadro[y, x, :3])
            cor = classificar_pixel(b, g, r)
            if cor:
                contagem[cor] += 1
            total += 1

    proporcoes = {cor: contagem[cor] / total for cor in ("azul", "verde", "vermelho")}
    cor, fracao = max(proporcoes.items(), key=lambda item: item[1])
    return (cor if fracao >= FRACAO_MINIMA else None), proporcoes


def main() -> None:
    camera = Picamera2()
    try:
        camera.configure(camera.create_preview_configuration(
            main={"size": (LARGURA, ALTURA), "format": "RGB888"}
        ))
        camera.start()
        time.sleep(2)
        ultima_amostra = None
        repeticoes = 0
        armado = True

        print("Detectando azul, verde e vermelho. Ctrl+C para encerrar.")
        while True:
            cor, proporcoes = detectar_cor(camera.capture_array())
            repeticoes = repeticoes + 1 if cor == ultima_amostra else 1
            ultima_amostra = cor

            if repeticoes >= QUADROS_ESTAVEIS:
                if cor is None:
                    armado = True
                elif armado:
                    print(f"Item: {cor} | cobertura: {proporcoes[cor]:.0%}", flush=True)
                    armado = False
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nEncerrado.")
    finally:
        camera.stop()
        camera.close()


if __name__ == "__main__":
    main()
