from transformers import AutoTokenizer, AutoModelForCausalLM

# Descargar y guardar en una carpeta específica
model_path = "../model/Qwen3-0.6B-base"

print("⬇️ Descargando el modelo Qwen3-0.6B...")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-0.6B")

# Guardar localmente
print
tokenizer.save_pretrained(model_path)
model.save_pretrained(model_path)

print(f"✅ Modelo guardado en: {model_path}")