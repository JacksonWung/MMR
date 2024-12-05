import pygame

class SoundManager:
    def __init__(self, sound_dir):
        pygame.mixer.init()
        self.notes = [
            "D3", "E3", "F3", "G3", "A3", "B3",  # 下八度
            "C4", "D4", "E4", "F4", "G4", "A4", "B4"  # 中央八度
        ]
        self.sounds = {note: pygame.mixer.Sound(f"{sound_dir}/{note}.wav") for note in self.notes}
        
        self.drums = {
            "normal": pygame.mixer.Sound(f"{sound_dir}/gain_drum.mp3"),
            "gain": pygame.mixer.Sound(f"{sound_dir}/money.mp3"),
            "loss": pygame.mixer.Sound(f"{sound_dir}/loss_drum.wav")
        }
        self.current_drum = None
        self.current_state = None  # 记录当前播放的状态
        self.previous_note = None
        self.current_note = None

        # 设置初始音量
        for sound in self.sounds.values():
            sound.set_volume(0.8)  # 增大音符音量
        for drum in self.drums.values():
            drum.set_volume(0.5)  # 降低背景音乐音量


    def play_sound(self, note):
        """
        播放指定音符。
        """
        if note in self.sounds:
            self.sounds[note].play()
            self.previous_note = self.current_note
            self.current_note = self.notes.index(note)  # 根据音符索引判断趋势


    def play_drum(self, drum_type):
        """
        播放指定类型的背景音乐。
        """

        if self.current_state == drum_type:
            # 当前状态未变化，保持当前音乐播放
            return
        
        if self.current_drum:
            self.current_drum.fadeout(1000)  # 1 秒内淡出当前音频

        if drum_type in self.drums:
            self.current_drum = self.drums[drum_type]
            self.current_drum.play(loops=-1, fade_ms=1000)  # 1 秒淡入新音频
            self.current_state = drum_type  # 更新状态


    def get_note_by_price_change(self, current_price, next_price):
        """
        根据价格变化计算对应的音符。
        - 不变：播放 C4
        - 每上涨 0.5%：音符升高一个
        - 每下降 0.5%：音符降低一个
        """
        if current_price == 0:  # 防止除以 0
            return "C4"
        
        # 计算价格变化的百分比
        price_change = (next_price - current_price) / current_price
        step = round(price_change / 0.005)  # 每 0.5% 升降一个音符
        
        # C4 的索引位置
        c4_index = self.notes.index("C4")
        target_index = c4_index + step

        # 确保音符在范围内
        target_index = max(0, min(len(self.notes) - 1, target_index))
        return self.notes[target_index]

    def play_based_on_price(self, current_price, next_price):
        """
        播放对应价格变化的音符。
        """
        note = self.get_note_by_price_change(current_price, next_price)
        self.play_sound(note)

    def is_rising(self):
        if self.previous_note is not None and self.current_note is not None:
            return self.current_note > self.previous_note
        return False
