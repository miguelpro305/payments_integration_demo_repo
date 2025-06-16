import os
import re

ROOT_DIR = './'  # Puedes cambiarlo por tu carpeta raíz, por ejemplo 'app/'

def convertir_anotaciones(path):
    for dirpath, _, filenames in os.walk(path):
        for file in filenames:
            if file.endswith('.py'):
                full_path = os.path.join(dirpath, file)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Reemplazar 'Optional[tipo]' por 'Optional[tipo]'
                nuevo_contenido = re.sub(r'(\w+)\s*\|\s*None', r'Optional[\1]', content)

                # Si hubo cambios, agregar import si es necesario y sobrescribir el archivo
                if nuevo_contenido != content:
                    if 'Optional' in nuevo_contenido and 'from typing import Optional' not in nuevo_contenido:
                        nuevo_contenido = 'from typing import Optional\n' + nuevo_contenido
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(nuevo_contenido)
                    print(f"✅ Modificado: {full_path}")

if __name__ == "__main__":
    convertir_anotaciones(ROOT_DIR)
