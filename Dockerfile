# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the bot script and requirements
COPY bot.py ./
COPY requirements.txt ./

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for the bot and Google API
ENV TELEGRAM_TOKEN=your_telegram_bot_token

# Copy Google service account JSON
COPY path/to/your/service_account.json /usr/src/app/service_account.json

# Run the bot
CMD ["python", "bot.py"]
