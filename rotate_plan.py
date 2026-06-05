import os
from PIL import Image

SRC_DIR = r"G:\Mi unidad\FOTOS SAN BASILIO"
DEST_DIR = r"C:\Users\mirro\.gemini\antigravity\scratch\san-basilio-coliving\images"

def rotate():
    plano_png_src = os.path.join(SRC_DIR, "PLANO.png")
    
    if os.path.exists(plano_png_src):
        with Image.open(plano_png_src) as img:
            # Rotar 90 grados a la derecha (horario)
            img_rot = img.rotate(-90, expand=True)
            
            # Guardar como PNG
            img_rot.save(os.path.join(DEST_DIR, "plano_distribucion.png"), "PNG", optimize=True)
            print("Guardado plano_distribucion.png rotado 90 grados horario.")
            
            # Convertir a RGB y guardar como plano.jpg
            if img_rot.mode in ("RGBA", "P"):
                img_rot_rgb = img_rot.convert("RGB")
            else:
                img_rot_rgb = img_rot
            
            img_rot_rgb.save(os.path.join(DEST_DIR, "plano.jpg"), "JPEG", quality=95)
            print("Guardado plano.jpg rotado 90 grados horario.")
    else:
        print("No se encuentra el archivo PLANO.png original.")

if __name__ == "__main__":
    rotate()
