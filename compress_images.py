import os
import shutil
import unicodedata
from PIL import Image, ImageOps

# Rutas de origen y destino
SRC_DIR = r"G:\Mi unidad\_SAN BASILIO"
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

def normalize_string(s):
    # Eliminar acentos y poner en minúsculas para comparaciones seguras
    return "".join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()

def process_photos():
    print("Iniciando procesamiento de fotos de San Basilio...")
    
    if not os.path.exists(SRC_DIR):
        print(f"Error: El directorio de origen {SRC_DIR} no existe.")
        return
        
    # 1. Planos (PLANO.png y PLANO2.jpg en la raíz)
    planos = ["PLANO.png", "PLANO2.jpg"]
    for plano in planos:
        plano_src = os.path.join(SRC_DIR, plano)
        if os.path.exists(plano_src):
            dest_name = "plano.jpg" if plano == "PLANO2.jpg" else "plano_distribucion.png"
            if plano.lower().endswith('.png'):
                with Image.open(plano_src) as img:
                    img.save(os.path.join(DEST_DIR, dest_name), "PNG", optimize=True)
                print(f"Procesado plano PNG: {dest_name}")
            else:
                compress_image(plano_src, dest_name, max_width=1600, quality=85)
                print(f"Procesado plano JPG: {dest_name}")

    # Encontrar las carpetas reales en el origen
    src_items = os.listdir(SRC_DIR)
    
    # 2. Procesar Habitaciones (1, 2, 3, 4)
    for room_num in [1, 2, 3, 4]:
        # Buscar una carpeta que contenga "habitacion" y el número de habitación
        target_folder = None
        for item in src_items:
            item_path = os.path.join(SRC_DIR, item)
            if os.path.isdir(item_path):
                normalized_name = normalize_string(item)
                if "habitacion" in normalized_name and str(room_num) in normalized_name:
                    target_folder = item_path
                    break
        
        if target_folder:
            print(f"\nProcesando fotos de Habitación {room_num} desde: {os.path.basename(target_folder)}...")
            files = [f for f in os.listdir(target_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            files = [f for f in files if not f.startswith('RESIZE_')]
            files.sort()
            
            for idx, filename in enumerate(files):
                src_path = os.path.join(target_folder, filename)
                dest_name = f"hab{room_num}_{idx+1}.jpg"
                compress_image(src_path, dest_name, quality=80)
        else:
            print(f"\nAdvertencia: No se encontró la carpeta para la Habitación {room_num}")

    # 3. Procesar Cocina y Baño (Zonas comunes)
    target_comunes = None
    for item in src_items:
        item_path = os.path.join(SRC_DIR, item)
        if os.path.isdir(item_path):
            normalized_name = normalize_string(item)
            if "cocina" in normalized_name or "comun" in normalized_name or "bano" in normalized_name:
                target_comunes = item_path
                break
                
    if target_comunes:
        print(f"\nProcesando fotos de Zonas Comunes desde: {os.path.basename(target_comunes)}...")
        files = [f for f in os.listdir(target_comunes) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        files.sort()
        
        processed_count = 0
        for idx, filename in enumerate(files):
            src_path = os.path.join(target_comunes, filename)
            dest_name = f"comun_{processed_count+1}.jpg"
            res = compress_image(src_path, dest_name, quality=80)
            if res:
                processed_count += 1
    else:
        print("\nAdvertencia: No se encontró la carpeta para Zonas Comunes")

    print("\n¡Procesamiento completado con éxito!")

if __name__ == "__main__":
    setup_directories()
    process_photos()
