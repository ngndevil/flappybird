import pygame, sys, random
from pygame import mixer

def draw_floor():
	screen.blit(floor, (floor_x, 600))
	screen.blit(floor, (floor_x + 432, 600))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (450, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midtop = (450, random_pipe_pos - 700))
	return bottom_pipe, top_pipe

def move_pipe(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	return pipes

def draw_pipe(pipes):
	for pipe in pipes:
		if pipe.bottom >= 600:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)

def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			hit_sound.play()
			return False
	if bird_rect.top <= -75 or bird_rect.bottom >= 600:
			swooshing_sound.play()
			return False
	return True

def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1, -bird_move * 3, 1)
	return new_bird

def bird_animation():
	new_bird = bird_list[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
	return new_bird, new_bird_rect

def score_display(game_state):
	if game_state == 'main game':
		score_surface = game_font.render(str(int(score)), True, WHITE)
		score_rect = score_surface.get_rect(center = (197.5, 100))
		screen.blit(score_surface, score_rect)
	if game_state == 'game over':
		score_surface = game_font.render(f'Score: {int(score)}', True, WHITE)
		score_rect = score_surface.get_rect(center = (197.5, 100))
		screen.blit(score_surface, score_rect)

		high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, WHITE)
		high_score_rect = high_score_surface.get_rect(center = (197.5, 570))
		screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

# Intialize the pygame
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

# Create screen
screen = pygame.display.set_mode((395, 702))

# Intialize Frame Rate
clock = pygame.time.Clock()

# Background
background = pygame.image.load('img/background.png').convert()

# Sound
# mixer.music.load("background.wav")
# mixer.music.play(-1)

# Floor
floor = pygame.image.load('img/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x = 0

# Bird
bird_up = pygame.transform.scale2x(pygame.image.load('img/birdup.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('img/birdmid.png').convert_alpha())
bird_down = pygame.transform.scale2x(pygame.image.load('img/birddown.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up] # 0 1 2
bird_index = 0
bird = bird_list[bird_index]
# bird = pygame.image.load('birdmid.png').convert()
# bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100, 351))

# Create timer for bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

# Pipe
pipe_surface = pygame.image.load('img/pipe.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# Create timer for pipe
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1300)
pipe_height = [200, 225, 250, 275, 300, 325, 350]

# Caption and Icon
pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

game_font = pygame.font.Font('04B_19.ttf', 40)

# Create game over screen
game_over_surface = pygame.transform.scale2x(pygame.image.load('img/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (197.5, 351))

# Add sound
flap_sound = pygame.mixer.Sound('sound/wing.wav')
hit_sound = pygame.mixer.Sound('sound/hit.wav')
point_sound = pygame.mixer.Sound('sound/point.wav')
swooshing_sound = pygame.mixer.Sound('sound/swooshing.wav')
point_sound_countdown = 110

# Variable
gravity = 0.25
bird_move = 0
game_active = True
score = 0
high_score = 0
WHITE = (255, 255, 255)


#Program
while True:

	#Background Image
	screen.blit(background, (0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if  event.key == pygame.K_SPACE and game_active:
				bird_move = 0
				bird_move =- 7	
				flap_sound.play()
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (100, 351)
				bird_move = 0
				score = 0
		if event.type == spawnpipe:
			pipe_list.extend(create_pipe())			
			print(create_pipe)
		if event.type == birdflap:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0
			bird, bird_rect = bird_animation()
	if game_active:

		# Bird image and movement
		bird_move += gravity	# Increase gravity
		roteted_bird = rotate_bird(bird)
		bird_rect.centery += bird_move
		screen.blit(roteted_bird, bird_rect)
		game_active = check_collision(pipe_list)

		# Pipe
		pipe_list = move_pipe(pipe_list)
		draw_pipe(pipe_list)
		score += 0.01
		score_display('main game')
		point_sound_countdown -= 1
		if point_sound_countdown <= 0:
			point_sound.play()
			point_sound_countdown = 110
		
	else:
		screen.blit(game_over_surface, game_over_rect)
		high_score = update_score(score, high_score)
		score_display('game over')

	#floor
	floor_x -= 1
	draw_floor()
	if floor_x <= -432:
		floor_x = 0

	pygame.display.update()
	clock.tick(120)		# Set Frame rate



