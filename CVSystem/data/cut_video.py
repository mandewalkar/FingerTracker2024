import moviepy.editor as mp
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from moviepy.video.io.VideoFileClip import VideoFileClip

# Step 1: Extract audio from the video
video_path = 'C0011.MP4'
audio_clip = mp.AudioFileClip(video_path)
audio_array = audio_clip.to_soundarray()
audio_clip.close()

# Step 2: Combine stereo channels into mono
if audio_array.ndim == 2:
    audio_array_mono = np.mean(audio_array, axis=1)
else:
    audio_array_mono = audio_array

#Generate a chirp signal of desired hz and duration

# Define parameters
duration = 2.5  # Duration of the tone in seconds
sample_rate = 44100  # Sample rate (samples per second)
frequency = 1000  # Frequency of the tone in Hz

# Calculate the number of samples
num_samples = int(duration * sample_rate)

# Generate the time axis
time = np.linspace(0, duration, num_samples, endpoint=False)

# Generate the tone
tone = np.sin(2 * np.pi * frequency * time)

# Normalize the tone to the range [-1, 1]
tone /= np.max(np.abs(tone))

# Optionally, if you want to add silence at the end to make it exactly 2.5 seconds long
desired_length = int(duration * sample_rate)
current_length = len(tone)
if current_length < desired_length:
    silence_length = desired_length - current_length
    silence = np.zeros(silence_length)
    tone = np.concatenate((tone, silence))

conv = signal.convolve(audio_array_mono, np.squeeze(tone)[::-1])
conv = np.abs(conv)

min = np.argmax(conv[:len(conv)//2])
max = np.argmax(conv[len(conv)//2:]) + (len(conv)//2 - 1) - (len(conv) - len(audio_array_mono))
start_time = min / sample_rate 
end_time = max / sample_rate 

#cut video
output_video_path = 'output_video.mp4'
clip = VideoFileClip(video_path)
trimmed_clip = clip.subclip(start_time, end_time)
trimmed_clip.write_videofile(output_video_path, codec='libx264', fps=clip.fps)
clip.close()
