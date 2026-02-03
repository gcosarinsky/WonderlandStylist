"""
Script para lanzar la aplicación Gradio
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api.gradio_app import demo

if __name__ == "__main__":
    print("🚀 Iniciando Wonderland Stylist...")
    print("📍 La app estará disponible en: http://localhost:7860")
    print("⚠️ Asegúrate de que Ollama está corriendo (ollama serve)")
    print("\nPresiona Ctrl+C para detener\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )