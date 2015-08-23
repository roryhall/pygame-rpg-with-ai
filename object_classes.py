import pygame
from tileC import Tile
from random import randint 

class Character(pygame.Rect):

    width, height = 32, 32

    def __init__(self, x, y):

        self.tx, self.ty = None, None
        pygame.Rect.__init__(self, x, y, Character.width, Character.height)

    def __str__(self):
        return str(self.get_number())

    def set_target(self, next_tile): # Sets the target tile the character is moving to
        if self.tx == None and self.ty == None:
            self.tx = next_tile.x
            self.ty = next_tile.y

    def get_number(self):
        
        return ((self.x / self.width) + Tile.H) + ((self.y / self.height) * Tile.V)

    def get_tile(self):

        return Tile.get_tile(self.get_number())

    def rotate(self, direction, img):

        if direction == 'n':
            if self.direction != 'n': # only do this if the charater is heading this direction
                self.direction = 'n'
                
                self.img = img

        if direction == 's':
            if self.direction != 's':
                self.direction = 's'
                self.img = img

        if direction == 'e':
            if self.direction != 'e':
                self.direction = 'e'
                self.img = img

        if direction == 'w':
            if self.direction != 'w':
                self.direction = 'w'
                self.img = img

class Zombie(Character):

    List = []
    spawn_tiles = (316, 148)
    
    zombie_s = pygame.image.load('images/zombie_front.png')
    zombie_n = pygame.image.load('images/zombie_back.png')
    zombie_e = pygame.image.load('images/zombie_right.png')
    zombie_w = pygame.image.load('images/zombie_left.png')
    
    health = 100

    def __init__(self, x, y):

        self.direction = 'w'
        self.img = Zombie.zombie_w
        self.health = Zombie.health
        
        Character.__init__(self, x, y)
        
        Zombie.List.append(self) # add every zombie that is instanciated

    @staticmethod
    def update(screen):
        for zombie in Zombie.List:
            screen.blit(zombie.img, (zombie.x, zombie.y))

            if zombie.health <=0:
                Zombie.List.remove(zombie)

            if zombie.tx != None and zombie.ty != None: # Target is set

                X = zombie.x - zombie.tx
                Y = zombie.y - zombie.ty

                vel = 2
                if X < 0: # ---> Right (East)
                    zombie.x += vel
                    zombie.rotate('e', Zombie.zombie_e)

                elif X > 0: # <---- Left (West)
                    zombie.x -= vel
                    zombie.rotate('w', Zombie.zombie_w)

                if Y > 0: # up
                    zombie.y -= vel
                    zombie.rotate('n', Zombie.zombie_n)

                elif Y < 0: # down
                    zombie.y += vel
                    zombie.rotate('s', Zombie.zombie_s)

                if X == 0 and Y == 0:
                    zombie.tx, zombie.ty = None, None
 
    @staticmethod
    def spawn(total_frames, FPS):
        if total_frames % (FPS) == 0: 
            if total_frames % (FPS * 48) == 0: # higher the multiplying value to slow the zombie spawn rate
                
                r  = randint(0, 2)
                sounds = [pygame.mixer.Sound('audio/zs1.ogg'),
                          pygame.mixer.Sound('audio/zs2.ogg'),
                          pygame.mixer.Sound('audio/zs2.ogg')
                          ]
                sounds = sounds[r]
                sounds.play()
            
                r = randint(0, len(Zombie.spawn_tiles) - 1) # pick a randon spawn tile
                tile_num = Zombie.spawn_tiles[r]
                spawn_node = Tile.get_tile(tile_num)
                Zombie(spawn_node.x, spawn_node.y)


class Survivor(Character):

    weapons_img = [pygame.image.load('images/automatic.png'),
               pygame.image.load('images/shotgun.png')]
    

    def __init__(self, x, y):

        self.current_weapon = 0 # 0 = automatic , 1 = shotgun
        self.direction = 'w'
        self.img = pygame.image.load('images/survivor_w.png')

        Character.__init__(self, x, y)
        
    def get_bullet_type(self):
        if self.current_weapon == 0:
            return 'automatic'

        elif self.current_weapon == 1:
            return 'shotgun'

        
    def movement(self):

        if self.tx != None and self.ty != None: # Target is set if it isn't moving don't do anything

            X = self.x - self.tx
            Y = self.y - self.ty

            vel = 8

            if X < 0: # --->
                self.x += vel
            elif X > 0: # <----
                self.x -= vel

            if Y > 0: # up
                self.y -= vel
            elif Y < 0: # down
                self.y += vel

            if X == 0 and Y == 0:
                self.tx, self.ty = None, None

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

        half = self.width/2
        weapon_img = Survivor.weapons_img[self.current_weapon]
        
        if self.direction == 'w':
            screen.blit(weapon_img, (self.x, self.y + half))
            
        elif self.direction == 'e':
            weapon_img = pygame.transform.flip(weapon_img, True, False)
            screen.blit(weapon_img, (self.x + half, self.y + half))           

        elif self.direction == 's':
            weapon_img = pygame.transform.rotate(weapon_img, 90) # CCW
            screen.blit(weapon_img, (self.x + half, self.y + half))
            
        elif self.direction == 'n':
            south = pygame.transform.rotate(weapon_img, 90)
            weapon_img = pygame.transform.flip(south, False, True)
            screen.blit(weapon_img, (self.x + half, self.y - half))
            

    def rotate(self, direction):

        path = 'images/survivor_'
        png = '.png'

        if direction == 'n':
            if self.direction != 'n':
                self.direction = 'n'
                self.img = pygame.image.load(path + self.direction + png)

        if direction == 's':
            if self.direction != 's':
                self.direction = 's'
                self.img = pygame.image.load(path + self.direction + png)

        if direction == 'e':
            if self.direction != 'e':
                self.direction = 'e'
                self.img = pygame.image.load(path + self.direction + png)

        if direction == 'w':
            if self.direction != 'w':
                self.direction = 'w'
                self.img = pygame.image.load(path + self.direction + png)


class Bullet (pygame.Rect):

    width, height = 7, 10
    List = []

    bullet_img = {'shotgun': pygame.image.load('images/shotgun_b.png'),
                  'automatic': pygame.image.load('images/automatic_b.png')
                  }

    weapons_damage = {'shotgun': (Zombie.health/2) + 1,
                      'automatic': (Zombie.health/6) + 1
                      }

    def __init__(self, x, y, velx, vely, direction, type_):



        if type_ == 'shotgun':
            try:
                dx = abs(Bullet.List[-1].x - x)
                dy = abs(Bullet.List[-1].y - y)

                if dx < 50 and dy < 50 and type_ == 'shotgun':
                    return                
            except:
                pass

        self.type = type_
        self.direction = direction
        self.velx = velx
        self.vely = vely

        if direction == 'n':
            south = pygame.transform.rotate(Bullet.bullet_img[type_], 90) # CCW
            self.img = pygame.transform.flip(south, False, True)

        if direction == 's':
            self.img = pygame.transform.rotate(Bullet.bullet_img[type_], 90) # CCW

        if direction == 'e':
            self.img = pygame.transform.flip(Bullet.bullet_img[type_], True, False)

        if direction == 'w':
            self.img = Bullet.bullet_img[type_]
            
        pygame.Rect.__init__(self, x, y, Bullet.width, Bullet.height)
        Bullet.List.append(self)


    def off_screen (self, screen):

        if self.x < 0:
            return True
        elif self.y < 0:
            return True
        elif self.x + self.width > screen.get_width():
            return True        
        elif self.y + self.height > screen.get_height():
            return True
        return False
        
    @staticmethod
    def super_massive_jumbo_loop(screen):

        for bullet in Bullet.List:

            bullet.x += bullet.velx
            bullet.y += bullet.vely
            screen.blit(bullet.img, (bullet.x, bullet.y))

            if bullet.off_screen(screen):
                Bullet.List.remove(bullet)
                continue

            for zombie in Zombie.List:
                if bullet.colliderect(zombie):
                    zombie.health -= Bullet.weapons_damage[bullet.type]
                    Bullet.List.remove(bullet)
                    break
                
            for tile in Tile.List:
                if bullet.colliderect(tile) and not(tile.walkable):
                    try:
                        Bullet.List.remove(bullet)
                    except:
                        pass # bullet not in list
                
        









