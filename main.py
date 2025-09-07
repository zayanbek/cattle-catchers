import pygame, sys, random, asyncio
from pygame.math import Vector2

class COWBOY:
	def __init__(self):
		self.reset()
		self.new_block = False

		self.sprite_sheet = pygame.image.load('Graphics/cowboy_sprite_sheet.png').convert_alpha()
		
		self.head_right = self.sprite_sheet.subsurface((80, 0, 40, 40)).copy()  

		self.tail_down = self.sprite_sheet.subsurface((0, 80-40, 40, 40)).copy()
		
		self.body_top_left = self.sprite_sheet.subsurface((0, 0, 40, 40)).copy()
		
		self.body_horizontal = self.sprite_sheet.subsurface((40, 0, 40, 40)).copy()  
		
		self.moo1 = pygame.mixer.Sound('Sound/moo.wav')
		self.moo2 = pygame.mixer.Sound('Sound/moo2.wav')

	def draw_cowboy(self):
		self.update_head_graphics()
		self.update_tail_graphics()

		for index,block in enumerate(self.body):
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			if index == 0:
				screen.blit(self.head,block_rect)
			elif index == len(self.body) - 1:
				screen.blit(self.tail,block_rect)
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(pygame.transform.rotate(self.body_horizontal, 90),block_rect) # vertical
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal,block_rect) # horizontal
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(pygame.transform.rotate(self.body_top_left, 180),block_rect) # bottom right
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(pygame.transform.rotate(self.body_top_left, -90),block_rect) # top right
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(pygame.transform.rotate(self.body_top_left, 90),block_rect) # bottom left 
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_top_left,block_rect)

	def update_head_graphics(self):
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1,0): self.head = pygame.transform.flip(self.head_right, True, False)  
		elif head_relation == Vector2(-1,0): self.head = self.head_right
		elif head_relation == Vector2(0,1): self.head = pygame.transform.rotate(self.head_right, 90)
		elif head_relation == Vector2(0,-1): self.head = pygame.transform.rotate(self.head_right, -90)

	def update_tail_graphics(self):
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(1,0): self.tail = pygame.transform.rotate(self.tail_down, -90)
		elif tail_relation == Vector2(-1,0): self.tail = pygame.transform.rotate(self.tail_down, 90)
		elif tail_relation == Vector2(0,1): self.tail = pygame.transform.rotate(self.tail_down, 180)
		elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

	def move_cowboy(self):
		if self.new_block == True:
			body_copy = self.body[:]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]

	def add_block(self):
		self.new_block = True

	def play_moo_sound(self):
		if random.randint(1, 2) == 1:
			self.moo1.play()
		else:
			self.moo2.play()

	def reset(self):
		# self.body = [Vector2(10,10), Vector2(9,10), Vector2(8,10), Vector2(7,10), Vector2(6,10), Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.body = [Vector2(i, 10) for i in range(10, 2, -1)]
		self.direction = Vector2(0,0)

class CATTLE:
	def __init__(self):
		self.randomize()

	def draw_cow(self):
		cow_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
		screen.blit(apple,cow_rect)

	def randomize(self):
		self.x = random.randint(2,cell_number - 3)
		self.y = random.randint(2,cell_number - 3)	
		
		self.pos = Vector2(self.x,self.y)

class MAIN:
	def __init__(self):
		self.cowboy = COWBOY()
		self.cow = CATTLE()
		self.score = 0

	def update(self):
		self.cowboy.move_cowboy()
		self.check_collision()
		self.check_fail()

	def draw_elements(self):
		screen.fill((175,215,70))
		self.draw_grass()

		# Draw Fence
		fence = pygame.image.load('Graphics/entire_fence.png').convert_alpha()
		fence_rect = pygame.Rect(0,0,800,800)
		screen.blit(fence,fence_rect)

		self.cow.draw_cow()
		self.cowboy.draw_cowboy()
		self.draw_score()

	def loop_made(self, body, target):
		tampered_cowboy = body[1:]
		target_x = int(target.x)
		target_y = int(target.y)

		same_x = [
			p for p in tampered_cowboy
			if int(p.x) == target_x and (int(p.x), int(p.y)) != (target_x, target_y)
		]

		same_y = [
			p for p in tampered_cowboy
			if int(p.y) == target_y and (int(p.x), int(p.y)) != (target_x, target_y)
		]

		unique_same_x = set((int(p.x), int(p.y)) for p in same_x)
		unique_same_y = set((int(p.x), int(p.y)) for p in same_y)

		return len(unique_same_x) >= 2 and len(unique_same_y) >= 2
	
	def check_collision(self):
		if self.loop_made(self.cowboy.body, self.cow.pos):
			self.cow.randomize()
			self.cowboy.add_block()
			self.cowboy.play_moo_sound()
			self.score += 1

		if self.cow.pos == self.cowboy.body[0]:
			self.game_over()
		

		for block in self.cowboy.body[1:]:
			if block == self.cow.pos:
				self.cow.randomize()

	

	def check_fail(self):
		if not 1 <= self.cowboy.body[0].x < cell_number-1 or not 1 <= self.cowboy.body[0].y < cell_number-1:
			self.game_over()

		for block in self.cowboy.body[1:]:
			if block == self.cowboy.body[0]:
				self.game_over()
		
	def game_over(self):
		self.cowboy.reset()
		self.score = 0

	def draw_grass(self):
		grass_color = (167,209,61)
		for row in range(cell_number):
			if row % 2 == 0: 
				for col in range(cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
			else:
				for col in range(cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)			

	def draw_score(self):
		score_text = str(self.score)
		score_surface = game_font.render(score_text,True,(56,74,12))
		score_x = int(cell_size * cell_number - 60)
		score_y = int(cell_size * cell_number - 40)
		score_rect = score_surface.get_rect(center = (score_x,score_y))
		apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

		pygame.draw.rect(screen,(167,209,61),bg_rect)
		screen.blit(score_surface,score_rect)
		screen.blit(apple,apple_rect)
		pygame.draw.rect(screen,(56,74,12),bg_rect,2)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
height, width = 800, 800
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/cow.png').convert_alpha()

title_text_color = (41, 30, 21)

game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
title_font = pygame.font.Font('Font/wild_west_font.ttf', 100)
play_font = pygame.font.Font('Font/wild_west_font.ttf', 50)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

# Render text
title_text_surface = title_font.render("Cattle Catcher", True, title_text_color)
title_text_rect = title_text_surface.get_rect()
title_text_rect.centerx = width // 2  # Center along x-axis
title_text_rect.top = 250          # Y-position (change as needed)

button_pos = (800/2-200/2, 400)
button_size = (200, 100)

button_image = pygame.transform.scale(pygame.image.load("Graphics/play_poster.png"), button_size)
button_rect = pygame.Rect(button_pos, button_size)

background_image = pygame.image.load("Graphics/wooden_table.png")  # Replace with your image file
background_image = pygame.transform.scale(background_image, (width, height))

async def main():

	game_state = "title" # title, game\

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == SCREEN_UPDATE:
				main_game.update()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					if main_game.cowboy.direction.y != 1:
						main_game.cowboy.direction = Vector2(0,-1)
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					if main_game.cowboy.direction.x != -1:
						main_game.cowboy.direction = Vector2(1,0)
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					if main_game.cowboy.direction.y != -1:
						main_game.cowboy.direction = Vector2(0,1)
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					if main_game.cowboy.direction.x != 1:
						main_game.cowboy.direction = Vector2(-1,0)
			if game_state == "title" and event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
				game_state = "game"
                
		if game_state == "game": 
			main_game.draw_elements()

		elif game_state == "title":
			screen.blit(background_image, (0, 0))
			screen.blit(title_text_surface, title_text_rect) # text

			screen.blit(button_image,button_pos)

			button_text = play_font.render("Play", True, title_text_color)
			button_text_rect = button_text.get_rect(center=button_rect.center)
			screen.blit(button_text, button_text_rect)
		
	
		pygame.display.update()
		clock.tick(80)
		await asyncio.sleep(0)

asyncio.run(main())