# mascota

Mascota virtual para ESP32-S3 (MicroPython). Grafica una cara minimalista en
una pantalla ST7789 usando [este driver](https://github.com/halherta/st7789_lcd_driver_micropython).

En esta primera etapa solo existe el modelo de estado de la mascota
(`src/mascota/state.py`), en Python puro sin dependencias de hardware, para
poder testearlo y lintearlo en la compu. El código de pantalla/hardware se
agrega en una etapa siguiente.

## Desarrollo

```bash
uv sync          # instala dependencias de dev
make format      # formatea y arregla lint automáticamente
make check       # formato + lint + tests (lo mismo que corre en CI)
```
