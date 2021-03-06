"""
使用pygame撰寫一個簡單的射擊遊戲
不使用pygame.Sprite，練習物件導向以及事件導向的撰寫
"""

import pygame
from pathlib import Path

from enemy import Enemy
from player import Player
from missile import MyMissile
from explosion import Explosion

parent_path = Path(__file__).parents[1]
image_path = parent_path / "res"
icon_path = image_path / "airplaneIcon.png"

# 初始化pygame系統
pygame.init()
pygame.mixer.init()
# 建立視窗物件，寬、高
screenHigh = 760
screenWidth = 1000
playground = (screenWidth, screenHigh)
screen = pygame.display.set_mode((screenWidth, screenHigh))

# Title, Icon and Background
pygame.display.set_caption("Pygame射擊遊戲")
icon = pygame.image.load(icon_path)     # 載入圖示
pygame.display.set_icon(icon)
background = pygame.Surface(screen.get_size())
background = background.convert()       # 改變pixel format，加快顯示速度
background.fill((50, 50, 50))           # 畫布為鐵黑色(三個參數為RGB)

# 載入音效
parent_path = Path(__file__).parents[1]
image_path = parent_path / "res"
sound_path = image_path / "sound"

bgm = sound_path / "backgroundmusic.MID"
gameOver = sound_path / "gameover.mid"
shoot_sound = sound_path / "shoot.wav"
explosion_sound = sound_path / "explosion.wav"
playerExplosion_sound = sound_path / "playerExplosion.wav"

# 載入地圖
background_image_path = image_path / "picture" / "background.jpg"
background_img = pygame.image.load(background_image_path)
background_img.convert()
background.blit(pygame.transform.scale(background_img, (screenWidth, screenHigh)), (0, 0))

# 載入字體，微軟正黑體
font_name = image_path / "font.ttf"


# 將文字寫入畫面中
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)    # 設定字體及大小
    text_surface = font.render(text, True, (255, 255, 255))     # 繪製
    text_rect = text_surface.get_rect() # 取得矩形
    text_rect.centerx = x   # 取得矩形x
    text_rect.y = y     # 取得矩形y
    surf.blit(text_surface, text_rect)


# 將血條寫入畫面中
def draw_hp(surf, hp, x, y):
    if hp < 0:
        hp = 0
    bar_length = 200    # 矩形長度
    bar_height = 30     # 矩形寬度
    fill = (hp / 50) * bar_length   # 血量百分比
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, (255, 0, 0), fill_rect)  # 紅色血條
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)    # 白色外框


# 載入得分
score = 0

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
if player.available:
    pygame.time.set_timer(createEnemy, 1000)

initial = True
game_over = False
running = True

space_first = 0
space_second = -400

clock = pygame.time.Clock()     # create an object to help track time


# 設定無窮迴圈，讓視窗持續更新與執行
while running:

    # 初始畫面
    if initial:
        pygame.mixer.music.load(bgm)
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)
        pygame.time.delay(100)

        screen.blit(background, (0, 0))
        draw_text(screen, "Pygame射擊遊戲", 80, screenWidth/2, screenHigh/4)
        draw_text(screen, "W,S：上下移動", 30, screenWidth/2, screenHigh/2)
        draw_text(screen, "A,D：左右移動", 30, screenWidth/2, screenHigh/2 + 40)
        draw_text(screen, "空白鍵：發射子彈", 30, screenWidth/2, screenHigh/2 + 80)
        draw_text(screen, "按下任意鍵開始遊戲", 24, screenWidth/2, screenHigh*3/4 + 20)

        pygame.display.update()

        # 載入得分
        score = 0

        waiting = True
        while waiting:
            dt = clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                elif event.type == pygame.KEYUP:
                    initial = False
                    waiting = False
                    print("遊戲開始!")

    # 結束畫面
    if game_over:

        pygame.mixer.music.load(gameOver)
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)
        pygame.time.delay(100)

        game_over_image_path = image_path / "picture" / "gameover.PNG"
        game_over_img = pygame.image.load(game_over_image_path)
        game_over_img.convert()

        game_over_background = pygame.Surface(screen.get_size())
        game_over_background = game_over_background.convert()       # 改變pixel format，加快顯示速度
        game_over_background.fill((50, 50, 50))                     # 畫布為鐵黑色(三個參數為RGB)

        game_over_background.blit(pygame.transform.scale(game_over_img, (screenWidth, screenHigh)), (0, 0))

        screen.blit(game_over_background, (0, 0))
        pygame.display.update()

        # pygame.time.delay(3000)
        draw_text(screen, "Score: %d" % score, 30, screenWidth/2, screenHigh/2 + 100)
        draw_text(screen, "按下任意鍵重新開始", 24, screenWidth/2, screenHigh*3/4 + 20)
        pygame.display.update()

        waiting = True
        Quit = False
        while waiting:
            dt = clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    Quit = True
                elif event.type == pygame.KEYUP:
                    pygame.mixer.music.stop()
                    initial = True
                    game_over = False
                    waiting = False

                    player = Player(playground=playground, sensitivity=movingScale)
                    player.hp = 50
                    Missiles = []
                    Enemies = []
                    Boom = []
        if Quit:
            break
        
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
                space_first = pygame.time.get_ticks()  # 獲取當前時間

                if space_first - space_second >= 400:
                    space_second = space_first
                    shoot = pygame.mixer.Sound(shoot_sound)
                    pygame.mixer.Sound.set_volume(shoot, 0.3)
                    shoot.play()

                    m_x = player.x + 20
                    m_y = player.y
                    Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                    m_x = player.x + 80
                    Missiles.append(MyMissile(playground, (m_x, m_y), movingScale))  # 若未指定參數，需按照宣告順序
                    pygame.time.set_timer(launchMissile, 400)  # 之後，每400 ms發射一組

                # shoot = pygame.mixer.Sound(shoot_sound)
                # pygame.mixer.Sound.set_volume(shoot, 0.3)
                # shoot.play()
                # m_x = player.x + 20
                # m_y = player.y
                # Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                # m_x = player.x + 80
                # Missiles.append(MyMissile(playground, (m_x, m_y), movingScale))  # 若未指定參數，需按照宣告順序
                # pygame.time.set_timer(launchMissile, 400)  # 之後，每400 ms發射一組

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
        if player.hp < 0:
            player.hp = 0
        print("剩餘HP:", player.hp)
        player.collided = False
        score -= 50

    for m in Missiles:
        m.collision_detect(Enemies)

    for e in Enemies:
        if e.collided:
            if player.hp > 0:
                explosion = pygame.mixer.Sound(explosion_sound)
                pygame.mixer.Sound.set_volume(explosion, 0.3)
                explosion.play()
            if player.hp <= 0:
                playerExplosion = pygame.mixer.Sound(playerExplosion_sound)
                pygame.mixer.Sound.set_volume(playerExplosion, 0.3)
                playerExplosion.play()
            Boom.append(Explosion(e.center))
            score += 100

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

    # 爆炸效果在player之上
    Boom = [item for item in Boom if item.available]
    for e in Boom:
        e.update()
        screen.blit(e.image, e.xy)

    if running and not initial:
        draw_text(screen, str(score), 32, screenWidth/2, 10)
        draw_hp(screen, player.hp, screenWidth - 210, screenHigh - 40)
        pygame.display.update()                 # 更新螢幕狀態
        dt = clock.tick(fps)                    # 每秒更新fps次

    if not player.available and not Boom:
        pygame.mixer.music.stop()
        print("HP歸零")
        pygame.time.delay(1000)
        game_over = True

pygame.quit()   # 關閉繪圖視窗
