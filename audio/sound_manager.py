import pygame

class SoundManager:
    def __init__(self, sound_dir):
        pygame.mixer.init()
        self.sounds = {
            "A4": pygame.mixer.Sound(f"{sound_dir}/A4.wav"),  # 低音
            "B4": pygame.mixer.Sound(f"{sound_dir}/B4.wav"),  # 中音
            "C5": pygame.mixer.Sound(f"{sound_dir}/C5.wav")   # 高音
        }

    def play_sound(self, note):
        """
        播放指定音符。
        :param note: 音符名称 (如 'A4', 'B4', 'C5')
        """
        if note in self.sounds:
            self.sounds[note].play()

    def play_based_on_price(self, current_price, previous_price):
        """
        根据价格变化播放音符：
        - 高于前一次价格，播放高音 C5
        - 等于前一次价格，播放中音 B4
        - 低于前一次价格，播放低音 A4
        :param current_price: 当前价格
        :param previous_price: 前一次价格
        """
        if current_price > previous_price:
            self.play_sound("C5")  # 高音
        elif current_price < previous_price:
            self.play_sound("A4")  # 低音
        else:
            self.play_sound("B4")  # 中音
