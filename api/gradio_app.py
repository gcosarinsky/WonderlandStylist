import gradio as gr
import requests
import json

# Configuración de Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "alicia:latest"  # Cambia esto por el nombre de tu modelo en Ollama

def generar_respuesta(frase_input, temperatura, max_tokens):
    """
    Genera una respuesta usando el modelo de Ollama con streaming.
    El Modelfile ya incluye el template, así que solo enviamos el texto de entrada.
    """
    # Payload para Ollama - el prompt ya está definido en Modelfile.alicia
    payload = {
        "model": MODEL_NAME,
        "prompt": frase_input,  # Solo el texto de entrada
        "stream": True,  # Habilitamos streaming
        "options": {
            "temperature": temperatura,
            "num_predict": max_tokens
        }
    }
    
    try:
        # Llamada a Ollama con streaming
        response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60)
        response.raise_for_status()
        
        respuesta_completa = ""
        
        # Procesar el stream línea por línea
        for line in response.iter_lines():
            if line:
                try:
                    # Cada línea es un JSON con un fragmento de la respuesta
                    chunk = json.loads(line.decode('utf-8'))
                    token = chunk.get('response', '')
                    respuesta_completa += token
                    
                    # Yield para actualizar la UI en tiempo real
                    yield respuesta_completa
                    
                    # Si done es True, terminamos
                    if chunk.get('done', False):
                        break
                        
                except json.JSONDecodeError:
                    continue
        
        if not respuesta_completa:
            yield "⚠️ El modelo no generó ninguna respuesta"
        
    except requests.exceptions.ConnectionError:
        yield "❌ Error: No se pudo conectar con Ollama. Asegúrate de que está corriendo (ollama serve)"
    except requests.exceptions.Timeout:
        yield "⏱️ Error: La solicitud tardó demasiado tiempo"
    except Exception as e:
        yield f"❌ Error inesperado: {str(e)}"

def verificar_modelo():
    """
    Verifica que el modelo esté disponible en Ollama
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = response.json().get('models', [])
        model_names = [m['name'] for m in models]
        
        if MODEL_NAME in model_names:
            return f"✅ Modelo '{MODEL_NAME}' disponible"
        else:
            return f"⚠️ Modelo '{MODEL_NAME}' no encontrado. Modelos disponibles: {', '.join(model_names)}"
    except:
        return "❌ Ollama no está corriendo. Ejecuta: ollama serve"



# Crear la interfaz de Gradio
with gr.Blocks(title="Wonderland Stylist 🎩🐰", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🎩 Wonderland Stylist 🐰
        ### Transforma tu texto al estilo de *Alicia en el País de las Maravillas*
        
        Escribe una frase simple y el modelo la reescribirá con el estilo fantasioso de Lewis Carroll.
        """
    )
    
    # Estado del modelo
    with gr.Row():
        estado_modelo = gr.Textbox(
            label="Estado del Modelo",
            value=verificar_modelo(),
            interactive=False
        )
    
    with gr.Row():
        with gr.Column(scale=1):
            # Input del usuario
            input_text = gr.Textbox(
                label="✏️ Texto de entrada",
                placeholder="Ejemplo: Era una tarde soleada y los niños jugaban en el parque",
                lines=3
            )
            
            # Controles de configuración
            with gr.Accordion("⚙️ Configuración del Modelo", open=False):
                temperatura = gr.Slider(
                    minimum=0.1,
                    maximum=2.0,
                    value=0.7,
                    step=0.1,
                    label="🌡️ Temperatura",
                    info="Mayor temperatura = más creatividad (pero menos coherencia)"
                )
                
                max_tokens = gr.Slider(
                    minimum=50,
                    maximum=500,
                    value=150,
                    step=50,
                    label="📏 Máximo de tokens",
                    info="Longitud máxima de la respuesta"
                )
            
            # Botones
            with gr.Row():
                generar_btn = gr.Button("✨ Transformar", variant="primary")
                limpiar_btn = gr.ClearButton([input_text], value="🗑️ Limpiar")
        
        with gr.Column(scale=1):
            # Output
            output_text = gr.Textbox(
                label="🎨 Texto transformado",
                lines=8,
                interactive=False
            )
    
    # Ejemplos
    gr.Examples(
        examples=[
            ["Era una tarde soleada y los niños jugaban en el parque"],
            ["El gato dormía plácidamente en el sofá"],
            ["María caminaba por la calle cuando empezó a llover"],
            ["Los estudiantes estudiaban para el examen final"],
            ["El reloj marcaba las cinco de la tarde"]
        ],
        inputs=input_text,
        label="💡 Ejemplos"
    )
    
    # Conectar el botón con la función
    generar_btn.click(
        fn=generar_respuesta,
        inputs=[input_text, temperatura, max_tokens],
        outputs=output_text
    )
    
    gr.Markdown(
        """
        ---
        ### ℹ️ Información
        - **Modelo:** Fine-tuneado con LoRA sobre Qwen3-0.6B
        - **Dataset:** Fragmentos de "Alicia en el País de las Maravillas"
        - **Técnica:** Low-Rank Adaptation (LoRA) con Unsloth
        """
    )

# Lanzar la aplicación
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Permite acceso desde la red local
        server_port=7860,
        share=False  # Cambia a True si quieres un link público temporal
    )