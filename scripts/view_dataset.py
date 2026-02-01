"""
Script para visualizar el dataset synthetic_alicia.jsonl
Muestra cada entrada input/output y espera Enter para continuar
"""

import json
import os

def view_dataset(filepath):
    """Lee y muestra el dataset línea por línea"""
    
    if not os.path.exists(filepath):
        print(f"Error: No se encuentra el archivo {filepath}")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total = len(lines)
    print(f"\n{'='*80}")
    print(f"Dataset: {os.path.basename(filepath)}")
    print(f"Total de ejemplos: {total}")
    print(f"{'='*80}\n")
    
    for i, line in enumerate(lines, 1):
        try:
            data = json.loads(line)
            
            # Limpiar la terminal (opcional)
            # os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"\n{'='*80}")
            print(f"Ejemplo {i}/{total}")
            print(f"{'='*80}")
            
            print(f"\n📝 INPUT:")
            print(f"{'-'*80}")
            print(data.get('input', 'N/A'))
            
            print(f"\n💬 OUTPUT:")
            print(f"{'-'*80}")
            print(data.get('output', 'N/A'))
            
            print(f"\n{'='*80}")
            
            if i < total:
                input("\nPresiona Enter para ver el siguiente ejemplo...")
            else:
                print("\n✅ Fin del dataset")
                
        except json.JSONDecodeError as e:
            print(f"Error al leer la línea {i}: {e}")
            continue

if __name__ == "__main__":
    # Ruta al dataset
    dataset_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        'synthetic_alicia.jsonl'
    )
    
    view_dataset(dataset_path)
