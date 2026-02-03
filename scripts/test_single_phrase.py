import requests
import json

# Configuración
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:0.6b"

def test_base_model(frase):
    """
    Prueba el modelo base con diferentes formatos de prompt
    """
    
    print("=" * 80)
    print(f"📝 Frase original: {frase}")
    print("=" * 80)
    
    # Probar diferentes formatos de prompt
    prompts = [
        # Prompt 1: Muy simple
        f"Reescribe esta frase con estilo fantasioso: {frase}",
        
        # Prompt 2: Con contexto
        f"Eres un escritor que escribe como Lewis Carroll. Reescribe: {frase}",
        
        # Prompt 3: Chat format
        f"User: Reescribe este texto con el estilo de Alicia en el País de las Maravillas: {frase}\nAssistant:",
        
        # Prompt 4: Formato instrucción (original)
        f"""### Instrucción:
Reescribe el siguiente texto con el estilo de Alicia en el País de las Maravillas.

### Entrada:
{frase}

### Respuesta:
"""
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{'='*80}")
        print(f"🧪 PRUEBA {i} - Formato de prompt {i}")
        print(f"{'='*80}")
        print(f"Prompt usado:\n{prompt[:100]}...")
        print("\n⏳ Generando...\n")
        
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "top_k": 40,
                "num_predict": 150
            }
        }
        
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            respuesta = result.get('response', '').strip()
            
            if respuesta:
                print("✅ RESPUESTA:")
                print("-" * 80)
                print(respuesta)
                print("-" * 80)
            else:
                print("⚠️ Respuesta vacía")
                print(f"Debug: {result}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()


if __name__ == "__main__":
    # Frase de prueba
    frase = "Era una tarde soleada y los niños jugaban en el parque"
    
    print("\n🧪 PRUEBA DEL MODELO BASE - MÚLTIPLES FORMATOS")
    print(f"🤖 Modelo: {MODEL_NAME}")
    print("=" * 80)
    
    # Verificar conexión
    try:
        response = requests.get("http://localhost:11434/api/tags")
        models = response.json().get('models', [])
        model_names = [m['name'] for m in models]
        print(f"✅ Ollama corriendo. Modelos disponibles: {model_names}\n")
        
        if MODEL_NAME not in model_names:
            print(f"⚠️ Modelo '{MODEL_NAME}' no encontrado")
            print(f"💡 Prueba con: {model_names[0] if model_names else 'ollama pull qwen2.5:0.5b'}")
            MODEL_NAME = model_names[0] if model_names else MODEL_NAME
    except:
        print("❌ Ollama no está corriendo")
        print("💡 Ejecuta: ollama serve")
        exit(1)
    
    test_base_model(frase)
    
    print("\n✅ Pruebas completadas")