"""Salva uma foto para verificar se a câmera CSI funciona."""

import time
from pathlib import Path

from picamera2 import Picamera2


def main() -> None:
    camera = Picamera2()
    try:
        camera.configure(camera.create_still_configuration(main={"size": (640, 480)}))
        camera.start()
        time.sleep(2)  # Aguarda a exposição automática estabilizar.
        destino = Path("camera_teste.jpg")
        camera.capture_file(str(destino))
        print(f"Foto salva em {destino.resolve()}")
    finally:
        camera.stop()
        camera.close()


if __name__ == "__main__":
    main()
