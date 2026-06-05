import os
from PIL import Image, ImageChops, ImageOps

SRC_DIR = r"G:\Mi unidad\FOTOS SAN BASILIO"
DEST_DIR = r"C:\Users\mirro\.gemini\antigravity\scratch\san-basilio-coliving\images"

def autocrop(image, background_color=(255, 255, 255)):
    # Convertir a RGB si es necesario
    if image.mode != "RGB":
        image = image.convert("RGB")
        
    bg = Image.new("RGB", image.size, background_color)
    diff = ImageChops.difference(image, bg)
    diff = ImageOps.grayscale(diff)
    
    # Bounding box del contenido
    bbox = diff.getbbox()
    if bbox:
        # Añadir un pequeño margen de 20px alrededor del plano para que no quede pegado al borde
        margin = 30
        left = max(0, bbox[0] - margin)
        top = max(0, bbox[1] - margin)
        right = min(image.width, bbox[2] + margin)
        bottom = min(image.height, bbox[3] + margin)
        return image.crop((left, top, right, bottom))
    return image

def rotate_and_crop():
    plano_png_src = os.path.join(SRC_DIR, "PLANO.png")
    
    if os.path.exists(plano_png_src):
        with Image.open(plano_png_src) as img:
            # 1. Rotar 90 grados horario (a la derecha)
            img_rot = img.rotate(-90, expand=True)
            print(f"Dimensiones después de rotar: {img_rot.size}")
            
            # 2. Recortar los márgenes blancos
            img_cropped = autocrop(img_rot)
            print(f"Dimensiones después del recorte: {img_cropped.size}")
            
            # 3. Guardar como PNG y JPG
            img_cropped.save(os.path.join(DEST_DIR, "plano_distribucion.png"), "PNG", optimize=True)
            img_cropped.save(os.path.join(DEST_DIR, "plano.jpg"), "JPEG", quality=95)
            print("Guardados plano.jpg y plano_distribucion.png recortados y en vertical.")
    else:
        print("No se encuentra PLANO.png original.")

if __name__ == "__main__":
    rotate_and_crop()
