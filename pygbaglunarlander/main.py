# from strategys.taxi_v3 import *
# from strategys.super_mario_bros.mario_gui import *
# from gym_super_mario_bros._app.cli import main


# if __name__ == "__main__":
#     main()
# asyncio.run(main())
import asyncio
import pygame
import gymnasium as gym
import pygame.ftfont
import Box2D
import pygbag
pygame.init()
pygame.ftfont.init()
WIDTH = 500
HEIGHT = 800
fps = 60
timer = pygame.time.Clock()

# ----------------------------------------------------------
GAME = 'LunarLander-v2'
KEY_MAP = [(-1, pygame.K_RETURN), (0, pygame.K_UP), (1, pygame.K_RIGHT), (2, pygame.K_DOWN), (3, pygame.K_LEFT)]
DESC = {
    'rule': """慢速，正确挺在两旗杆中为胜""",
    'action': '上: 无动作； 下： 下喷气 左： 左喷气 右： 右喷气'
}


def judge_win(reward):
    if reward > 0:
        return True
    if reward < 0:
        return False
# ----------------------------------------------------------


KEY_ACTIONS = {k: a for a, k in KEY_MAP}
huge_font = pygame.font.Font(None, 42)
font = pygame.font.Font(None, 24)
LOSS_TEXT = huge_font.render("You Lost!", True, "blue")
WIN_TEXT = huge_font.render("You Win!", True, "blue")
RESTART_TEXT = font.render("Game Over: Press Enter to Restart", True, "blue")


async def main():
    env = gym.make(GAME, render_mode='human')
    env.clock = pygame.time.Clock()
    fps = 60
    env.reset()
    env.render()
    run = True
    game_over = False
    while run:
        env.clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                action = KEY_ACTIONS.get(event.key)
                if action == -1:
                    if game_over:
                        game_over = False
                        env.reset()
                elif action is not None:
                    if not game_over:
                        next_state, reward, game_over, truncated, info = env.step(action)
        if game_over:
            game_res = judge_win(reward)
            env.screen.blit(WIN_TEXT if game_res else LOSS_TEXT, (160, 220))
            env.screen.blit(RESTART_TEXT, (160, 280))
        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())

