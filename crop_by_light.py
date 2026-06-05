import os
from PIL import Image

SRC_DIR = r"G:\Mi unidad\FOTOS SAN BASILIO"
DEST_DIR = r"C:\Users\mirro\.gemini\antigravity\scratch\san-basilio-coliving\images"

def crop_original_by_light():
    plano_png_src = os.path.join(SRC_DIR, "PLANO.png")
    
    if os.path.exists(plano_png_src):
        with Image.open(plano_png_src) as img:
            # Mantener la orientación vertical original (sin rotar)
            print(f"Tamaño original: {img.size}")
            
            # Convertir a escala de grises para analizar luminosidad
            gray = img.convert("L")
            width, height = img.size
            pixels = gray.load()
            
            min_x, min_y = width, height
            max_x, max_y = 0, 0
            
            # Buscar píxeles claros (luminosidad > 200)
            for y in range(height):
                for x in range(width):
                    if pixels[x, y] > 200:
                        if x < min_x: min_x = x
                        if y < min_y: min_y = y
                        if x > max_x: max_x = x
                        if y > max_y: max_y = y
            
            print(f"Caja delimitadora de fondo claro: ({min_x}, {min_y}) a ({max_x}, {max_y})")
            
            if max_x > min_x and max_y > min_y:
                # Añadir un margen agradable de 20px
                margin = 25
                left = max(0, min_x - margin)
                top = max(0, min_y - margin)
                right = min(width, max_x + margin)
                bottom = min(height, max_y + margin)
                
                # Recortar
                cropped_img = img.crop((left, top, right, bottom))
                print(f"Tamaño después del recorte claro: {cropped_img.size}")
                
                # Convertir a RGB para guardar en JPEG (para evitar KeyError RGBA)
                if cropped_img.mode in ("RGBA", "P"):
                    # Crear fondo blanco para rellenar transparencias
                    bg = Image.new("RGB", cropped_img.size, (255, 255, 255))
                    bg.paste(cropped_img, mask=cropped_img.split()[3] if cropped_img.mode == "RGBA" else None)
                    final_img = bg
                else:
                    final_img = cropped_img.convert("RGB")
                
                # Guardar en JPEG y PNG
                final_img.save(os.path.join(DEST_DIR, "plano.jpg"), "JPEG", quality=95)
                final_img.save(os.path.join(DEST_DIR, "plano_distribucion.png"), "PNG", optimize=True)
                print("Recorte vertical original aplicado y guardado con éxito.")
            else:
                print("No se encontraron píxeles claros.")
    else:
        print("No se encuentra PLANO.png original.")

if __name__ == "__main__":
    crop_original_by_light()
