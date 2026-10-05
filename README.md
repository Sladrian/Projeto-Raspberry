# Esteira separadora por cores — primeira etapa

## Se você usa Raspbian 9 (Stretch) e webcam USB

O Raspberry Pi 3 deste projeto está com Raspbian 9 (Stretch), arquitetura
armhf. Durante o primeiro teste, será usada uma webcam USB. **Use os arquivos
com `_usb` no nome.** Os scripts sem esse sufixo usam a câmera CSI e Picamera2,
que exige Raspberry Pi OS Bullseye ou mais recente.

Primeiro verifique se a webcam aparece e se o OpenCV já está instalado:

```bash
ls /dev/video*
python3 -c 'import cv2; print(cv2.__version__)'
```

Se aparecer `/dev/video0` e o import funcionar, rode um teste que não aciona motores:

```bash
python3 camera_teste_usb.py
```

Confira a foto `camera_teste.jpg`. Só depois teste a detecção:

```bash
python3 detectar_cores_usb.py
```

Se a webcam estiver em `/dev/video1`, troque `cv2.VideoCapture(0)` por
`cv2.VideoCapture(1)` nos dois scripts. Se o import de `cv2` falhar ou a câmera
não capturar, anote o erro exato antes de instalar ou mudar qualquer pacote.

## Se você usa Raspberry Pi OS Bullseye ou mais recente

Protótipo para **Raspberry Pi 3 com câmera CSI**. Primeiro testa a câmera e
depois reconhece peças azuis, verdes e vermelhas. **Ainda não aciona servos**:
o destino de cada cor, os pinos e o tempo entre câmera e desvio precisam ser
definidos e medidos na esteira real.

## Preparação

Estes scripts usam Picamera2, compatível com Raspberry Pi OS Bullseye ou mais
recente com a pilha de câmera libcamera. Confira a versão instalada:

```bash
cat /etc/os-release
```

Se `python3 -c 'import picamera2'` falhar, instale pelo gerenciador de pacotes
do Raspberry Pi OS (evite misturar com instalações de `pip`):

```bash
sudo apt update
sudo apt install python3-picamera2 --no-install-recommends
```

Se o sistema for anterior ao Bullseye ou estiver no modo de câmera legado,
verifique isso antes de tentar executar os scripts; será necessário adaptar a
captura de imagens.

## Teste

Com a câmera conectada e o Raspberry ligado:

```bash
python3 camera_teste.py
```

Abra `camera_teste.jpg` e confira se a esteira está enquadrada e iluminada.
Depois rode:

```bash
python3 detectar_cores.py
```

Passe uma peça por vez pelo centro da imagem. O terminal imprime a cor quando
ela aparece em três quadros consecutivos; espera a área ficar sem cor por três
quadros antes de registrar outra peça. Ctrl+C encerra a leitura.

## Calibração

- Use iluminação estável e fundo neutro, de preferência sem azul, verde ou vermelho.
- O código analisa a região central da imagem e amostra um pixel a cada oito.
- Ajuste os limites de matiz, saturação e brilho em `classificar_pixel` e a
  `FRACAO_MINIMA` conforme o material e a iluminação reais.
- Este detector simples não separa duas peças juntas, nem calcula o tempo de
  chegada aos servos. Essas etapas vêm depois dos primeiros testes de câmera.
