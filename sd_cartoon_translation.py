import requests
import base64

def generate_image_from_image(input_image, output_image):
    url = "http://127.0.0.1:7860/sdapi/v1/img2img"
    
    # Read and encode the input image in base64
    with open(input_image, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    payload = {
        "prompt": "best quality, cartoon_portrait, solo, looking at viewer, head, <lora:cartoonish_v1:0.3>,",
        "negative_prompt": "EasyNegativeV2 ng_deepnegative_v1_75t bad-image-v2-39000",
        "guidance_scale": 3,
        "steps": 20,
        "seed": 1431360298,
        "width": 512,
        "height": 512,
        "sampler_name": "Euler a",
        "init_images": [encoded_image],
        "denoising_strength": 0.3,
        "send_images": True
    }

    # Send the payload to the API
    response = requests.post(url, json=payload)
    
    # Check for successful response
    if response.status_code == 200:
        r = response.json()

        # Decode and save the generated image
        with open(output_image, 'wb') as f:
            f.write(base64.b64decode(r['images'][0]))

        print("Image generated and saved as ", output_image)
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

# Example usage
generate_image_from_image("output.png")
