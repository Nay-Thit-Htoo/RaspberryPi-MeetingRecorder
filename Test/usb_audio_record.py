import pyaudio
import wave

def record_audio(filename, duration, channels, rate, chunk_size):
    # Set up the audio interface
    audio = pyaudio.PyAudio()

    # Find the USB audio card device index
    device_index = None
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if 'USB' in device_info['name']:
            device_index = i
            print(f"Found USB device at index {device_index}: {device_info['name']}")
            break

    if device_index is None:
        print("USB audio device not found!")
        return

    # Open stream for recording
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=rate,
                        input=True,
                        input_device_index=device_index,
                        frames_per_buffer=chunk_size)

    print("Recording...")

    frames = []

    # Record for the given duration
    for _ in range(int(rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the audio interface
    audio.terminate()

    # Save the recorded audio to a file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

# Parameters
filename = "output.wav"
duration = 10  # Record for 10 seconds
channels = 1  # Stereo
rate = 44100  # Sample rate
chunk_size = 1024  # Buffer size

record_audio(filename, duration, channels, rate, chunk_size)
