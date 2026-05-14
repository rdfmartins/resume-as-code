#!/bin/bash

# Script de automação para geração rápida de PDF a partir de Markdown do CV Pipeline

if [ -z "$1" ]; then
  echo "Uso: ./generate_pdf.sh <arquivo.md>"
  exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="${INPUT_FILE%.md}.pdf"

echo "Iniciando o motor de renderização PDF..."
CSS_FILE="./cv_style.css"
npx -y md-to-pdf "$INPUT_FILE" --stylesheet "$CSS_FILE" --launch-options '{ "args": ["--no-sandbox", "--disable-setuid-sandbox"] }' > pdf_generation.log 2>&1
if [ $? -eq 0 ]; then
  echo "[OK] PDF gerado com sucesso: $OUTPUT_FILE"
else
  echo "[ERRO] Falha ao gerar o PDF."
  exit 1
fi
