import pygame
import os
import random
from states import settings
from states import utils
from states.base_state import State
from states.death_state import DeathState  #ADDED: death screen
from states import entities
from states.upgrade_state import UpgradeState

# assets folder is at repo root
repo_root = os.path.dirname(os.path.dirname(__file__))
asset_folder = os.path.join(repo_root, "assets")

class GameState(State):
    saved_player_position = None

    def on_enter(self, app):
        self.app = app
        pygame.init()
        pygame.mixer.init(devicename="pygame.mixer.get_dev_info()")
        
        # Sets the background color, and draws the image
        self.bg_color = (0, 0, 0)
        bg_name = "background_asteroids.png"
        self.bg_image = pygame.image.load(os.path.join(asset_folder, bg_name))

        # Creates the sprite groups
        self.ally_ships = pygame.sprite.Group()
        self.ally_bullets = pygame.sprite.Group()
        self.enemy_ships = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        # Countdown for player readiness
        self.countdown = 3.0   # seconds
        self.countdown_active = True

        if hasattr(app, "testing") and app.testing:
            self.countdown_active = False

        # Spawning Enemies
        self.enemy_ships.empty()

        # Loading Level Data
        self.bg_image = utils.build_level(
            level_name="first_level",
            enemy_ships=self.enemy_ships,
            temp_type=entities.Basic_Enemy
        )
        num_enemies = 10
        columns = num_enemies

        spacing_x = app.width // columns

        for i in range(num_enemies):
            # base position in column
            x = i * spacing_x + spacing_x // 2

            # add small randomness so it's not perfectly aligned
            x += random.randint(-20, 20)

            # spawn in top 1/4
            y = random.randint(0, app.height // 4)

            enemy = Basic_Enemy(
                frames=utils.load_spritesheet(
                    asset_folder=asset_folder,
                    sheet_name="enemy_basic.png",
                    key_color=utils.SHEET_BG,
                    frame_width=utils.FRAME_SIZE,
                    frame_height=utils.FRAME_SIZE
                ),
                start_pos=(x, y)
            )

            self.enemy_ships.add(enemy)



        # Spawning Player
        player_speed = 5
        self.player = entities.Player_Auto(
            # Loads the sprite sheet into the player's frames
            frames=utils.load_spritesheet(
                sheet_name="player_auto_ship.png",
                frame_width=utils.FRAME_SIZE,
                frame_height=utils.FRAME_SIZE
            ),
            speed=player_speed,
            start_pos=(app.width // 2, app.height - 50),
        )
        self.ally_ships.add(self.player)
        self.player_start_pos = (app.width // 2, app.height - 50)
        self.enemy_hit_count = 0
        self.lives = 3

        # Restore saved position if returning from pause
        if GameState.saved_player_position is not None:
            self.player.rect.center = GameState.saved_player_position

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Save player position before pausing
            GameState.saved_player_position = self.player.rect.center
            from states.pause_state import PauseScreen
            app.change_state(PauseScreen(app, self))

                # Keybind to quickly debug something
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            app.change_state(UpgradeState(app, self))
        
        # Shooting input
        if event.type == pygame.KEYDOWN and event.key == settings.keybind_player_shoot:
            if self.player.can_shoot:
                self.player.shoot(self.ally_bullets)
    
    def update(self, app, dt):
        # Keeps GameState from updating
        if self.countdown_active:
            self.countdown -= dt

            if self.countdown <= 0:
                self.countdown_active = False
            return # returns it to main.py loop

        keys = pygame.key.get_pressed()
        self.player.update(keys)

        play_area = pygame.Rect(0, 0, app.width, app.height)
        self.player.rect.clamp_ip(play_area)

        player_pos = (self.player.rect.x, self.player.rect.y)
        self.enemy_ships.update(player_pos=player_pos)

        # Enemy auto-fire logic for basic enemies
        for enemy in self.enemy_ships:
            if isinstance(enemy, entities.Basic_Enemy):
                enemy.shoot_cooldown -= dt
                if enemy.shoot_cooldown <= 0 and not enemy.can_shoot:
                    enemy.can_shoot = True

                if enemy.can_shoot:
                    enemy.shoot(self.enemy_bullets)

        # If enemy touches player
        if pygame.sprite.spritecollide(self.player, self.enemy_ships, False):
            if hasattr(app, "testing") and app.testing:
                app.change_state(DeathState("You Died", self.enemy_hit_count))
                return


            self.lives -= 1
            self.player.rect.center = self.player_start_pos

            if self.lives <= 0:
                app.change_state(DeathState("You Died", self.enemy_hit_count))
                sfx_player_boom = pygame.mixer.Sound("assets/sfx/p_boom.wav")
                pygame.mixer.Sound.play(sfx_player_boom)
                return

        # If enemy bullet hits player
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            self.lives -= 1
            self.player.rect.center = self.player_start_pos

            if self.lives <= 0:
                app.change_state(DeathState("You Died", self.enemy_hit_count))
                return
        # Update shooting cooldown
        if not self.player.can_shoot:
            self.player.shoot_cooldown -= dt
            if self.player.shoot_cooldown <= 0:
                self.player.can_shoot = True
        
        # Allow continuous shooting by holding spacebar
        if keys[settings.keybind_player_shoot] and self.player.can_shoot:
            self.player.shoot(self.ally_bullets)
        
        # Update bullets
        self.ally_bullets.update()
        self.enemy_bullets.update()
        
        # see if bullet hit an enemy
        collisions = pygame.sprite.groupcollide(
            self.ally_bullets, 
            self.enemy_ships, 
            True,  # Remove bullet on collision
            True   # Remove enemy on collision
        )
        #Score tracking for hits,
        if collisions:
            sfx_boom = pygame.mixer.Sound("assets/sfx/en_boom.wav")
            pygame.mixer.Sound.play(sfx_boom)
            self.enemy_hit_count += len(collisions)


    def draw(self, app, screen):
        screen.fill(self.bg_color)
        screen.blit(self.bg_image, (0, 0))
        self.ally_ships.draw(screen)
        self.enemy_ships.draw(screen)
        self.ally_bullets.draw(screen)
        self.enemy_bullets.draw(screen)


        if self.countdown_active:
            font = pygame.font.Font(None, 200)

            count = int(self.countdown) + 1  # makes it show 3,2,1

            if count > 0:
                text = font.render(str(count), True, (255, 255, 255))
            else:
                text = font.render("GO", True, (255, 255, 255))

            rect = text.get_rect(center=(app.width // 2, app.height // 2))
            screen.blit(text, rect)

        
        # Draws Text for Readiness Countdown
        if self.countdown_active:
            font = pygame.font.Font(None, 200)
            count = int(self.countdown) + 1  # makes it show 3,2,1

            if count > 0:
                text = font.render(str(count), True, (255, 255, 255))
            else:
                text = font.render("GO", True, (255, 255, 255))

            rect = text.get_rect(center=(app.width // 2, app.height // 2))
            screen.blit(text, rect)


        # delete after testing
        # pygame.draw.rect(screen, (255,255,255), self.player.hitbox)

        # Draw hit counter
        font = pygame.font.Font(None, 36)
        counter_text = font.render(f"Hits: {self.enemy_hit_count}", True, (255, 255, 255))
        screen.blit(counter_text, (10, 10))
        font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 20)

        for i in range(self.lives):
            heart = font.render("♥", True, (255, 0, 0))
            screen.blit(heart, (10 + i * 30, screen.get_height() - 40))

