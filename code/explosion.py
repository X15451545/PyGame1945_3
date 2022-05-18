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
            # 建立爆炸效果圖片序列，這裡只用五張圖
            __parent__path = Path(__file__).parents[1]
            icon_path = __parent__path / "res" / "explosion_small.png"
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent__path / "res" / "explosion_medium.png"
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent__path / "res" / "explosion_large.png"
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent__path / "res" / "explosion_medium.png"
            Explosion.explosion_effect.append(pygame.image.load(icon_path))

        self.__image_index = 0
        self._image = Explosion.explosion_effect[self.__image_index]
        self.__fps_count = 0

    def update(self):
        self.__fps_count += 1
        if self.__fps_count > 30:
            self.__image_index += 1
            if self.__image_index > 4:
                self._available = False
            else:
                self._image = Explosion.explosion_effect[self.__image_index]
