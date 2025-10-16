import logging
import requests
import config
from random import randint

logging.basicConfig(
    filename='analytics.log',  
    level=logging.DEBUG,       
    format='%(asctime)s %(message)s' 
)

class Research:
    class Calculations:
        def __init__(self, data):
            self.data = data

        def counts(self):
            logging.debug("Calculating the counts of heads and tails")

            heads = sum(1 for pair in self.data if pair == [0, 1])
            tails = sum(1 for pair in self.data if pair == [1, 0])
            return heads, tails

        def fractions(self, heads, tails):
            logging.debug(f"Calculating fractions: heads={heads}, tails={tails}")

            total = heads + tails
            if total == 0:
                return 0, 0
            return heads/total, tails/total


    def __init__(self, file_path):
        self.file_path = file_path


    def send_telegram_message(self, message):
        url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"
        data = {"chat_id": config.telegram_chat_id, "text": message}
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            logging.info(f"Telegram message sent successfully: {message}")
        except Exception as e:
            logging.error(f"Failed to send Telegram message: {e}")

    def file_reader(self, has_header=True):
        logging.debug(f"Reading file: {self.file_path}")
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()

                if has_header:
                    lines = lines[1:]

                data = []
                for line in lines:
                    clean = line.strip()  
                    parts = clean.split(',')  
                    row = [int(x) for x in parts]
                    data.append(row)
                logging.debug(f"File read successfully: {len(data)} rows")
                return data

        except FileNotFoundError:
            logging.error(f"File not found: {self.file_path}")
            raise FileNotFoundError(f"File '{self.file_path}' not found.")

class Analytics(Research.Calculations):
    def predict_random(self, n):
        logging.debug(f"Generating {n} random predictions")
        predictions = []
        for _ in range(n):
            head = randint(0, 1)
            tail = 1-head
            predictions.append([head, tail])
        return predictions

    def predict_last(self):
        logging.debug("Returning the last observation from data")
        if not self.data:
            return None
        return self.data[-1]
    
    def save_file(self, data, file_name, extension):
        full_name = f"{file_name}.{extension}"
        logging.debug(f"Saving data to file: {full_name}")
        try:
            with open(full_name, 'w') as f:
                if isinstance(data, list) and all(isinstance(row, list) for row in data):
                    for row in data:
                        f.write(','.join(map(str, row)) + '\n')
                else:
                    f.write(str(data))

            logging.info(f"File saved successfully: {full_name}")
            return full_name
        except Exception as e:
            logging.error(f"Error saving file {full_name}: {e}")
            raise Exception(f"Could not save file: {e}")


