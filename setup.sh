#!/bin/bash
echo "🚀 بدء إعداد بيئة Python..."
python --version
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ اكتمل التثبيت!"
