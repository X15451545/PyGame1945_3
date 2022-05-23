"""
使用pygame撰寫一個簡單的射擊遊戲
不使用pygame.Sprite，練習物件導向以及事件導向的撰寫
"""
import time

import pygame
from pathlib import Path

from enemy import Enemy
from player import Player
from missile import MyMissile
from explosion import Explosion

parent_path = Path(__file__).parents[1]
# print(parent_path)
image_path = parent_path / "res"
# print(image_path)
icon_path = image_path / "airplaneIcon.png"
# print(icon_path)

# 初始化pygame系統
pygame.init()
pygame.mixer.init()
# 建立視窗物件，寬、高
screenHigh = 760
screenWidth = 1000
playground = (screenWidth, screenHigh)
screen = pygame.display.set_mode((screenWidth, screenHigh))

# Title, Icon and Background
pygame.display.set_caption("1942偽")
icon = pygame.image.load(icon_path)     # 載入圖示
pygame.display.set_icon(icon)
background = pygame.Surface(screen.get_size())
background = background.convert()       # 改變pixel format，加快顯示速度
background.fill((50, 50, 50))           # 畫布為鐵黑色(三個參數為RGB)

# 載入音效
parent_path = Path(__file__).parents[1]
image_path = parent_path / "res"
sound_path = image_path / "sound"

BGM = sound_path / "BGM.MID"
shoot_sound = sound_path / "shoot.wav"
explosion_sound = sound_path / "explosion.wav"
heroExplosion_sound = sound_path / "heroExplosion.wav"

# background_image_path = image_path / "mapback.png"
# image = pygame.image.load(background_image_path)
# image.convert()
# background.blit(pygame.transform.scale(image, (screenWidth, screenHigh)), (0, 0))
# background.blit(image, (0, 0))


fps = 120                       # 更新頻率，包含畫面更新與事情更新
movingScale = 600 / fps

player = Player(playground=playground, sensitivity=movingScale)

# 建立物件串列
Missiles = []
Enemies = []
Boom = []

# 建立事件編號
launchMissile = pygame.USEREVENT + 1
createEnemy = pygame.USEREVENT + 2

# 建立敵機，每秒一台
pygame.time.set_timer(createEnemy, 1000)

running = True
clock = pygame.time.Clock()     # create an object to help track time

pygame.mixer.music.load(BGM)
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

# 設定無窮迴圈，讓視窗持續更新與執行
while running:
    # 從pygame事件佇列中，一項一項的檢查

    # 玩家移動方法一
    # ============================================================
    # for event in pygame.event.get():
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_a:  # "a", "A", 左移
    #             player.to_the_left()
    #         if event.key == pygame.K_d:
    #             player.to_the_right()
    #         if event.key == pygame.K_s:
    #             player.to_the_bottom()
    #         if event.key == pygame.K_w:
    #             player.to_the_top()
    #
    #     if event.type == pygame.KEYUP:
    #         if event.key == pygame.K_a or event.key == pygame.K_d:
    #             player.stop_x()
    #         if event.key == pygame.K_s or event.key == pygame.K_w:
    #             player.stop_y()
    #
    #     if event.type == pygame.QUIT:
    #         running = False
    # ============================================================

    # 玩家移動方法二
    # ============================================================
    keyCountX = 0  # 用來計算按鍵被按下的次數，X軸一組
    keyCountY = 0  # 用來計算按鍵被按下的次數，Y軸一組

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:  # "a", "A", 左移
                keyCountX += 1
                player.to_the_left()
            if event.key == pygame.K_d:
                keyCountX += 1
                player.to_the_right()
            if event.key == pygame.K_s:
                keyCountY += 1
                player.to_the_bottom()
            if event.key == pygame.K_w:
                keyCountY += 1
                player.to_the_top()

            if event.key == pygame.K_SPACE:
                shoot = pygame.mixer.Sound(shoot_sound)
                pygame.mixer.Sound.set_volume(shoot, 0.3)
                shoot.play()
                m_x = player.x + 20
                m_y = player.y
                Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                m_x = player.x + 80
                Missiles.append(MyMissile(playground, (m_x, m_y), movingScale))  # 若未指定參數，需按照宣告順序
                pygame.time.set_timer(launchMissile, 400)  # 之後，每400 ms發射一組

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                if keyCountX == 1:
                    keyCountX = 0
                    player.stop_x()
                else:
                    keyCountX -= 1
            if event.key == pygame.K_s or event.key == pygame.K_w:
                if keyCountY == 1:
                    keyCountY = 0
                    player.stop_y()
                else:
                    keyCountY -= 1

            if event.key == pygame.K_SPACE:
                pygame.time.set_timer(launchMissile, 0)  # 停止發射

        # 自動發射飛彈
        if event.type == launchMissile:
            shoot = pygame.mixer.Sound(shoot_sound)
            pygame.mixer.Sound.set_volume(shoot, 0.3)
            shoot.play()
            m_x = player.x + 20
            m_y = player.y
            Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
            m_x = player.x + 80
            Missiles.append(MyMissile(playground, (m_x, m_y), movingScale))  # 若未指定參數，需按照宣告順序
            pygame.time.set_timer(launchMissile, 400)  # 之後，每400 ms發射一組

        if event.type == createEnemy:
            Enemies.append(Enemy(playground=playground, sensitivity=movingScale))

        if event.type == pygame.QUIT:
            running = False
    # ============================================================

    screen.blit(background, (0, 0))         # 更新背景圖片
    player.collision_detect(Enemies)

    if player.collided:
        print("剩餘HP:", player.hp)
        player.collided = False

    for m in Missiles:
        m.collision_detect(Enemies)

    for e in Enemies:
        if e.collided:
            if player.hp > 0:
                explosion = pygame.mixer.Sound(explosion_sound)
                pygame.mixer.Sound.set_volume(explosion, 0.3)
                explosion.play()
            if player.hp <= 0:
                heroExplosion = pygame.mixer.Sound(heroExplosion_sound)
                pygame.mixer.Sound.set_volume(heroExplosion, 0.3)
                heroExplosion.play()
            Boom.append(Explosion(e.center))

    Missiles = [item for item in Missiles if item.available]
    for m in Missiles:
        m.update()
        screen.blit(m.image, m.xy)

    Enemies = [item for item in Enemies if item.available]
    for e in Enemies:
        e.update()
        screen.blit(e.image, e.xy)

    if player.hp > 0:
        player.update()                         # 更新player狀態
        screen.blit(player.image, player.xy)    # 添加player圖片

    if player.hp <= 0:
        player.available = False
        print("HP歸零")

    # player.update()                         # 更新player狀態
    # screen.blit(player.image, player.xy)    # 添加player圖片

    # 爆炸效果在player之上
    Boom = [item for item in Boom if item.available]
    for e in Boom:
        e.update()
        screen.blit(e.image, e.xy)

    pygame.display.update()                 # 更新螢幕狀態
    dt = clock.tick(fps)                    # 每秒更新fps次

    if not player.available:
        time.sleep(2)
        running = False

pygame.quit()   # 關閉繪圖視窗
