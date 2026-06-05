import os
import shutil
from PIL import Image, ImageOps

# Rutas de origen y destino
SRC_DIR = r"G:\Mi unidad\FOTOS SAN BASILIO"
DEST_DIR = r"C:\Users\mirro\.gemini\antigravity\scratch\san-basilio-coliving\images"

# Desactivar límite de píxeles para fotos de ultra alta resolución (ej. 200MP)
Image.MAX_IMAGE_PIXELS = None

def setup_directories():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        print(f"Creado directorio de destino: {DEST_DIR}")

def compress_image(src_path, dest_filename, max_width=1200, quality=80):
    try:
        dest_path = os.path.join(DEST_DIR, dest_filename)
        
        # Abrir imagen
        with Image.open(src_path) as img:
            # Corregir orientación basada en metadatos EXIF (rotación de móviles)
            img = ImageOps.exif_transpose(img)
            
            # Convertir a RGB si está en RGBA (para poder guardarla como JPEG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
                
            # Calcular nuevas dimensiones manteniendo la proporción
            w, h = img.size
            if w > max_width:
                ratio = max_width / float(w)
                new_h = int(float(h) * ratio)
                img = img.resize((max_width, new_h), Image.Resampling.LANCZOS)
                print(f"  Redimensionada {os.path.basename(src_path)} de {w}x{h} a {max_width}x{new_h}")
            
            # Guardar con compresión y optimización
            img.save(dest_path, "JPEG", quality=quality, optimize=True)
            size_kb = os.path.getsize(dest_path) / 1024.0
            print(f"  Guardada: {dest_filename} ({size_kb:.1f} KB)")
            return dest_path
    except Exception as e:
        print(f"Error procesando {src_path}: {e}")
        return None

def process_photos():
    print("Iniciando procesamiento de fotos de San Basilio...")
    
    # 1. Planos (PLANO.png y PLANO2.jpg en la raíz)
    planos = ["PLANO.png", "PLANO2.jpg"]
    for plano in planos:
        plano_src = os.path.join(SRC_DIR, plano)
        if os.path.exists(plano_src):
            # Guardar plano principal optimizado
            dest_name = "plano.jpg" if plano == "PLANO2.jpg" else "plano_distribucion.png"
            if plano.lower().endswith('.png'):
                # Copiar y optimizar PNG
                with Image.open(plano_src) as img:
                    img.save(os.path.join(DEST_DIR, dest_name), "PNG", optimize=True)
                print(f"Procesado plano PNG: {dest_name}")
            else:
                # Comprimir plano JPG
                compress_image(plano_src, dest_name, max_width=1600, quality=85)
                print(f"Procesado plano JPG: {dest_name}")

    # 2. Procesar Habitación 2 (servirá para Hab 1, Hab 2 y Hab 3)
    hab2_src_dir = os.path.join(SRC_DIR, "Habitación 2")
    if os.path.exists(hab2_src_dir):
        print("\nProcesando fotos de Habitación 2...")
        files = [f for f in os.listdir(hab2_src_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        # Filtrar posibles archivos de resize temporales
        files = [f for f in files if not f.startswith('RESIZE_')]
        files.sort() # Ordenar para consistencia
        
        # Procesaremos TODAS las fotos para el carrusel de Habitación 2
        for idx, filename in enumerate(files):
            src_path = os.path.join(hab2_src_dir, filename)
            
            # Guardar como fotos de la Habitación 2
            dest_name_hab2 = f"hab2_{idx+1}.jpg"
            compress_image(src_path, dest_name_hab2, quality=80)
            
            # Mapear provisionalmente a la Habitación 1 y 3 (según instrucciones del usuario)
            dest_name_hab1 = f"hab1_{idx+1}.jpg"
            dest_name_hab3 = f"hab3_{idx+1}.jpg"
            shutil.copy(os.path.join(DEST_DIR, dest_name_hab2), os.path.join(DEST_DIR, dest_name_hab1))
            shutil.copy(os.path.join(DEST_DIR, dest_name_hab2), os.path.join(DEST_DIR, dest_name_hab3))
            print(f"  Copiada temporalmente a {dest_name_hab1} y {dest_name_hab3}")

    # 3. Procesar Habitación 4
    hab4_src_dir = os.path.join(SRC_DIR, "Habitación 4")
    if os.path.exists(hab4_src_dir):
        print("\nProcesando fotos de Habitación 4...")
        files = [f for f in os.listdir(hab4_src_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        files.sort()
        
        # Procesaremos TODAS las fotos para el carrusel de Habitación 4
        for idx, filename in enumerate(files):
            src_path = os.path.join(hab4_src_dir, filename)
            dest_name = f"hab4_{idx+1}.jpg"
            compress_image(src_path, dest_name, quality=80)

    # 4. Procesar Cocina y Baño (Zonas comunes)
    comunes_src_dir = os.path.join(SRC_DIR, "COCINA Y BAÑO")
    if os.path.exists(comunes_src_dir):
        print("\nProcesando fotos de Zonas Comunes...")
        files = [f for f in os.listdir(comunes_src_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        files.sort()
        
        # Procesaremos TODAS las fotos representativas para las zonas comunes
        processed_count = 0
        for idx, filename in enumerate(files):
            src_path = os.path.join(comunes_src_dir, filename)
            dest_name = f"comun_{processed_count+1}.jpg"
            res = compress_image(src_path, dest_name, quality=80)
            if res:
                processed_count += 1

    print("\n¡Procesamiento completado con éxito!")

if __name__ == "__main__":
    setup_directories()
    process_photos()
