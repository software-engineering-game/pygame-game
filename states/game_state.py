import pygame
import os
from states import settings
from states import utils
from states import entities
from states.base_state import State
from states.death_state import DeathState  #ADDED: death screen
from states.upgrade_state import UpgradeState
from states.win_state import WinState

# assets folder is at repo root
repo_root = os.path.dirname(os.path.dirname(__file__))
asset_folder = os.path.join(repo_root, "assets")

class GameState(State):
    saved_player_position = None

    def on_enter(self, app):
        self.app = app
        #pygame.init()
        #pygame.mixer.init(devicename="pygame.mixer.get_dev_info()")
        
        # reset upgrade-tuned stats at run start
        settings.BULLET_SPEED = settings.DEFAULT_BULLET_SPEED
        settings.BULLET_COOLDOWN = settings.DEFAULT_BULLET_COOLDOWN

        # Sets the background color
        self.bg_color = (0, 0, 0)

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

        # progression state
        self.level_sequence = utils.get_level_sequence()
        if not self.level_sequence:
            raise ValueError("No levels found in level_data.json")
        self.level_index = 0
        self.current_level_name = self.level_sequence[self.level_index]
        self.current_level_data = utils.load_level(self.current_level_name)
        self.pending_level_index = None
        self.waiting_for_upgrade = False

        # spawn first wave of first level
        self.enemy_ships.empty()
        self.bg_image = utils.build_level(
            level_name=self.current_level_name,
            enemy_ships=self.enemy_ships
        )
        self.current_level_num = 1

        self.enemy_hitboxes = utils.extract_hitboxes(self.enemy_ships)
        self.bullet_hitboxes = []

        # Spawning Player with class Player_Auto
        self.player_speed = 5
        self.player_start_pos = (app.width // 2, app.height - 50)
        self.player = entities.Player_Auto(
            # Loads the sprite sheet into the player's frames
            frames=utils.load_spritesheet(
                sheet_name="player_auto_ship.png",
                frame_width=utils.FRAME_SIZE,
                frame_height=utils.FRAME_SIZE
            ),
            speed=self.player_speed,
            start_pos=self.player_start_pos,
        )
        self.ally_ships.add(self.player)
        self.enemy_hit_count = 0
        self.lives = 3

        # Restore saved position if returning from pause
        if GameState.saved_player_position is not None:
            self.player.rect.center = GameState.saved_player_position

    def _resume_after_upgrade(self):
        if self.pending_level_index is not None:
            self.level_index = self.pending_level_index
            self.current_level_name = self.level_sequence[self.level_index]
            self.current_level_data = utils.load_level(self.current_level_name)

        self.pending_level_index = None
        self.waiting_for_upgrade = False

        # reset projectiles between waves so transitions are fair
        self.enemy_ships.empty()
        self.enemy_bullets.empty()
        self.ally_bullets.empty()
        self.bg_image = utils.build_level(
            level_name=self.current_level_name,
            enemy_ships=self.enemy_ships
        )
        self.current_level_num += 1

        # short countdown before next wave starts
        self.countdown = 1.5
        self.countdown_active = True

    def on_upgrade_complete(self):
        self._resume_after_upgrade()

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Save player position before pausing
            GameState.saved_player_position = self.player.rect.center
            from states.pause_state import PauseScreen
            app.change_state(PauseScreen(app, self))

                # Keybind to quickly debug something
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            self.waiting_for_upgrade = True
            self.pending_level_index = self.level_index
            app.change_state(UpgradeState(app, self))
        
        # Shooting input
        if event.type == pygame.KEYDOWN and event.key == settings.keybind_player_shoot:
            if self.player.can_shoot:
                self.player.shoot(self.ally_bullets)
    
    def update(self, app, dt):
        # Keeps GameState from updating during countdown
        if self.countdown_active:
            self.countdown -= dt

            if self.countdown <= 0:
                self.countdown_active = False
            return # returns it to main.py loop

        keys = pygame.key.get_pressed()
        self.player.update(keys)

        play_area = pygame.Rect(0, 0, app.width, app.height)
        self.player.rect.clamp_ip(play_area)

        player_pos = (self.player.rect.centerx, self.player.rect.centery)
        self.enemy_ships.update(player_pos=player_pos)
        for enemy in self.enemy_ships:
            enemy.rect.clamp_ip(play_area)

        # Enemy auto-fire logic for basic enemies
        for enemy in self.enemy_ships:
            if isinstance(enemy, entities.Basic_Enemy):
                enemy.shoot_cooldown -= dt
                if enemy.shoot_cooldown <= 0 and not enemy.can_shoot:
                    enemy.can_shoot = True

                if enemy.can_shoot:
                    enemy.shoot(self.enemy_bullets)
                    self.bullet_hitboxes = utils.extract_hitboxes(self.enemy_bullets)

        # If enemy touches player or enemy bullet hits player
        if (self.player.check_collisions(self.enemy_hitboxes) or self.player.check_collisions(self.bullet_hitboxes)):
            if hasattr(app, "testing") and app.testing:
                app.change_state(DeathState("You Died", self.enemy_hit_count))
                return

            pygame.sprite.spritecollide(self.player,self.enemy_bullets,True)

            self.lives -= 1
            self.player.rect.center = self.player_start_pos
            self.player.hitbox.center = self.player_start_pos

        # If lives reaches zero
        if self.lives <= 0:
            #sfx_player_boom = pygame.mixer.Sound("assets/sfx/p_boom.wav")
            #pygame.mixer.Sound.play(sfx_player_boom)
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
        
        # Checks if ally_bullet hit an enemy_ship
        collisions = pygame.sprite.groupcollide(
            self.ally_bullets,
            self.enemy_ships,
            True,  # Remove bullet on collision
            True   # Remove enemy on collision
        )
        #Score tracking for hits,
        if collisions:
            #sfx_boom = pygame.mixer.Sound("assets/sfx/en_boom.wav")
            #pygame.mixer.Sound.play(sfx_boom)
            self.enemy_hit_count += len(collisions)

        # Level progression: clear level -> upgrade pick -> spawn next level
        if not self.enemy_ships and not self.waiting_for_upgrade:
            is_last_level = self.level_index >= len(self.level_sequence) - 1

            if is_last_level:
                app.change_state(WinState("You Win!", self.enemy_hit_count))
                return

            self.waiting_for_upgrade = True
            if not is_last_level:
                self.pending_level_index = self.level_index + 1
            else:
                self.pending_level_index = self.level_index

            app.change_state(UpgradeState(app, self))
            return


    def draw(self, app, screen):
        # Background
        screen.fill(self.bg_color)
        screen.blit(self.bg_image, (0, 0))
        
        # Game Entities
        self.ally_ships.draw(screen)
        self.enemy_ships.draw(screen)
        self.ally_bullets.draw(screen)
        self.enemy_bullets.draw(screen)
        
        font_file = os.path.join(asset_folder, "fonts/PressStart2P-vaV7.ttf")

        # Draws Text for Readiness Countdown
        if self.countdown_active:
            font = pygame.font.Font(font_file, 140)
            count = int(self.countdown) + 1  # makes it show 3,2,1

            if count > 0:
                text = font.render(str(count), True, (255, 255, 255))
            else:
                text = font.render("GO", True, (255, 255, 255))

            rect = text.get_rect(center=(app.width // 2, app.height // 2))
            screen.blit(text, rect)

        # Draw hit counter
        font = pygame.font.Font(font_file, 20)
        counter_text = font.render(f"Score: {self.enemy_hit_count}", True, (255, 255, 255))
        screen.blit(counter_text, (10, 10))
        
        # Draws Lives Counter
        #screen.blit(pygame.image.load("assets/icon_lives.png"), (35,settings.HEIGHT - 40))
        font = pygame.font.Font(font_file, 20)
        heart = font.render("♥x" + str(self.lives), True, (255, 0, 0))
        screen.blit(heart, (35, screen.get_height() - 40))
        
        level_text = font.render(
           f"Level: {self.current_level_num}",
           True,
           (255, 255, 255)
        )
        screen.blit(level_text, (10, 45))

