import os
import re

# ============================================
# CONFIGURACIÓN
# ============================================
carpeta_antes   = r"C:\Users\irmaf\Downloads\Fotos_antes"
carpeta_despues = r"C:\Users\irmaf\Downloads\Fotos_despues"
proyecto        = "demo-visor"
# ============================================

def renombrar_por_lotes(carpeta_raiz, estado_prefijo):
    print(f"\n📁 Iniciando procesamiento en: {carpeta_raiz}\n")
    
    if not os.path.exists(carpeta_raiz):
        print(f"❌ La carpeta raíz no existe: {carpeta_raiz}")
        return

    # Listamos las subcarpetas (lote_1c, lote_da1, etc.)
    subcarpetas = [f for f in os.listdir(carpeta_raiz) if os.path.isdir(os.path.join(carpeta_raiz, f))]
    
    if not subcarpetas:
        print(f"⚠️ No se encontraron subcarpetas de lotes en {carpeta_raiz}.")
        return

    for lote_nombre in subcarpetas:
        ruta_lote = os.path.join(carpeta_raiz, lote_nombre)
        print(f"📦 Procesando {lote_nombre}...")
        
        archivos = os.listdir(ruta_lote)
        
        for nombre_original in archivos:
            if not nombre_original.lower().endswith(('.jpeg', '.jpg', '.png')):
                continue
                
            # EXPRESIÓN REGULAR PERFECTA:
            # ^(\d+) busca los dígitos justo al inicio (ej: 77)
            # e ignora el "de-" o "a-" y el resto del texto de WhatsApp
            coincidencia = re.match(r"^(\d+)", nombre_original)
            
            if coincidencia:
                id_numero = coincidencia.group(1) # Aquí guarda el 77, 24, etc.
                
                # Construimos el nombre con todo lo que me pediste:
                # [proyecto] _ [lote] _ [estado] _ [número de registro].jpg
                nombre_nuevo = f"{proyecto}_{lote_nombre}_{estado_prefijo}_{id_numero}.jpg"
                
                origen  = os.path.join(ruta_lote, nombre_original)
                destino = os.path.join(ruta_lote, nombre_nuevo)
                
                try:
                    os.rename(origen, destino)
                    print(f"  ✅ {nombre_original}")
                    print(f"    → {nombre_nuevo}\n")
                except Exception as e:
                    print(f"  ❌ Error en {nombre_original}: {e}\n")
            else:
                print(f"  ⚠️ No se encontró número de registro al inicio de: {nombre_original} (Saltado)\n")

# Ejecutamos el flujo para antes (inicio) y despues (termino)
renombrar_por_lotes(carpeta_antes, "inicio")
renombrar_por_lotes(carpeta_despues, "termino")

print("¡Proceso completado! Tus fotos ya tienen el lote, estado y su número de registro original.")
