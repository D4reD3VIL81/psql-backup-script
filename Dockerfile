FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and app files
COPY requirements.txt requirements.txt
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default command to prevent immediate container exit
CMD ["bash"]
