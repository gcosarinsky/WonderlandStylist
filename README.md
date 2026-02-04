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
El prompt utilizado sigue el siguiente template:

> ### Instrucción:
> 
> Reescribe el siguiente texto con el estilo de Alicia en el País de las Maravillas.
> 
> 
> 
> ### Entrada:
> 
> {frase}
> 
> 
> 
> ### Respuesta:


### 2. Fine-tuning del Modelo
Ejecutar el notebook `notebook_02_lora_finetuning.ipynb` para entrenar el modelo Qwen3 0.6B con LoRA. 

**Requisitos:**
- GPU compatible con CUDA
- Librería Unsloth instalada

**Proceso:**
El notebook realiza fine-tuning utilizando Unsloth, que incluye optimizaciones para acelerar el entrenamiento. Al finalizar, genera automáticamente el modelo cuantizado en formato GGUF (Q4_K_M) y lo guarda en:

```
model/Qwen3-0.6B-Base.Q4_K_M_Alicia.gguf
```

### 3. Cargar el Modelo en Ollama

Una vez generado el archivo GGUF, es necesario crear un modelo personalizado en Ollama utilizando el archivo `model\Modelfile.alicia`, que define el prompt del sistema y los parámetros de inferencia.

**Opción 1: Usar el script automatizado**

Ejecutar el script correspondiente a tu sistema operativo:

**Windows:**
```bash
setup_ollama_model.bat
```

**Linux/Mac:**
```bash
chmod +x setup_ollama_model.sh
./setup_ollama_model.sh
```

**Opción 2: Pasos manuales**

1. Navegar al directorio del modelo:
```bash
cd model
```

2. Crear el modelo personalizado en Ollama:
```bash
ollama create alicia -f Modelfile.alicia
```

3. Iniciar el modelo en modo servidor:
```bash
ollama run alicia
```

**Nota:** El modelo debe permanecer en ejecución para que la aplicación Python pueda enviar requests de inferencia a través de la API de Ollama.


### 4. Ejecutar la Interfaz Gradio

```bash
python scripts/run_gradio_app.py
```

O directamente:

```bash
python api/gradio_app.py
```
## 🧪 Testing y Validación

### Probar el Modelo Base (Sin Fine-tuning)

Para comparar el comportamiento del modelo Qwen3:0.6b antes del fine-tuning:

```bash
python scripts/test_base_model.py
```

Este script ejecuta múltiples prompts de prueba, incluyendo el template utilizado en el modelo final. Los resultados se guardan automáticamente con timestamp.

**Ejemplo de salida:** `scripts/test_base_model_output_20260203_155348.txt`

### Inspeccionar el Dataset de Entrenamiento

Para visualizar los pares de entrenamiento generados:

```bash
python scripts/view_dataset.py
```

Este script permite explorar el dataset `synthetic_alicia.jsonl` ejemplo por ejemplo, mostrando el formato instruction-input-output utilizado durante el fine-tuning.


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

## 🔍 Resultados y Conclusiones

El modelo presenta limitaciones significativas en la generación de texto con el estilo de Alicia en el País de las Maravillas. A continuación se muestran ejemplos representativos del comportamiento actual:

**Input de prueba:**
```
El gato dormía plácidamente en el sofá
```

**Outputs generados:**

1. *"El gato dormía plácidamente en el sofá, como si el mundo fuera una estatua."*
    - Añade una comparación, pero no captura el estilo narrativo característico.

2. *"A Alicia le gustaba la idea de que el gato dormía plácidamente en el sofá, porque creía que así sería el gato que dormía en su propio cuarto."*
    - Incorpora el personaje de Alicia, pero la estructura es confusa y redundante.

3. *"El gato durmiendo en el sofá, no parece muy lejos de aquí."*
    - Apenas modifica el texto original, perdiendo coherencia.

4. *"«—No te lo digo en serio—. —De nuevo, le estaba diciendo a Alicia que no podía dejarlo con ella. —No, es una vez en su vida que un gato dura un día y no más.»"*
    - Genera diálogos sin contexto y con poca coherencia semántica.

### Análisis y Mejoras Propuestas

**Problemas identificados:**

- El modelo no logra capturar consistentemente el tono y las estructuras narrativas características de Lewis Carroll
- Las transformaciones tienden a ser superficiales o a generar texto incoherente
- La estrategia de generación de datos sintéticos (invertir texto estilizado → texto plano) puede no ser óptima

**Líneas de mejora:**

1. **Revisión del dataset de entrenamiento:**
    - Aumentar la cantidad de ejemplos de entrenamiento
    - Validar manualmente la calidad de los pares sintéticos generados
    - Considerar incluir ejemplos reales de transformaciones de estilo

2. **Optimización del prompt template:**
    - Experimentar con instrucciones más específicas
    - Ajustar los parámetros de temperatura y top-p durante la inferencia

3. **Alternativas de arquitectura:**
    - Probar modelos base de mayor capacidad (1.5B-3B parámetros)
    - Considerar enfoques de transfer learning desde modelos pre-entrenados en tareas similares


## 📝 Notas

- El modelo está optimizado para español
- Los datos de entrenamiento provienen del texto original "Alicia en el País de las Maravillas" de Lewis Carroll
- La cuantización Q4_K_M reduce el tamaño del modelo manteniendo la calidad
- Este proyecto fue realizado con la asistencia de Github Copilot


