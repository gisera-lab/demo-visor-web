import os
from PIL import Image, ExifTags

# ============================================
# CONFIGURACIÓN (Rutas a tus carpetas principales)
# ============================================
carpeta_antes   = r"C:\Users\irmaf\Downloads\Fotos_antes"
carpeta_despues = r"C:\Users\irmaf\Downloads\Fotos_despues"

# Dimensiones FIJAS estandarizadas para el pop-up (Proporción 4:3 limpia)
ancho_fijo      = 800  
alto_fijo       = 600  
calidad_webp    = 75    
# ============================================

def corregir_orientacion(img):
    """Detecta la orientación nativa del celular y rota la imagen si es necesario."""
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = img._getexif()
        if exif and orientation in exif:
            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
    except:
        pass
    return img

def redimensionar_y_recortar_centro(img, ancho_destino, alto_destino):
    """
    Cambia el tamaño manteniendo la proporción y recorta el centro 
    para asegurar que todas las fotos tengan EXACTAMENTE la misma dimensión.
    """
    proporcion_w = ancho_destino / img.width
    proporcion_h = alto_destino  / img.height
    proporcion   = max(proporcion_w, proporcion_h)

    # Redimensionar conservando proporción para no deformar
    nuevo_ancho = int(img.width  * proporcion)
    nuevo_alto  = int(img.height * proporcion)
    img = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)

    # Recortar al centro exacto para estandarizar el tamaño visual
    left = (nuevo_ancho - ancho_destino) // 2
    top  = (nuevo_alto  - alto_destino)  // 2
    img  = img.crop((left, top, left + ancho_destino, top + alto_destino))

    return img

def optimizar_visor_por_lotes(carpeta_raiz):
    print(f"\n📁 Iniciando Optimización Masiva WebP en: {carpeta_raiz}\n")
    
    if not os.path.exists(carpeta_raiz):
        print(f"❌ La carpeta raíz no existe: {carpeta_raiz}")
        return

    # os.walk recorre automáticamente la carpeta raíz y todas sus subcarpetas de lotes
    for root, dirs, files in os.walk(carpeta_raiz):
        # Mostramos qué lote se está optimizando en el momento
        if files:
            nombre_lote = os.path.basename(root)
            print(f"📦 Optimizando imágenes del {nombre_lote}...")

        for archivo in files:
            if not archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
                
            ruta_origen = os.path.join(root, archivo)
            nombre_base, _ = os.path.splitext(archivo)
            ruta_destino = os.path.join(root, f"{nombre_base}.webp")
            
            try:
                img = Image.open(ruta_origen)
                peso_antes = os.path.getsize(ruta_origen) / 1024
                
                # Tu procesamiento digital original
                img = corregir_orientacion(img)
                img = redimensionar_y_recortar_centro(img, ancho_fijo, alto_fijo)
                
                # Guardar en WebP ultraligero para GitHub
                img.save(ruta_destino, "WEBP", quality=calidad_webp, method=6)
                
                peso_despues = os.path.getsize(ruta_destino) / 1024
                ahorro = (1 - peso_despues / peso_antes) * 100
                
                # Remover original para dejar limpio el lote de producción
                os.remove(ruta_origen)
                
                print(f"  ✅ {archivo} ➔ {nombre_base}.webp ({ahorro:.0f}% ahorro)")
                
            except Exception as e:
                print(f"  ❌ Error al procesar {archivo}: {e}")
        print()

# Ejecución del optimizador dinámico por lotes
optimizar_visor_por_lotes(carpeta_antes)
optimizar_visor_por_lotes(carpeta_despues)

print("🎉 ¡Fase de optimización completada! Todas las carpetas de lotes tienen imágenes WebP de 800x600px listas para la web.")
