FROM alpine:3.23

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install Python and its maintained package-manager setuptools build.
# Application dependencies are installed into the image environment.
RUN apk add --no-cache python3 py3-pip py3-setuptools \
    && addgroup -S appgroup \
    && adduser -S appuser -G appgroup -h /app

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY app.py .

RUN chown -R appuser:appgroup /app

USER appuser:appgroup

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=2)" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
