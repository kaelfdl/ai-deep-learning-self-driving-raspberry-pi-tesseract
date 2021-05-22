import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((100,100))

def get_key(key_name):
    flag = False
    for event in pygame.event.get():
        pass
    key_input = pygame.key.get_pressed()
    key = getattr(pygame, 'K_{}'.format(key_input))
    if key_input[key]:
        flag = True
    pygame.display.update()
    return flag

def main():
    if get_key('w'):
        print('Key w was pressed')


if __name__ == '__main__':
    init()
    while(1):
        main()