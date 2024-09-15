from datetime import datetime
import os
import pyaudio
import wave
import threading

import file_upload_service

# Parameters for audio recording
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 2 # 1 channel (mono)
RATE = 44100  # 44.1kHz sampling rate
CHUNK = 1024  # 2^10 samples for buffer

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Create a flag to control the recording state
stop_recording = threading.Event()

def record_audio(record_user_obj):
    # Open audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print(f"[Audio Recording] Start Audio Recording...")
    
    frames = []

    # Continue recording until stop_recording event is set
    while not stop_recording.is_set():
        data = stream.read(CHUNK)
        frames.append(data)

    print(f"[Audio Recording] Stop Audio Recording...")
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()

     # Ensure the subfolder exists
    os.makedirs(record_user_obj['usercode'], exist_ok=True)    
    output_audio_path=os.path.join(record_user_obj['usercode'],f"{record_user_obj['usercode']}_{datetime.now().strftime('%d_%m_%Y')}.wav")
 
    # Write the recorded data to a WAV file
    with wave.open(output_audio_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    audio.terminate()
    file_upload_service.file_upload_to_server(output_audio_path,record_user_obj)


def stop_audio_recording(record_user_obj):    
    # Set the flag to stop the recording
    stop_recording.set()

def start_audio_record(record_user_obj):   
    # Start recording in a separate thread
    record_thread = threading.Thread(target=record_audio,args=(record_user_obj,))
    record_thread.start()

