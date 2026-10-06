"""Captura uma foto de uma webcam USB com fswebcam no Raspbian Stretch."""

import subprocess


DISPOSITIVO = '/dev/video0'


def capturar_foto(caminho, resolucao='640x480', silencioso=False):
    comando = ['fswebcam', '-d', DISPOSITIVO, '-r', resolucao,
               '-S', '5', '--no-banner', caminho]
    if silencioso:
        comando.insert(1, '-q')
    subprocess.check_call(comando)


def main():
    capturar_foto('camera_teste.jpg')
    print('Foto salva em camera_teste.jpg')


if __name__ == '__main__':
    main()
