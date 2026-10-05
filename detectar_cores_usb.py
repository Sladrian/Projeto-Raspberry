"""Deteccao inicial de azul, verde e vermelho com webcam USB.

Compativel com a sintaxe do Python 3.5 do Raspbian Stretch. Nao aciona servos.
"""

import colorsys
import time
from collections import Counter

import cv2


PASSO_AMOSTRA = 8
SATURACAO_MINIMA = 0.35
BRILHO_MINIMO = 0.20
FRACAO_MINIMA = 0.10
QUADROS_ESTAVEIS = 3


def classificar_pixel(b, g, r):
    matiz, saturacao, brilho = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    if saturacao < SATURACAO_MINIMA or brilho < BRILHO_MINIMO:
        return None
    graus = matiz * 360
    if graus < 15 or graus >= 345:
        return 'vermelho'
    if 75 <= graus <= 170:
        return 'verde'
    if 190 <= graus <= 260:
        return 'azul'
    return None


def detectar_cor(quadro):
    altura, largura = quadro.shape[:2]
    contagem = Counter()
    total = 0
    for y in range(altura // 4, 3 * altura // 4, PASSO_AMOSTRA):
        for x in range(largura // 4, 3 * largura // 4, PASSO_AMOSTRA):
            b, g, r = (int(valor) for valor in quadro[y, x, :3])
            cor = classificar_pixel(b, g, r)
            if cor:
                contagem[cor] += 1
            total += 1
    proporcoes = {cor: contagem[cor] / float(total)
                  for cor in ('azul', 'verde', 'vermelho')}
    cor = max(proporcoes, key=proporcoes.get)
    return (cor if proporcoes[cor] >= FRACAO_MINIMA else None), proporcoes


def main():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError('Nao foi possivel abrir /dev/video0. Confira a webcam USB.')
    try:
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        ultima_amostra = None
        repeticoes = 0
        armado = True
        print('Detectando azul, verde e vermelho. Ctrl+C para encerrar.')
        while True:
            ok, quadro = camera.read()
            if not ok:
                raise RuntimeError('A camera parou de fornecer imagens.')
            cor, proporcoes = detectar_cor(quadro)
            repeticoes = repeticoes + 1 if cor == ultima_amostra else 1
            ultima_amostra = cor
            if repeticoes >= QUADROS_ESTAVEIS:
                if cor is None:
                    armado = True
                elif armado:
                    print('Item: {} | cobertura: {:.0%}'.format(
                        cor, proporcoes[cor]), flush=True)
                    armado = False
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('\nEncerrado.')
    finally:
        camera.release()


if __name__ == '__main__':
    main()
