import os
import pandas as pd
import pygame

pygame.mixer.init()

class MusicPlayer:
    def __init__(self):
        self.music_list = None
        self.music_path = None

    def update_music_list(self, music_str):
        music_str = music_str.replace('"', '')
        self.music_list = [theStr for theStr in music_str]

    def run(self):
        self.get_music()
        if self.music_path is not None:

            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play()

    def music_lookup_from_root(self, root_path, input_name):
        music_path = os.path.join(root_path, input_name + ".mp3")
        if os.path.exists(music_path):
            return music_path
        else:
            print(f"未找到音乐文件: {music_path}")
            return None

    def music_lookup_from_excel(self, excel_file, input_name):
        df = pd.read_excel(excel_file, header=None)
        other_input = input_name[::-1]
        matchA = df[df[0] == input_name]
        matchB = df[df[0] == other_input]
        if not matchA.empty or not matchB.empty:
            if matchA.empty:
                music_path = matchB.iloc[0, 1]
            else:
                music_path = matchA.iloc[0, 1]
            return music_path
        else:
            print(f"未找到匹配的音乐: {input_name}")
            return None

    def get_music(self):
        if len(self.music_list) == 1:
            input_name = self.music_list[0]
            self.music_path = self.music_lookup_from_root("Srcs/music/music_files", input_name)

        elif len(self.music_list) == 2:
            input_name = "".join(self.music_list)
            self.music_path = self.music_lookup_from_excel("Srcs/music/locate.xlsx", input_name)

if __name__ == "__main__":
    player = MusicPlayer()
    player.update_music_list('["song_name"]')  # 替换为你的歌曲名称
    player.run()
