# Notebook 02: Fine-Tuning con Unsloth
# 1. Instalación de herramientas de alta eficiencia
!pip install --no-deps "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps xformers trl peft accelerate bitsandbytes

from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

# 2. Cargar modelo Llama-3 (optimizado para 4-bit)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/llama-3-8b-bnb-4bit",
    max_seq_length = 2048,
    load_in_4bit = True,
)

# 3. Configurar LoRA (Solo entrenamos el 1-2% de los parámetros)
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
)

# 4. Formatear el Dataset (Prompt Engineering). Formato Instrucción-Input-Respuesta (formato Alpaca)
prompt_format = """A continuación se muestra una instrucción que describe una tarea. 
Escribe una respuesta que complete adecuadamente la petición.

### Instrucción:
{}

### Entrada:
{}

### Respuesta:
{}"""

def formatting_prompts_func(examples):
    instructions = examples["instruction"]
    inputs       = examples["input"]
    outputs      = examples["output"]
    texts = []
    for instruction, input, output in zip(instructions, inputs, outputs):
        text = prompt_format.format(instruction, input, output)
        texts.append(text)
    return { "text" : texts, }

dataset = load_dataset("json", data_files="dataset_alicia.jsonl", split="train")
dataset = dataset.map(formatting_prompts_func, batched = True)

# 5. Entrenamiento
trainer = SFTTrainer(
    model = model,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = 2048,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        max_steps = 60,
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        output_dir = "outputs",
    ),
)
trainer.train()

# 6. Exportar a GGUF para Ollama
model.save_pretrained_gguf("model_alicia", tokenizer, quantization_method = "q4_k_m")