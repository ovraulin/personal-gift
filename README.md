# mascota

Mascota virtual para ESP32-S3 (MicroPython). Grafica una cara minimalista en
una pantalla ST7789 usando [este driver](https://github.com/halherta/st7789_lcd_driver_micropython).

- `src/mascota/state.py`: modelo de estado (hambre/energía/afecto/mood). Python
  puro, sin dependencias de hardware.
- `src/mascota/face.py`: dibuja una cara minimalista según el `mood`, sobre
  cualquier objeto que implemente `fill`/`fill_rect`/`line` (el mismo subset
  que expone el driver real). También Python puro, testeable en la compu.
- `device/`: código que solo corre en el ESP32-S3.
  - `st7789py.py`: driver vendorizado de
    [halherta/st7789_lcd_driver_micropython](https://github.com/halherta/st7789_lcd_driver_micropython)
    (sin LICENSE en el repo original; vendorizado para uso personal).
  - `main.py`: entry point que arma la pantalla (pines de la Waveshare
    ESP32-S3-LCD-1.47), instancia la mascota y la va redibujando.

Todo lo de `src/mascota/` se testea y lintea en la compu con `uv`/`ruff`/
`pytest`. Lo de `device/` no se testea en la compu (depende de `machine`,
`micropython`, etc.) — se prueba corriéndolo en el ESP32.

## Desarrollo

```bash
uv sync          # instala dependencias de dev
make format      # formatea y arregla lint automáticamente
make check       # formato + lint + tests (lo mismo que corre en CI)
```

## Deploy al device

Copiar al filesystem del ESP32-S3 (por ejemplo con `mpremote cp`):
`device/main.py`, `device/st7789py.py` y la carpeta `src/mascota/`.
