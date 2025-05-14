import pygame
from settings import SOUNDS_PATH, SOUND_SETTINGS, DEFAULT_VOLUME, MUSIC_VOLUME
import os

class SoundManager:
    def __init__(self):
        """Khởi tạo Sound Manager"""
        self.sounds = {}
        self.is_sound_enabled = True
        self.is_music_enabled = True
        self.load_sounds()
        
    def load_sounds(self):
        """Load tất cả âm thanh"""
        for key, filename in SOUND_SETTINGS.items():
            full_path = os.path.join(SOUNDS_PATH, filename)
            try:
                if "BACKGROUND" in key:
                    # Background music được load riêng
                    if key == "BACKGROUND":
                        self.background_music = full_path
                    elif key == "MENU_BACKGROUND":
                        self.menu_background_music = full_path
                else:
                    sound = pygame.mixer.Sound(full_path)
                    sound.set_volume(DEFAULT_VOLUME)
                    self.sounds[key] = sound
            except Exception as e:
                print(f"Không thể tải âm thanh {filename}: {str(e)}")
                
    def reload_sound_effects(self):
        """Reload và thiết lập lại âm lượng cho các sound effect"""
        # Lưu lại các key hiện có
        current_keys = list(self.sounds.keys())
        
        # Xóa tất cả sound effects hiện tại
        for key in current_keys:
            self.sounds[key].stop()
            del self.sounds[key]
            
        # Load lại các sound effects
        for key, filename in SOUND_SETTINGS.items():
            if "BACKGROUND" not in key:
                full_path = os.path.join(SOUNDS_PATH, filename)
                try:
                    sound = pygame.mixer.Sound(full_path)
                    sound.set_volume(DEFAULT_VOLUME)
                    self.sounds[key] = sound
                except Exception as e:
                    print(f"Không thể tải lại âm thanh {filename}: {str(e)}")
                
    def play_sound(self, sound_key):
        """Phát âm thanh effect"""
        if self.is_sound_enabled and sound_key in self.sounds:
            try:
                self.sounds[sound_key].play()
            except Exception as e:
                print(f"Không thể phát âm thanh {sound_key}: {str(e)}")
            
    def play_background(self, music_type="BACKGROUND"):
        """Phát nhạc nền"""
        if not self.is_music_enabled:
            return
            
        try:
            # Tạm dừng nhạc hiện tại
            pygame.mixer.music.stop()
            
            # Load và phát nhạc mới
            if music_type == "BACKGROUND" and hasattr(self, 'background_music'):
                pygame.mixer.music.load(self.background_music)
            elif music_type == "MENU_BACKGROUND" and hasattr(self, 'menu_background_music'):
                pygame.mixer.music.load(self.menu_background_music)
            else:
                return
                
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)  # -1 để loop vô hạn
            
            # Đảm bảo các âm thanh effect vẫn hoạt động
            for sound in self.sounds.values():
                sound.set_volume(DEFAULT_VOLUME)
                
        except Exception as e:
            print(f"Không thể phát nhạc nền {music_type}: {str(e)}")
                
    def stop_background(self):
        """Dừng nhạc nền"""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Không thể dừng nhạc nền: {str(e)}")
        
    def toggle_sound(self):
        """Bật/tắt âm thanh effect"""
        self.is_sound_enabled = not self.is_sound_enabled
        
    def toggle_music(self):
        """Bật/tắt nhạc nền"""
        self.is_music_enabled = not self.is_music_enabled
        if self.is_music_enabled:
            self.play_background()
        else:
            self.stop_background()
