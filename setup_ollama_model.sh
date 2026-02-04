#!/bin/bash

echo "============================================"
echo "  Wonderland Stylist - Ollama Model Setup"
echo "============================================"
echo ""

echo "[1/3] Navegando al directorio del modelo..."
cd "$(dirname "$0")/model" || {
    echo "ERROR: No se pudo acceder al directorio model"
    exit 1
}
echo "OK: En directorio $(pwd)"
echo ""

echo "[2/3] Creando modelo personalizado en Ollama..."
ollama create alicia -f Modelfile.alicia || {
    echo "ERROR: Fallo al crear el modelo"
    exit 1
}
echo "OK: Modelo creado exitosamente"
echo ""

echo "[3/3] Iniciando modelo en modo servidor..."
echo "NOTA: Presiona Ctrl+C para detener el servidor"
echo ""
ollama run alicia
