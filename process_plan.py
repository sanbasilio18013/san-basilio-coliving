import os
from PIL import Image

SRC_DIR = r"G:\Mi unidad\FOTOS SAN BASILIO"
DEST_DIR = r"C:\Users\mirro\.gemini\antigravity\scratch\san-basilio-coliving\images"

def process():
    plano_png = os.path.join(SRC_DIR, "PLANO.png")
    plano_jpg_orig = os.path.join(SRC_DIR, "PLANO2.jpg")
    
    # 1. Guardar la versión PNG convertida a JPG como plano_png.jpg
    if os.path.exists(plano_png):
        with Image.open(plano_png) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            dest_path = os.path.join(DEST_DIR, "plano_png_ver.jpg")
            img.save(dest_path, "JPEG", quality=90)
            print(f"Guardado plano_png_ver.jpg desde PLANO.png con tamaño {img.size}")
            
    # 2. Guardar la versión de PLANO2.jpg rotada 90 grados a la derecha (horario)
    if os.path.exists(plano_jpg_orig):
        with Image.open(plano_jpg_orig) as img:
            # Rotar 90 grados horario
            img_rot_cw = img.rotate(-90, expand=True)
            img_rot_cw.save(os.path.join(DEST_DIR, "plano_rot_cw.jpg"), "JPEG", quality=90)
            print(f"Guardado plano_rot_cw.jpg (rotado 90 horario) con tamaño {img_rot_cw.size}")
            
            # Rotar 90 grados antihorario
            img_rot_ccw = img.rotate(90, expand=True)
            img_rot_ccw.save(os.path.join(DEST_DIR, "plano_rot_ccw.jpg"), "JPEG", quality=90)
            print(f"Guardado plano_rot_ccw.jpg (rotado 90 antihorario) con tamaño {img_rot_ccw.size}")

if __name__ == "__main__":
    process()
