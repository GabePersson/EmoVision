import os
import pandas as pd
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class MusicPlayerThread:
    def __init__(self):
        self.music_list = None
        self.player = QMediaPlayer()
        self.music_path = None
        self.init = False

    def updateMusicList(self, music_str):
        music_str = music_str.replace('"', '')
        self.music_list = [theStr for theStr in music_str]

    def run(self):
        self.get_music()
        self.init = True
        if self.music_path is not None:
            media = QMediaContent(QUrl.fromLocalFile(self.music_path))
            self.player.setMedia(media)
            self.player.play()

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
            # 根据数组中的名称播放音乐，需要将名称做转化，转化为“忧”，“喜”，“怒”，“恐”，“惊”，“思”（注意！！！！原来的无情绪，neutra对应的是思“
            input_name = self.music_list[0]
            # 假设通过根路径检索音乐，这里支持两种方法，哪种都可以，下附了一个excel的调用，excel可能需要重新改动路径，也许根路径法会更好！
            self.music_path = self.music_lookup_from_root("Srcs/music/music_files", input_name)

        elif len(self.music_list) == 2:
            # 将两个元素组合起来，作为检索输入
            input_name = "".join(self.music_list)
            # 通过Excel文件检索音乐
            self.music_path = self.music_lookup_from_excel("Srcs/music/locate.xlsx", input_name)

    def stop(self):
        self.player.stop()


