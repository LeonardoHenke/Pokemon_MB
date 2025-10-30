FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /POKEMON_MB_CLI

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /API_POKEMON_MB/requirements.txt
RUN pip install -e .

EXPOSE 8000

# Comando padrão: ajusta se seu arquivo principal da CLI for outro
CMD ["python", "src/CLI.py"]