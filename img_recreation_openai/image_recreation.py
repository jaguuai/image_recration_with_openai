import openai
import os
import configparser
from PIL import Image

# Load the configuration from the file
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    required_keys = ['api_key', 'text_model', 'dalle_model', 'size', 'max_tokens']
    missing_keys = [key for key in required_keys if key not in config['API']]

    if missing_keys:
        raise KeyError(f"⚠️ Config dosyasındaki şu anahtarlar eksik: {', '.join(missing_keys)}")
    
    return config

# Parse the image size from the config (in format 1024x1024)
def parse_size(size_str):
    width, height = size_str.split('x')
    return int(width), int(height)

# Generate a description for the image using OpenAI's API
def generate_description_from_image(image_path, config):
    try:
        # Open the image (just to load it for further processing)
        image = Image.open(image_path)
        
        # Generate description using the OpenAI API
        response = openai.Completion.create(
            model=config['API']['text_model'],
            prompt=f"Please describe the contents of this image: {image_path}",
            max_tokens=int(config['API']['max_tokens'])
        )
        description = response.choices[0].text.strip()
        print(f"🎨 Görsel: {image_path}\nAçıklama: {description}")
        return description

    except Exception as e:
        print(f"⚠️ Görsel açıklaması oluşturulurken hata oluştu: {str(e)}")
        return None

# Create a new image from the description using OpenAI's DALL-E API
def create_image_from_description(description, config):
    try:
        width, height = parse_size(config['API']['size'])
        
        response = openai.Image.create(
            prompt=description,
            n=1,
            size=f"{width}x{height}",
            model=config['API']['dalle_model']
        )
        image_url = response['data'][0]['url']
        print(f"🎨 Görsel oluşturuldu: {image_url}")
        return image_url
    except Exception as e:
        print(f"⚠️ Görsel oluşturulurken hata oluştu: {str(e)}")
        return None

# Process images in the folder
def process_images_in_folder(config):
    image_folder = config['Settings']['image_folder']
    
    # Get all image files in the folder
    images = [f for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
    
    for idx, image_filename in enumerate(images[:int(config['Settings']['num_images'])]):  # Process first 3 images
        image_path = os.path.join(image_folder, image_filename)
        
        # Generate description for the image
        description = generate_description_from_image(image_path, config)
        
        if description:
            # Create a new image based on the description
            create_image_from_description(description, config)

# Main execution
def main():
    try:
        # Load the config
        config = load_config()
        
        # Set the OpenAI API key
        openai.api_key = config['API']['api_key']
        
        # Process the images in the folder
        process_images_in_folder(config)
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()
