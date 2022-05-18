from pathlib import Path
import random
import pygame.image
from GameObject import GameObject


# 爆炸類別
class Explosion(GameObject):
    # 全域、靜態變數
    explosion_effect = []

    # 建構式
    def __init__(self, xy=None):
        GameObject.__init__(self)
        if xy is None:
            self._x = random.randint(10, self._playground[0] - 100)
            self._y = -100
        else:
            self._x = xy[0]  # 座標屬性
            self._y = xy[1]

        if Explosion.explosion_effect:
            pass
        else:
            # 建立爆炸效果圖片序列
            __parent__path = Path(__file__).parents[1]
            icon_path = __parent__path / "res" / "picture" / "bomb_enemy_0.png"
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent__path / "res" / "picture" / "bomb_enemy_1.png"
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent__path / "res" / "picture" / "bomb_enemy_2.png"
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent__path / "res" / "picture" / "bomb_enemy_3.png"
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent__path / "res" / "picture" / "bomb_enemy_4.png"
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent__path / "res" / "picture" / "bomb_enemy_5.png"
            Explosion.explosion_effect.append(pygame.image.load(icon_path))

        self.__image_index = 0
        self._image = Explosion.explosion_effect[self.__image_index]
        self._frame_rate = 90  # 設定爆炸圖片顯示的間隔時間
        self._last_update = pygame.time.get_ticks()  # 獲取最近刷新時間

    def update(self):
        now = pygame.time.get_ticks()  # 獲取當前時間
        if now - self._last_update > self._frame_rate:  # 當與上一張圖的時間差達到frame_rate時，顯示下一張爆炸圖片
            self._last_update = now  # 紀錄最近刷新時間
            self.__image_index += 1  # 幀數+1，這樣下次才會調用下一張照片
            if self.__image_index == 6:  # 當爆炸圖片達到最後一張時判定為失效
                self._available = False
            else:
                self._image = Explosion.explosion_effect[self.__image_index]
