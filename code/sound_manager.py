import os
import pygame
import numpy as np
import wave

class SoundManager:
    def __init__(self, audio_dir):
        pygame.mixer.init()
        self.audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', audio_dir)
        self.original_sound = None
        self.sample_rate = None
        self.audio_data = None

    def load_sound(self, file_name):
        """Load a WAV sound file and prepare it for processing."""
        file_path = os.path.join(self.audio_dir, file_name)
        with wave.open(file_path, 'rb') as wav_file:
            self.sample_rate = wav_file.getframerate()
            n_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            raw_data = wav_file.readframes(wav_file.getnframes())
            
            # Convert raw audio to numpy array
            self.audio_data = np.frombuffer(raw_data, dtype=np.int16).reshape(-1, n_channels)
            self.original_sound = self.audio_data.copy()

    def apply_reverb(self, intensity):
        """Apply a simple reverb effect by mixing delayed versions of the audio."""
        if self.audio_data is not None:
            delay = int(self.sample_rate * 0.03)  # 30ms delay
            decay = 0.5 + (0.05 * intensity)  # Scale decay with intensity
            
            reverb_audio = self.audio_data.copy()
            for i in range(delay, len(self.audio_data)):
                reverb_audio[i] += (self.audio_data[i - delay] * decay).astype(np.int16)
            
            self.audio_data = np.clip(reverb_audio, -32768, 32767)  # Ensure audio stays within 16-bit range

    def apply_distortion(self, intensity):
        """Apply a distortion effect by compressing audio dynamically."""
        if self.audio_data is not None:
            gain = 1 + (intensity / 5)  # Increase gain based on intensity
            distorted_audio = self.audio_data * gain
            
            # Apply soft clipping
            threshold = 30000  # Limit for clipping
            distorted_audio = np.clip(distorted_audio, -threshold, threshold)
            
            self.audio_data = distorted_audio.astype(np.int16)

    def play_sound(self):
        """Play the processed sound using pygame."""
        if self.audio_data is not None:
            sound = pygame.mixer.Sound(buffer=self._numpy_to_bytes(self.audio_data))
            sound.play()

    def reset_sound(self):
        """Reset the sound to the original unprocessed state."""
        if self.original_sound is not None:
            self.audio_data = self.original_sound.copy()

    def _numpy_to_bytes(self, audio):
        """Convert numpy array back to byte string for pygame."""
        return audio.tobytes()

# Usage Example
if __name__ == "__main__":
    sm = SoundManager(audio_dir="audio")
    sm.load_sound("example.wav")
    
    print("Playing original sound...")
    sm.play_sound()
    pygame.time.wait(3000)
    
    sm.apply_reverb(intensity=5)
    print("Playing sound with reverb...")
    sm.play_sound()
    pygame.time.wait(3000)
    
    sm.reset_sound()
    sm.apply_distortion(intensity=7)
    print("Playing sound with distortion...")
    sm.play_sound()
    pygame.time.wait(3000)