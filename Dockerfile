FROM python:3

RUN apt-get update
RUN apt-get install -y firefox-esr wget
RUN apt-get clean

RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz; \
    elif [ "$ARCH" = "aarch64" ]; then \
        wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux-aarch64.tar.gz -O /tmp/geckodriver.tar.gz; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    tar -xvzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver

RUN geckodriver --version

# Устанавливаем рабочую директорию
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копируем файлы приложения в контейнер
COPY . /app

# Открываем порт, на котором будет работать Flask
EXPOSE 5000

# Запускаем приложение
CMD ["python", "front.py"]