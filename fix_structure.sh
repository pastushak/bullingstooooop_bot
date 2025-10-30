#!/bin/bash

cd ~/Projects/bullingstooooop_bot

echo "🔧 Виправляємо структуру проєкту..."

# Перевіряємо вміст requirements.txt
echo ""
echo "�� Поточний requirements.txt в functions/:"
cat functions/requirements.txt

# Створюємо правильний requirements.txt
cat > functions/requirements.txt << 'EOF'
functions-framework==3.*
python-telegram-bot==20.7
python-dotenv==1.0.1
EOF

echo ""
echo "✅ Оновлений functions/requirements.txt:"
cat functions/requirements.txt

# Очищаємо кеш
echo ""
echo "🧹 Очищаємо кеш..."
rm -rf functions/venv
rm -rf functions/__pycache__

echo ""
echo "✅ Готово! Тепер можна деплоїти"
