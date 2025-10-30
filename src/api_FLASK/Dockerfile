# puxa a imagem oficial do Python 3.12 slim
FROM python:3.12-slim

# define variáveis de ambiente para melhorar o desempenho do Python e melhorar a depuração
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /POKEMON_MB_API

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

EXPOSE 8000

CMD ["python3", "src/api_FLASK/app.py"]