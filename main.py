import openai
import requests
import time
from datetime import datetime
from google.cloud import storage
from dotenv import load_dotenv
import os
import random

load_dotenv()

# OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
ACCESS_TOKEN = os.getenv('THREADS_ACCESS_TOKEN')
BUSINESS_ACCOUNT_ID = os.getenv('THREADS_BUSINESS_ACCOUNT_ID')

house_type = [
    "1LDK",
    "2DK",
    "3LDK",
    "4LDK",
    "studioHouse",
    "penthouse",
    "houseWithLoft",
    "townHouse",
    "duplex",
    "openPlan"
]
price = [
    "~$100,000",
    "$100,000〜$300,000",
    "$300,000〜$500,000",
    "$500,000〜$1,000,000",
    "$1,000,000~$10,000,000",
    "$10,000,000~"
]
architectural_style = [
    "ModernHouse",
    "CraftsmanHouse",
    "ColonialHouse",
    "VictoriaHouse",
    "TraditionalJapaneseHouses",
    "MediterraneanStyleHouse",
    "FuturisticHouse"
]

def generate_image_for_api(my_prompt):
    response = openai.images.generate(
            model="dall-e-3",
            prompt=my_prompt,
            n=1,
            size="1024x1024",
        )
    image_url = response.data[0].url
    print(f"Generated image URL: {image_url}")
    return image_url

def save_image(url, image_path):
    img_response = requests.get(url)
    # save image as file
    image_path = f"/tmp/image_{BUSINESS_ACCOUNT_ID}.png"
    with open(image_path, 'wb') as file:
        file.write(img_response.content)
    if img_response.status_code == 200:
        with open('generated_image.png', 'wb') as f:
            f.write(img_response.content)
        return "Image downloaded successfully."
    else:
        return "Failed to download the image."
    
def create_post_detail(image_url, my_prompt):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"What are in this image? Describe it good for sns post. The image title tells that {my_prompt} for 100 letters",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                },
            ],
            }
        ],
        max_tokens=1000,
    )
    ai_response = response.choices[0].message.content
    return ai_response
  
def upload_to_bucket(blob_name, file_path, bucket_name):
    # Create a Cloud Storage client
    storage_client = storage.Client()
    # Get the bucket that the file will be uploaded to
    bucket = storage_client.bucket(bucket_name)
    # Create a new blob and upload the file's content
    blob = bucket.blob(blob_name+'.png')
    blob.upload_from_filename(file_path)
    # Make the blob publicly viewable
    blob.make_public()
    # Return the public URL of the uploaded file
    return blob.public_url

def post_threads(image_url, caption):
    url = f'https://graph.threads.net/v1.0/{BUSINESS_ACCOUNT_ID}/threads'
    params = {
        'media_type': 'IMAGE',
        'image_url': image_url,
        'text': caption,
        'access_token': ACCESS_TOKEN,
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        media_id = response.json().get('id')
        print(f"Media ID: {media_id}")
        url = f'https://graph.threads.net/v1.0/{BUSINESS_ACCOUNT_ID}/threads_publish'
        params = {
            'creation_id': media_id,
            'access_token': ACCESS_TOKEN
        }
        response = requests.post(url, data=params)
        if response.status_code == 200:
            print("Image uploaded and published successfully!")
        else:
            print(f"Failed to publish the image: {response.text}")
    else:
        print(f"Failed to create media object: {response.text}")

if __name__ == '__main__':
    # pick cartoon and pattern
    house_type = random.choice(house_type)
    price = random.choice(price)
    architectural_style = random.choice(architectural_style)
    my_prompt = f"{architectural_style} with {house_type} at a cost of {price}. Do not include text."
    image_path = f"/tmp/image_{BUSINESS_ACCOUNT_ID}.png"
    image_url = generate_image_for_api(my_prompt)
    res = save_image(image_url, image_path)
    current_time = int(time.time())
    date_time = datetime.fromtimestamp(current_time)
    current_time_string = date_time.strftime("%Y-%m-%d %H:%M")
    image_url = upload_to_bucket(current_time_string, image_path, "ai-bot-app-dev")
    print(image_url)
    ai_response = create_post_detail(image_url, my_prompt)
    caption = f"{ai_response} #{architectural_style} #{house_type} #{price}"
    post_threads(image_url, caption)

