FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/src/

# Set Python path to include src
ENV PYTHONPATH=/app

# Expose ports for API and Streamlit
EXPOSE 8000
EXPOSE 8501

# Create a startup script
RUN echo '#!/bin/bash\n\
    uvicorn src.api.endpoints:app --host 0.0.0.0 --port 8000 & \n\
    streamlit run src/frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0\n\
    ' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]