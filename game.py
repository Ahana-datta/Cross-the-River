import pygame
import sys
import random
import math
import time
import config as cfg
from config import Player, MovingObs, StationaryObs

#initialize the screen
pygame.init()
surf = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

height = surf.get_height()
#surf = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
width = surf.get_width()
h = height/30
w = width

lev = 1
turn = 1

score = [0, 0]
sc = [0, 0]

# player1
pl1img = pygame.image.load("pl1ic.png")
pl1icon = pygame.image.load("player1.png")
pl1pos = [width/2, 0]
# keys for player1 [up, down, right, left]
key1 = [False, False, False, False]
pl1 = Player(pl1icon, pl1pos[0], pl1pos[1], score[0], sc[0], 1, key1, surf)

# player2
pl2img = pygame.image.load("pl2ic.png")
pl2icon = pygame.image.load("player2.png")
pl2pos = [w/2, height-50]
# keys for player1 [w, s, d, a]
key2 = [False, False, False, False]
pl2 = Player(pl2icon, pl2pos[0], pl2pos[1], score[1], sc[1], 1, key2, surf)

pl = pl1

# moving obstacles
movobs = []
movobsic = []
no_movobs = 5
for i in range(no_movobs):
	movobsic.append(pygame.image.load(("movobs"+str(i+1)+".png")))

movobs_posx = []
movobs_posy = []
#movobs_posx.append(random.randint(5,width-65))
#movobs_posy.append((6*h))
for i in range(no_movobs-1):
	movobs_posx.append(random.randint(20,width-100))
	movobs_posy.append((2.8*h + 5 + (4.4*(i+1)*h)))
movobs_posx.append(random.randint(20,width-100))
movobs_posy.append((h + 15 + height/30))

movobs_chngx = []
for i in range(no_movobs):
	movobs_chngx.append(1 + i%lev)
	movobs.append(MovingObs(movobsic[i], movobs_posx[i], movobs_posy[i], movobs_chngx[i], surf))
movobs_chngy = []


# stationary obstacles
statobs = []
statobsic = []
no_statobs = 6

statobs_posx = []
statobs_posy = []
for i in range(no_statobs - 1):
	statobs_posx.append(random.randint(40,width-100))
	statobs_posy.append((h - 10 + (4.4*(i+1)*h)))
statobs_posx.append(random.randint(40, width/2))
statobs_posy.append((h - 10 + 4.4*3*h))
statobs_posx[2] = (random.randint((10 + width/2),(width-100)))
statobs_posy[2] = h - 10 + 4.4*3*h

for i in range(no_statobs):
	statobsic.append(pygame.image.load(("statobs"+str(i+1)+".png")))
	statobs.append(StationaryObs(statobsic[i], statobs_posx[i], statobs_posy[i], surf))

# other initializations
dispbot = height-h-10
disptop = 0
run = True
gameover = False
obs_score = []
for i in range(no_movobs + no_statobs):
	obs_score.append(0)

check = 1

bonus = 32
prevtime = 0

def switch_player(turn_no, level):
	global pl
	global disp_end
	global disp_start
	if turn_no%2 != 0:
		pl = pl1
		pl.posx = pl1pos[0]
		pl.posy = pl1pos[1]
		for i in range(4):
			pl.key1[i] = False
		disp_start = disptop
		disp_end = dispbot
		switch_player_text = cfg.overfonts.render((" Player 1 Round "+str(level)+" "), True, (0, 0, 0))
	else:
		pl = pl2
		pl.posx = pl2pos[0]
		pl.posy = pl2pos[1]
		for i in range(4):
			pl.key1[i] = False
		disp_start = dispbot
		disp_end = disptop
		switch_player_text = cfg.overfonts.render(" Player 2 Round "+str(level)+" ", True, (0, 0, 0))
	switchrect = switch_player_text.get_rect()
	switchrect.center = [width/2, height/2]
	surf.blit(switch_player_text, switchrect)
	
	pygame.display.update()
	
	time.sleep(1)
	return pl.posx, pl.posy, False

def isCollision(plx, ply, obsx, obsy):
	#obsrect = pygame.Rect(obsx, obsy, 64, 64)
	distance = math.sqrt(math.pow(plx - obsx, 2) + (math.pow(ply - obsy, 2)))
	#if pl.rect.colliderect(obsrect):
	#	return True
	if distance < 60:
		return True
	else:
		return False

def game_over_text(mess):
	#gameover = True
	over_text = cfg.overfonts.render(mess, True, (255, 0, 0))
	gameoverrect = over_text.get_rect()
	gameoverrect.center = [width/2, height/2]
	surf.blit(over_text, gameoverrect)
	#time.sleep(1)
	return True
#switch_player(turn, lev)
while run: # main game loop

	surf.fill(cfg.river)
	h = height/30

	# draw top bank
	top = pygame.draw.rect(surf, cfg.bank, (0, 0, width, 64))

	# display scores and player icons
	surf.blit(pl1img, (2,0))
	surf.blit(pl2img, (width-66,0))
	pl1text = cfg.fonts.render(("Player 1 SCORE:"+str(pl1.score)), True, (0, 0, 0))
	pl2text = cfg.fonts.render("Player 2 SCORE:"+str(pl2.score), True, (0, 0, 0))
	pl1screct = pl1text.get_rect()
	pl1screct.topleft = (67,2)
	surf.blit(pl1text, pl1screct)
	pl2screct = pl2text.get_rect()
	pl2screct.topright = (width-67,2)
	surf.blit(pl2text, pl2screct)
	

	if lev < 6:

		# switch player if turn was updated in previous iteration i.e. if check == 1
		if check:
		
			check = 0
			pl.posx, pl.posy, gameover = switch_player(turn, lev)
			for i in range(no_movobs):
				movobs[i].chngx = pl.lev + i%2
		
		# draw partitons
		for i in range(1, 6):
			pygame.draw.rect(surf, cfg.sand, (5, (h+(4.4*i*h)), width-10, 50))
		
		# draw bottom bank
		bottom = pygame.draw.rect(surf, cfg.bank, (0, height-60, width, 60))
		
		# display score
		bonus_score_text = cfg.font.render("Bonus score: " + str(bonus), True, (255, 255, 255))
		bonusrect = bonus_score_text.get_rect()
		bonusrect.topright = [width-10, h + 30]
		surf.blit(bonus_score_text, bonusrect)

		# add moving obstacles
		for i in range(no_movobs):
			movobs[i].addMovingObs(movobs[i].posx, movobs[i].posy)

		# add stationary obstacles
		for i in range(no_statobs):
			statobs[i].addStationaryObs(statobs[i].posx, statobs[i].posy)
		
		# add "start" "end" and score texts
		start = cfg.fonts.render("START", True, (0, 0, 0))
		end = cfg.fonts.render("END", True, (0, 0, 0))
		
		startrect = start.get_rect()
		startrect.centerx = (w/2)
		startrect.top = disp_start
		surf.blit(start, startrect)
		endrect = end.get_rect()
		endrect.centerx = (w/2)
		endrect.top = disp_end
		surf.blit(end, endrect)

		# add player
		pl.addPlayer(pl.posx, pl.posy)
		

		# check for collisions
		for i in range(no_movobs):
			coll = isCollision(pl.posx, pl.posy, movobs[i].posx, movobs[i].posy)
			if coll:
				gameover = game_over_text(cfg.hit)
				bonus = -15		
				break
		for i in range(no_statobs):
			coll = isCollision(pl.posx, pl.posy, statobs[i].posx, statobs[i].posy)
			if coll:
		#		print("hit")
				gameover = game_over_text(cfg.hit)
				bonus = -15	
				break

		# check if player reached end
		if (pl.posy+32 >= endrect.top and endrect.top != 0) or (pl.posy <= 20 and endrect.top == 0):
		#	print("reached end = " + str(endrect.top))
			gameover = game_over_text(cfg.success)

		check = 0
		# create time bonus
		nowtime = pygame.time.get_ticks()/1000
		bonus = bonus - (nowtime - prevtime)
		prevtime = nowtime
		if bonus < 0 and bonus != -15:
			bonus = 0

		pygame.display.update()

	    # update score
		if not gameover:
#			score[(turn+1)%2] = sc[(turn+1)%2]
			pl.score = pl.sc
			# print("pl1pos="+str(pl1pos[1]))
			for i in range(no_statobs):
				#print("statpos="+str(int(statobs_posy[i])))
				if pl.posy + math.pow(-1, turn)*50 == int(statobs[i].posy):
					obs_score[i] = 5
					#print(score)
					
			for i in range(no_movobs):
				if pl.posy + math.pow(-1, turn)*50 == int(movobs[i].posy):
					obs_score[no_statobs + i] = 10
					
			for i in range(no_statobs + no_movobs):
				#score[(turn+1)%2] += obs_score[i]
				pl.score += obs_score[i]
		
		else:
			time.sleep(1)

		# check for events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

				# for controlling movement of player 1 using keys for player 1
				elif turn%2 != 0:
					if event.key == pygame.K_UP:
						pl.key1[0] = True
					elif event.key == pygame.K_DOWN:
						pl.key1[1] = True
					elif event.key == pygame.K_RIGHT:
						pl.key1[2] = True
					elif event.key == pygame.K_LEFT:
						pl.key1[3] = True

				# for controlling movement of player 2 using keys for player 2
				else:
					if event.key == pygame.K_w:
						pl.key1[0] = True
					elif event.key == pygame.K_s:
						pl.key1[1] = True
					elif event.key == pygame.K_d:
						pl.key1[2] = True
					elif event.key == pygame.K_a:
						pl.key1[3] = True

			# when key is released we need to reset values in pl.key ekse the player will continue to move
			elif event.type == pygame.KEYUP:
				if turn%2 != 0:
					if event.key == pygame.K_UP:
						pl.key1[0] = False
					elif event.key == pygame.K_DOWN:
						pl.key1[1] = False
					elif event.key == pygame.K_RIGHT:
						pl.key1[2] = False
					elif event.key == pygame.K_LEFT:
						pl.key1[3] = False
				else:
					if event.key == pygame.K_w:
						pl.key1[0] = False
					elif event.key == pygame.K_s:
						pl.key1[1] = False
					elif event.key == pygame.K_d:
						pl.key1[2] = False
					elif event.key == pygame.K_a:
						pl.key1[3] = False
			elif event.type == pygame.VIDEORESIZE:
				width = event.dict['size'][0]
				height = event.dict['size'][1]
		
		# update positions if game not over
		if not gameover:
			pl.updatepos()
		
			# change pos of moving obstacles
			for i in range(no_movobs):
				movobs[i].posx += movobs[i].chngx
		
		# if game is over i.e. player has hit and obstacle or end, update turn, lev, obstacle speed & re-initialize score and bonus score 
		else:
			check = 1
			pl.score += bonus
			pl.sc = pl.score
			bonus = 32
			for i in range(no_statobs + no_movobs):
				obs_score[i] = 0
			turn += 1
			if turn%2 != 0:
				lev += 1

				# change level of players depending on who won this round
				if pl1.score > pl2.score:
					pl1.lev += 1
				elif pl2.score > pl1.score:
					pl2.lev +=1
				else:
					pl1.lev += 1
					pl2.lev += 1

				# change position of stationary obstacle
				for i in range(no_statobs - 1):
					statobs_posx.append(random.randint(40,width-100))
					statobs_posy.append((h - 10 + (4.4*(i+1)*h)))
				statobs_posx.append(random.randint(40, width/2))
				statobs_posy.append((h - 10 + 4.4*3*h))
				statobs_posx[2] = (random.randint((10 + width/2),(width-100)))
				statobs_posy[2] = h - 10 + 4.4*3*h

	# if game is over i.e. 5 rounds are over		
	else:
		# display winner
		if pl2.score > pl1.score:
			game_over_text(cfg.pl2win)
			surf.blit(pl2icon, (width/2, (height/2)-100))
		elif pl2.score < pl1.score:
			game_over_text(cfg.pl1win)
			surf.blit(pl1icon, (width/2, (height/2)-100))
		else:
			game_over_text(cfg.bothwin)
			surf.blit(pl1icon, (width/2 - 70, (height/2)-100))
			surf.blit(pl2icon, (width/2 + 10, (height/2)-100))
		pygame.display.update()

		# handle exit from game 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

        
