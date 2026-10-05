"""Salva uma foto de uma webcam USB no Raspberry Pi."""

import cv2


def main():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError('Nao foi possivel abrir /dev/video0. Confira a webcam USB.')
    try:
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # Alguns modelos precisam de alguns quadros para ajustar a exposicao.
        quadro = None
        for _ in range(10):
            ok, quadro_atual = camera.read()
            if ok:
                quadro = quadro_atual
        if quadro is None:
            raise RuntimeError('A camera abriu, mas nao forneceu imagem.')
        if not cv2.imwrite('camera_teste.jpg', quadro):
            raise RuntimeError('Nao foi possivel salvar camera_teste.jpg.')
        print('Foto salva em camera_teste.jpg')
    finally:
        camera.release()


if __name__ == '__main__':
    main()
