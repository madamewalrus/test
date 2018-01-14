import pygame
import random
import sys


screen_width = 640
screen_height = 480
screen_size = screen_width, screen_height

screen = None



def write_text(screen, text, color, big):
    if big:
        height = screen.get_height()/5
        up = screen.get_height()/2
    else:
        height = screen.get_height()/12
        up = screen.get_height()-(screen.get_height()/24)

    font = pygame.font.Font(None, height)
    rend = font.render(text, 1, color)
    textpos = rend.get_rect(
        centerx = screen.get_width()/2,
        centery = up
    )

    screen.blit(rend, textpos)

def timed_wait(time_to_wait,event_types_that_cancel):
    """
    Wait for time_to_wait, but cancel if the relevent event happens.  
    Return True if cancelled or false if we waited the full time.
    """

    finished_waiting_event_id = pygame.USEREVENT + 1
    pygame.time.set_timer(finished_waiting_event_id,time_to_wait)

    pygame.event.clear()

    pressed = False
    waiting = True
    while waiting:
        evt = pygame.event.wait()
        if is_quit(evt):
            quit()
	elif evt.type in event_types_that_cancel:
	    waiting = False
	    pressed = True
	elif evt.type == finished_waiting_event_id:
	    waiting = False

    pygame.time.set_timer(finished_waiting_event_id, 0)

    return pressed

def start():
    global screen
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    

def quit():
    pygame.quit()
    sys.exit()

def ready_screen():
    white = pygame.Color("white")
    write_text(screen, "Ready?", white, True)
    pygame.display.flip()

def wait():
    time_to_wait = random.randint(1500,3000) #Between 1.5 and 3 seconds
    pygame.time.wait(time_to_wait) # Note bug: can't quit during this time


def is_quit(evt):
    return (
        evt.type == pygame.QUIT or
        (
            evt.type == pygame.KEYDOWN and
            evt.key == pygame.K_ESCAPE
         )
    )

def shape_wait():
    """
    wait while we display a shape.  Return True if a key was 
    pressed or false otherwise
    """
    press_events = pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN
    return timed_wait(2000, press_events) #2 seconds


def tick():
    colour = pygame.Color("green")
    w = screen.get_width()/2
    h = screen.get_height()/4
    points = (
        (w-w/5,h-h/9),
        (w,    h+h/5),
        (w+w/3,h-h/3)
    )

    screen.fill(pygame.Color("black"))
    pygame.draw.lines(screen, colour, False, points, 20)
    

def cross():
    colour = pygame.Color("red")
    w = screen.get_width()/2
    h = screen.get_height()/4
    left   = w - w/3
    right  = w + w/3
    top    = h - h/3
    bottom = h + h/3

    start1 = left, top
    end1   = right, bottom

    start2 = left, bottom
    end2   = right, top

    screen.fill(pygame.Color("black"))
    pygame.draw.line(screen, colour, start1, end1, 20)
    pygame.draw.line(screen, colour, start2, end2, 20)
    




def green_success():
    tick()
    green = pygame.Color("green")
    white = pygame.Color("white")
    write_text(screen, "Well Done!", green, True)
    write_text(screen, "You pressed on green!", white, False)
    pygame.display.flip()
    pygame.time.wait(2000) #can't quit

def green_failure():
    cross()
    red = pygame.Color("red")
    white = pygame.Color("white")
    write_text(screen, "Bad Luck!", red, True)
    write_text(screen, "Green means press something!", white, False)
    pygame.display.flip()
    pygame.time.wait(2000) #can't quit

def red_success():
    tick()
    green = pygame.Color("green")
    white = pygame.Color("white")
    write_text(screen, "Well Done!", green, True)
    write_text(screen, "You didn't press on red!", white, False)
    pygame.display.flip()
    pygame.time.wait(2000) #can't quit

def red_failure():
    cross()
    red = pygame.Color("red")
    white = pygame.Color("white")
    write_text(screen, "Bad Luck!", red, True)
    write_text(screen, "Red means don't press!", white, False)
    pygame.display.flip()
    pygame.time.wait(2000) #can't quit

def green_shape():
    green = pygame.Color("green")
    centre = (screen.get_width()/2, screen.get_height()/2)
    radius = screen.get_width()/3

    screen.fill(pygame.Color("white"))
    pygame.draw.circle(screen,green,centre,radius, 0)

    write_text(screen, "Press Something!", pygame.Color("black"), False)

    pygame.display.flip()

    pressed = shape_wait()

    if pressed:
        green_success()
    else:
        green_failure()

def red_shape():
    red = pygame.Color("red")
    height = 2*(screen.get_height()/3)
    left = (screen.get_width()/2)-(height/2)
    top = screen.get_height()/6

    screen.fill(pygame.Color("white"))
    pygame.draw.rect(screen,red,(left, top, height, height), 0)

    write_text(screen, "Don't Press!", pygame.Color("black"), False)

    pygame.display.flip()

    pressed = shape_wait()

    if pressed:
        red_failure()
    else:
        red_success()


def shape():
    GREEN = 0
    RED   = 1
    shape = random.choice([GREEN, RED])
    
    if shape == GREEN:
        green_shape()
    else:
        red_shape()

def end():
    screen.fill(pygame.Color("black"))
    white = pygame.Color("white")
    write_text(screen, "Thanks for Playing!",white,True)
    write_text(screen, "Press a key to exit",white,False)
    pygame.display.flip()

    pygame.event.clear()
    event_types_that_cancel = pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN
    waiting = True
    while waiting:
        evt = pygame.event.wait()
        if evt.type == pygame.QUIT:
            quit()
        elif evt.type in event_types_that_cancel:
            waiting = False
           

start()

ready_screen()

wait()

shape()

end()