# 1. On part d'une image qui contient déjà Python
FROM python:3.9-slim

# 2. On crée un dossier pour le code
WORKDIR /app

# 3. On installe les librairies nécessaires
# (On installe aussi gcc pour que mysql-connector fonctionne bien)
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential

# 4. On copie la liste des besoins (requirements.txt) et on installe
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. On copie tout ton code Scrapy dans le conteneur
COPY . .

WORKDIR /app/comparateur

# 6. La commande par défaut (sera remplacée par celle du docker-compose)
CMD ["scrapy", "list"]

EXPOSE 8501

