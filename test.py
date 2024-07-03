import numpy as np
from moviepy.editor import VideoFileClip

def make_white_pixels_transparent(input_path, output_path, tolerance=30):
    """
    Makes all white pixels within a given tolerance transparent in the video.
    
    :param input_path: Path to the input WebM file
    :param output_path: Path to the output WebM file with transparency
    :param tolerance: Tolerance for white pixel detection
    """
    def process_frame(frame):
        # Convert frame to float and normalize to 0-1 range
        frame = frame.astype(np.float32) / 255
        # Define the white color (R, G, B)
        white_color = np.array([1, 1, 1], dtype=np.float32)
        # Calculate the distance from the white color
        distance = np.linalg.norm(frame[:, :, :3] - white_color, axis=2)
        # Create alpha channel
        alpha_channel = np.where(distance <= (tolerance / 255), 0, 1)
        # Expand alpha channel dimensions to match the frame dimensions
        alpha_channel = np.expand_dims(alpha_channel, axis=2)
        # Combine frame with alpha channel
        frame_with_alpha = np.concatenate((frame, alpha_channel), axis=2)
        # Convert frame back to 0-255 range
        frame_with_alpha = (frame_with_alpha * 255).astype(np.uint8)
        return frame_with_alpha

    # Load the video file
    video_clip = VideoFileClip(input_path)
    
    # Apply the process_frame function to each frame of the video
    transparent_clip = video_clip.fl_image(process_frame)
    
    # Write the video file in WebM format with transparency
    transparent_clip.write_videofile(output_path, codec='libvpx-vp9')

# Example usage
input_file = "output_video00000.webm"
output_file = "transparent_video00000.webm"
make_white_pixels_transparent(input_file, output_file)
