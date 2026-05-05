#!/bin/bash

set -e  # corta si hay error

echo "📦 Downloading Transfermarkt dataset..."

DATA_DIR="data/raw/transfermarkt/kaggle_player_scores"

# Crear carpeta si no existe
mkdir -p $DATA_DIR

# Descargar dataset
kaggle datasets download \
  -d davidcariboo/player-scores \
  -p $DATA_DIR

# Ir a carpeta
cd $DATA_DIR

# Descomprimir (sobrescribe si existe)
unzip -o player-scores.zip

# Borrar zip
rm player-scores.zip

echo "✅ Dataset descargado y listo en: $DATA_DIR"