
import pygame
import sys
import random
pygame.init()
width=600
height=600
flying=False
gameOver=False

screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("FlappyBird")
background=pygame.image.load("images/bg.png")
background=pygame.transform.scale(background,(600,600))
ground=pygame.image.load("images/ground.png")
ground_scroll=0
scroll_speed=3
clock=pygame.time.Clock()
fps=30 #(frame per second)
pipe_frequency=5000
last_pipe=pygame.time.get_ticks()
score=0
pass_pipe=False
font=pygame.font.SysFont('helvetica',40)
button_img=pygame.image.load("images/restart.png")

def reset_game():
    pipe_group.empty()
    flappy.rect.x=100
    flappy.rect.y=height//2
    score=0
    return score


class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)

    def draw(self):
        action=False
        screen.blit(self.image,(self.rect.x,self.rect.y))
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                action=True

        return action



button=Button(width//2,50,button_img)



def draw_score(text,font,color,x,y):
    img=font.render(text,1,color)
    screen.blit(img,(x,y))



class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position): #constructor function
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("images/pipe.png")
        self.rect=self.image.get_rect()  #rectangle around pipe images
        if position==1:
            self.image=pygame.transform.flip(self.image,False,True) #true in y axis - horizontaly
            self.rect.bottomleft=[x,y-random.randint(50,150)]
        if position==-1:
            self.rect.topleft=[x,y]

    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right<0:
            self.kill()


pipe_group=pygame.sprite.Group()




class Bird(pygame.sprite.Sprite): #sprite class has in built functions like draw and update
    def __init__(self,x,y): #constructer function - called by default, something that will happen
        self.images=[]
        self.index=0
        self.counter=0
        self.vel=0
        self.clicked=False
        pygame.sprite.Sprite.__init__(self) #mandatory line because it calls the draw and update functions so that we do not have to write them seperaterly
        for i in range(1,4):
            image=pygame.image.load(f"images/bird{i}.png")
            self.images.append(image)
        self.image=self.images[self.index]
        self.rect=self.image.get_rect() #cannot move an image by itslef, a rectangle around it does.
        self.rect.center=[x,y]

    def update(self):
        if flying==True:
            self.vel+=0.5
            if self.vel>5:
                self.vel=5
            if self.rect.bottom<450:
                self.rect.y+=self.vel
        if gameOver==False:
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False: #checks if it is a left
                self.vel-=5
                self.clicked=True
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked=False

            flap_cool=5
            self.counter+=1
            if self.counter>flap_cool:
                self.index+=1
                self.counter=0
                if self.index>=len(self.images):
                    self.index=0
            self.image=self.images[self.index]
            self.image=pygame.transform.rotate(self.images[self.index],self.vel*-1)
        else:
            self.image=pygame.transform.rotate(self.images[self.index],-90)





bird_group=pygame.sprite.Group() # so that we can refer to all three bird images at once (whole group of birds as they are in the same place)
flappy=Bird(100,height/2)
bird_group.add(flappy)


while True:
    clock.tick(fps)
    screen.blit(background,(0,0))
    pipe_group.draw(screen)

    screen.blit(ground,(ground_scroll,450))



    if len(pipe_group)>0:
        if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right and pass_pipe==False:
            pass_pipe=True

        if pass_pipe==True:
            if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.right:
                score=score+1
                pass_pipe=False

    draw_score(str(score),font,"red",40,40)




    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.y<0:
        gameOver=True



    if gameOver==False and flying==True:

        time_now=pygame.time.get_ticks()
        if time_now-last_pipe>pipe_frequency:
            pipe_height=random.randint(-100,100)
            btm_pipe=Pipe(width,height//2+pipe_height,-1)
            top_pipe=Pipe(width,height//2+pipe_height,1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now
        pipe_group.update()




        ground_scroll-=scroll_speed
        if abs(ground_scroll)>100:  #absolute converts negative value to positive value
            ground_scroll=0

    bird_group.draw(screen)
    bird_group.update()

    if flappy.rect.bottom>=450:
        gameOver=True
        flying=False

    if gameOver==True:
        if button.draw()==True:
            gameOver=False
            score=reset_game()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()

        if event.type==pygame.MOUSEBUTTONDOWN and flying==False:
            flying=True

    pygame.display.update()

