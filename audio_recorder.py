from datetime import datetime
import os
import threading
import wave
import pyaudio

import file_upload_service


class AudioRecorder:
    def __init__(self,record_user_obj):
        self.record_user_obj=record_user_obj
        self.output_audio_path = os.path.join(record_user_obj['usercode'],f"{record_user_obj['usercode']}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.wav")
        self.channels = 2
        self.rate = 44100
        self.chunk = 1024
        self.format = pyaudio.paInt16
        
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False
        self.record_thread=None
    
    def start_recording(self):
        if self.recording:
            return
        
        self.recording = True
        self.frames = []
        
        def record():
            self.stream = self.audio.open(format=self.format,
                                          channels=self.channels,
                                          rate=self.rate,
                                          input=True,
                                          frames_per_buffer=self.chunk)
            print(f"[Audio Record Service]:[Start Audio Record]")
            while self.recording:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
            
            self.stream.stop_stream()
            self.stream.close()
            self.save_wave()
        
        self.record_thread = threading.Thread(target=record)
        self.record_thread.start()
    
    def stop_recording(self):
        self.recording = False
        if(self.record_thread is not None):
            self.record_thread.join()  # Wait for the recording thread to finish
    
    def save_wave(self): 
        with wave.open(self.output_audio_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
        
        print(f"[Audio Record Service]:[Saved Audio Record] ", os.path.basename(self.output_audio_path))
    
    def terminate(self):
        self.audio.terminate()   
        if(os.path.exists(self.output_audio_path)):
            file_upload_service.file_upload_to_server(self.output_audio_path,self.record_user_obj)   
            file_upload_service.delete_file_after_upload(self.output_audio_path)