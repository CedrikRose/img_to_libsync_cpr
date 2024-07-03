from gradio_client import Client

def generate_video_from_image(image_path, output):
    client = Client("http://127.0.0.1:7860/")
    result = client.predict(
        image_path,	# str (filepath or URL to image) in 'Source image' Image component
        "cuttet_audio.mp3",	# str (filepath or URL to file) in 'Input audio' Audio component
        "full",	# str in 'preprocess' Radio component
        True,	# bool in 'Still Mode (fewer head motion, works with preprocess `full`)' Checkbox component
        True,	# bool in 'GFPGAN as Face enhancer' Checkbox component
        1,	# int | float (numeric value between 0 and 10) in 'batch size in generation' Slider component
        "256",	# str in 'face model resolution' Radio component
        1,	# int | float (numeric value between 0 and 46) in 'Pose style' Slider component
        fn_index=0
    )
    print(result)
    
    # Save the resulting video
    with open(output, "wb") as f:
        f.write(result["video"])
    
    print("Video generated and saved as ", output)

# Example usage
generate_video_from_image("final_output.png")
