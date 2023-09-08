import json
import logging
import os
import secrets
import sys
import textwrap

import openai
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont


load_dotenv()

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')

AI_ROLE = 'You are an original quote generator. Your quotes should be unique, thought-provoking, and have the potential to inspire or resonate with others. Feel free to draw inspiration from personal experiences, observations, or reflections. Your quote can be in any format, such as a short sentence or a short phrase. Be creative and strive to create something that is both memorable and impactful. Do not write anything except for the quote. No explanation, no source, just the quote' 
AI_PROMPT = 'Create an original quote that conveys a meaningful message or insight. Also come up with an original name of a character who said it and an original source title (like a book, movie or something of sorts). Write it all as a json file with the following columns: "author", "source", "quote". Do not include brackets [] in your answer.'
QUOTE_BG_THEME = 'Quote Background'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        quote_data = create_quote()
        get_random_image()
        place_text_on_image(quote_data['quote'])
        
        return render_template('index.html', quote_data=quote_data)

    else:        
        return render_template('index.html')
    

def create_quote():
    try:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': AI_ROLE},
                {'role': 'user', 'content': AI_PROMPT}
            ]
        )
    except Exception as e:
        return "There was an error: " + str(e)
    
    answer = completion.choices[0].message.content
    answer_json = json.loads(answer)

    quote_data = {
        'author': answer_json['author'],
        'source': answer_json['source'],
        'quote': answer_json['quote']
    }
    
    return quote_data


def get_random_image():
    query = QUOTE_BG_THEME.lower().replace(' ', '%20')
    
    url = r'https://api.pexels.com/v1/search?query=' + query
    response = requests.get(url, headers={'Authorization': PEXELS_API_KEY}, params={'per_page': 1})

    if response.status_code == 200:
        json_page = response.json()
        total_results = int(json_page['total_results'])
        random_page_num = secrets.choice(range(1, total_results))
        
        random_page = requests.get(url, headers={'Authorization': PEXELS_API_KEY}, params={'per_page': 1, 'page': random_page_num}).json()
        random_image = random_page['photos'][0]['src']['landscape']
        with open('static/images/image.jpeg', 'wb') as f:
            f.write(requests.get(random_image).content)
        
        return random_image


def place_text_on_image(text):
    try:
        img = Image.open('static/images/image.jpeg')
    except FileNotFoundError:
        return None
    draw = ImageDraw.Draw(img, "RGBA")
    font = ImageFont.truetype('arial.ttf', 50)
    wrapped_text = textwrap.wrap(text, width=img.width//28)
    
    x, y = 100, 100
    draw.rectangle((x-20, y-20, x + img.width-200, y + img.height-200), fill=(0, 0, 0, 204))
    for line in wrapped_text:
        draw.text((x, y), line, font=font, fill="white")
        y += 65
        
    img.save('static/images/final_image.jpeg')


if __name__ == '__main__':
    app.run(debug=True)
