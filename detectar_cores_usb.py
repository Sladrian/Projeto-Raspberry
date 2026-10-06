"""Deteccao inicial de azul, verde e vermelho com webcam USB.

Compativel com a sintaxe do Python 3.5 do Raspbian Stretch. Nao aciona servos.
"""

import colorsys
from collections import Counter

from PIL import Image

from camera_teste_usb import capturar_foto


PASSO_AMOSTRA = 8
SATURACAO_MINIMA = 0.35
BRILHO_MINIMO = 0.20
FRACAO_MINIMA = 0.10
QUADROS_ESTAVEIS = 3
FOTO_ATUAL = 'camera_ultima.jpg'


def classificar_pixel(r, g, b):
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


def detectar_cor(imagem):
    largura, altura = imagem.size
    pixels = imagem.load()
    contagem = Counter()
    total = 0
    for y in range(altura // 4, 3 * altura // 4, PASSO_AMOSTRA):
        for x in range(largura // 4, 3 * largura // 4, PASSO_AMOSTRA):
            cor = classificar_pixel(*pixels[x, y])
            if cor:
                contagem[cor] += 1
            total += 1
    proporcoes = {cor: contagem[cor] / float(total)
                  for cor in ('azul', 'verde', 'vermelho')}
    cor = max(proporcoes, key=proporcoes.get)
    return (cor if proporcoes[cor] >= FRACAO_MINIMA else None), proporcoes


def main():
    ultima_amostra = None
    repeticoes = 0
    armado = True
    print('Detectando azul, verde e vermelho. Ctrl+C para encerrar.', flush=True)
    print('Cada captura atualiza {} para conferir o enquadramento.'.format(
        FOTO_ATUAL), flush=True)
    try:
        while True:
            capturar_foto(FOTO_ATUAL, '320x240', silencioso=True)
            with Image.open(FOTO_ATUAL) as foto:
                imagem = foto.convert('RGB')
            cor, proporcoes = detectar_cor(imagem)
            repeticoes = repeticoes + 1 if cor == ultima_amostra else 1
            ultima_amostra = cor
            print('Amostra: vermelho {:.0%} | verde {:.0%} | azul {:.0%} | '
                  'candidato: {} ({}/{})'.format(
                      proporcoes['vermelho'], proporcoes['verde'],
                      proporcoes['azul'], cor or 'nenhum',
                      min(repeticoes, QUADROS_ESTAVEIS), QUADROS_ESTAVEIS),
                  flush=True)
            if repeticoes >= QUADROS_ESTAVEIS:
                if cor is None:
                    armado = True
                elif armado:
                    print('Item: {} | cobertura: {:.0%}'.format(
                        cor, proporcoes[cor]), flush=True)
                    armado = False
    except KeyboardInterrupt:
        print('\nEncerrado.')


if __name__ == '__main__':
    main()
