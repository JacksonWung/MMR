import os
import pygame
from pydub import AudioSegment
from pydub.generators import Sine

class SoundManager:
    def __init__(self, audio_dir, initial_price):
        pygame.mixer.init()
        self.initial_price = initial_price
        self.audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', audio_dir)
        self.notes = [
            "D3", "E3", "F3", "G3", "A3", "B3",  # Lower octave
            "C4", "D4", "E4", "F4", "G4", "A4", "B4"  # Middle octave
        ]
        self.sounds = self.load_sounds()
        self.drums = self.load_drums()
        self.current_drum = None
        self.current_state = None  # Record the current play state

    def load_sounds(self):
        sounds = {}
        for note in self.notes:
            full_path = os.path.join(self.audio_dir, f"{note}.wav")
            sounds[note] = pygame.mixer.Sound(full_path)
            sounds[note].set_volume(0.8)  # Increase note volume
        return sounds

    def load_drums(self):
        drums = {
            "normal": pygame.mixer.Sound(os.path.join(self.audio_dir, "gain_drum.mp3")),
            "gain": pygame.mixer.Sound(os.path.join(self.audio_dir, "money.mp3")),
            "loss": pygame.mixer.Sound(os.path.join(self.audio_dir, "loss_drum.wav"))
        }
        for drum in drums.values():
            drum.set_volume(0.3)  # Lower background music volume
        return drums

    def play_sound(self, sound):
        """ Play the specified sound. """
        sound.play()

    def play_drum(self, drum_type):
        """ Play the specified type of background music. """
        if self.current_state == drum_type:
            # Keep the current music playing if the state hasn't changed
            return

        if self.current_drum:
            self.current_drum.fadeout(1000)  # Fade out current audio in 1 second

        if drum_type in self.drums:
            self.current_drum = self.drums[drum_type]
            self.current_drum.play(loops=-1, fade_ms=1000)  # Fade in new audio in 1 second
            self.current_state = drum_type  # Update state

    def get_note_by_price_change(self, current_price, next_price):
        """
        Calculate the corresponding note based on price change.
        - No change: play C4
        - Every 0.5% increase: raise one note
        - Every 0.5% decrease: lower one note
        """
        if current_price == 0:  # Prevent division by zero
            return "C4"

        # Calculate percentage change in price
        price_change = (next_price - self.initial_price) / self.initial_price
        step = round(price_change / 0.005)  # Change one note per 0.5%

        # Index position of C4
        c4_index = self.notes.index("C4")
        target_index = c4_index + step

        # Ensure the note index is within range
        target_index = max(0, min(len(self.notes) - 1, target_index))
        return self.notes[target_index]

    def play_based_on_price(self, current_price, next_price, apply_reverb=False, reverb_intensity=5, apply_distortion=False, distortion_intensity=5):
        """ Play the corresponding note based on price change and apply filters if necessary. """
        note = self.get_note_by_price_change(current_price, next_price)
        sound = self.sounds[note]

        # Apply reverb if specified
        if apply_reverb:
            sound = self.apply_reverb(sound, intensity=reverb_intensity)

        # Apply distortion if specified
        if apply_distortion:
            sound = self.apply_distortion(sound, intensity=distortion_intensity)

        # Play the processed sound
        self.play_sound(sound)

    def apply_reverb(self, sound, intensity=5):
        """
        Apply a simple reverb effect with a specific intensity.
        This is achieved by mixing the sound with a delayed version of itself.
        """
        sound_path = os.path.join(self.audio_dir, f"{sound}.wav")
        sound_audio = AudioSegment.from_wav(sound_path)

        # Simple reverb: Add delayed version of the sound to create an echo effect
        delay_ms = 50 * intensity  # Delay is controlled by intensity
        delayed_sound = sound_audio + delay_ms  # Add delay to simulate reverb
        reverb_sound = sound_audio.overlay(delayed_sound, position=delay_ms)

        # Export the reverb sound and load it back into pygame
        reverb_sound.export("temp_reverb.wav", format="wav")
        return pygame.mixer.Sound("temp_reverb.wav")

    def apply_distortion(self, sound, intensity=5):
        """
        Apply distortion effect with a specific intensity.
        This will simulate a distortion effect by increasing the gain.
        """
        sound_path = os.path.join(self.audio_dir, f"{sound}.wav")
        sound_audio = AudioSegment.from_wav(sound_path)

        # Apply distortion effect by increasing the gain
        distorted_sound = sound_audio + (intensity * 3)  # Increase the gain by 3dB for each unit of intensity
        distorted_sound.export("temp_distortion.wav", format="wav")
        
        # Convert pydub AudioSegment back to pygame Sound
        return pygame.mixer.Sound("temp_distortion.wav")