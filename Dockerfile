FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV GRADIO_ANALYTICS_ENABLED=False
ENV MPLCONFIGDIR=/tmp/matplotlib

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/matplotlib

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY peak_ground_acceleration_estimator.py app.py ./

EXPOSE 7860

CMD ["python", "app.py"]
