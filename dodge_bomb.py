import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1200, 700
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横線方向判定結果, 縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def tra_img() -> dict:
    KK_DICT = {
        (0, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0),
        (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0),
        (-5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 2.0),
        (0, -5): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 270, 2.0), True, False),
        (+5, -5): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 2.0), True, False),
        (+5, 0): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 180, 2.0), False, True),
        (+5, +5): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 225, 2.0), False, True),
        (0, +5): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 2.0), True, False),
        (-5, +5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0),
    }
    return KK_DICT


def min(tmr, max):
    if tmr < max:
        return tmr
    else:
        return max


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bomb = pg.Surface((20, 20))
    pg.draw.circle(bomb, (255, 0, 0), (10, 10), 10)
    bomb.set_colorkey((0, 0, 0)) 
    bomb_rct = bomb.get_rect()
    bomb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    img_dict = tra_img()
    accs = [a for a in range(1, 11)]
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        # if kk_rct.colliderect(bomb_rct):  # 衝突判定
        #     return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        sum_mv = tuple(sum_mv)
        kk_img = img_dict[sum_mv]
        screen.blit(kk_img, kk_rct)
        bomb_rct.move_ip(vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)])
        yoko, tate = check_bound(bomb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bomb, bomb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
