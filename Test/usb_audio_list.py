import pyaudio

def list_audio_devices():
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # List all available devices
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        print(f"Device Index: {i}")
        print(f" - Name: {device_info['name']}")
        print(f" - Max Input Channels: {device_info['maxInputChannels']}")
        print(f" - Max Output Channels: {device_info['maxOutputChannels']}")
        print(f" - Default Sample Rate: {device_info['defaultSampleRate']}")
        print("")

    # Terminate PyAudio
    audio.terminate()

list_audio_devices()
