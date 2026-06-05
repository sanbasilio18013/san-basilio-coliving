import os
from PIL import Image

SRC_DIR = r"G:\Mi unidad\FOTOS SAN BASILIO"
DEST_DIR = r"C:\Users\mirro\.gemini\antigravity\scratch\san-basilio-coliving\images"

def rotate_and_crop_by_luminosity():
    plano_png_src = os.path.join(SRC_DIR, "PLANO.png")
    
    if os.path.exists(plano_png_src):
        with Image.open(plano_png_src) as img:
            # 1. Rotar 90 grados a la derecha (horario)
            img_rot = img.rotate(-90, expand=True)
            print(f"Tamaño rotado: {img_rot.size}")
            
            # Convertir a escala de grises para analizar luminosidad
            gray = img_rot.convert("L")
            
            # Buscaremos los píxeles oscuros (luminosidad < 240)
            width, height = img_rot.size
            pixels = gray.load()
            
            min_x, min_y = width, height
            max_x, max_y = 0, 0
            
            # Recorrer píxeles para encontrar el área de los trazos del plano
            for y in range(height):
                for x in range(width):
                    # Trazos oscuros del plano
                    if pixels[x, y] < 240:
                        if x < min_x: min_x = x
                        if y < min_y: min_y = y
                        if x > max_x: max_x = x
                        if y > max_y: max_y = y
            
            print(f"Caja delimitadora de trazos: ({min_x}, {min_y}) a ({max_x}, {max_y})")
            
            if max_x > min_x and max_y > min_y:
                # Añadir un margen agradable de 30px
                margin = 40
                left = max(0, min_x - margin)
                top = max(0, min_y - margin)
                right = min(width, max_x + margin)
                bottom = min(height, max_y + margin)
                
                # Recortar
                cropped_img = img_rot.crop((left, top, right, bottom))
                print(f"Tamaño después del recorte: {cropped_img.size}")
                
                # Asegurarnos de que el fondo sea blanco limpio o rellenarlo si tiene transparencia
                if cropped_img.mode in ("RGBA", "P"):
                    # Crear fondo blanco
                    bg = Image.new("RGB", cropped_img.size, (255, 255, 255))
                    bg.paste(cropped_img, mask=cropped_img.split()[3] if cropped_img.mode == "RGBA" else None)
                    final_img = bg
                else:
                    final_img = cropped_img
                
                # Guardar en JPEG y PNG
                final_img.save(os.path.join(DEST_DIR, "plano.jpg"), "JPEG", quality=95)
                final_img.save(os.path.join(DEST_DIR, "plano_distribucion.png"), "PNG", optimize=True)
                print("Recorte y rotación aplicados con éxito.")
            else:
                print("No se encontraron trazos oscuros para recortar.")
    else:
        print("No se encuentra PLANO.png original.")

if __name__ == "__main__":
    rotate_and_crop_by_luminosity()
