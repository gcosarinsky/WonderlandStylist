# 🎩 Wonderland Stylist

Un proyecto de IA que transforma texto plano al estilo literario de "Alicia en el País de las Maravillas" de Lewis Carroll, utilizando un modelo LLM optimizado para ejecutarse con recursos de hardware limitados.

## 📋 Descripción

Este proyecto implementa un sistema completo de fine-tuning y deployment de un modelo de lenguaje para transformar frases cotidianas en texto con el estilo característico de Alicia en el País de las Maravillas. El modelo final es ligero y eficiente, diseñado para funcionar en hardware modesto.

## 🏗️ Arquitectura del Proyecto

### 1. Generación de Datos Sintéticos
- **Modelo**: `llama3.2` mediante Ollama
- **Proceso**: Generación de pares de texto (normal → estilo Alicia)
- **Salida**: Dataset sintético en formato JSONL

### 2. Fine-tuning con LoRA
- **Framework**: Unsloth
- **Modelo base**: Qwen3 0.6B
- **Técnica**: LoRA (Low-Rank Adaptation)
- **Formato final**: GGUF optimizado (Q4_K_M)

### 3. Inferencia
- **Runtime**: Ollama
- **Interfaz**: Gradio Web UI
- **Modelo**: `Qwen3-0.6B-Base.Q4_K_M_Alicia.gguf`

## 📁 Estructura del Proyecto

```
WonderlandStylist/
├── api/                    # API y aplicación web
│   └── gradio_app.py      # Interfaz Gradio
├── data/                   # Datos de entrenamiento
│   ├── synthetic_alicia.jsonl
│   ├── chunks_nltk.txt
│   ├── create_chunks.py
│   └── raw/               # Texto original de Alicia
├── model/                  # Modelos y configuración
│   ├── Modelfile.alicia
│   └── Qwen3-0.6B-Base.Q4_K_M_Alicia.gguf
├── notebooks/              # Notebooks de desarrollo
│   ├── notebook_01_gen_synthetic_data.ipynb
│   └── notebook_02_lora_finetuning.ipynb
├── scripts/                # Scripts de utilidad y testing
│   ├── run_gradio_app.py
│   ├── test_base_model.py
│   └── view_dataset.py
└── fastapi_tests/          # Tests y experimentos con FastAPI
```

### Requisitos
- Python 3.8+
- Ollama instalado
- CUDA (opcional, para aceleración GPU)

## 💻 Uso

### 1. Generar Dataset Sintético
Ejecutar el script `data/create_chunks.py` para fragmentar el texto original de Alicia usando NLTK. Luego, ejecutar el notebook `notebook_01_gen_synthetic_data.ipynb` para transformar cada fragmento al estilo plano usando llama3.2. Este proceso inverso genera el dataset de entrenamiento en formato instruction-input-output, guardado en `data/synthetic_alicia.jsonl`.

### 2. Fine-tuning del Modelo
Ejecutar el notebook `notebook_02_lora_finetuning.ipynb` para entrenar el modelo Qwen3 con LoRA (se necesita GPU para usar unsloth)

### 3. Cargar el Modelo en Ollama

```bash
cd model
ollama create alicia -f Modelfile.alicia
```

### 4. Ejecutar la Interfaz Gradio

```bash
python scripts/run_gradio_app.py
```

O directamente:

```bash
python api/gradio_app.py
```

## 🧪 Testing

Probar el modelo base:
```bash
python scripts/test_base_model.py
```

Ver el dataset generado:
```bash
python scripts/view_dataset.py
```

## 🛠️ Tecnologías Utilizadas

- **Ollama**: Runtime para modelos LLM
- **Unsloth**: Framework de fine-tuning optimizado
- **Gradio**: Framework para interfaces web interactivas
- **Qwen3 0.6B**: Modelo base ligero
- **LoRA**: Técnica de fine-tuning eficiente
- **GGUF**: Formato de modelo cuantizado

## 📊 Características del Modelo

- **Tamaño**: ~400MB (cuantizado Q4_K_M)
- **Parámetros**: 0.6B
- **Requisitos de RAM**: ~2-4GB

## 📝 Notas

- El modelo está optimizado para español
- Los datos de entrenamiento provienen del texto original "Alicia en el País de las Maravillas" de Lewis Carroll
- La cuantización Q4_K_M reduce el tamaño del modelo manteniendo la calidad

