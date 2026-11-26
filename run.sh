#!/bin/bash
# Script para executar análise associativa com Spark

source .venv/bin/activate
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

python analise_associativa.py
