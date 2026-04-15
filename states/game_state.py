import pygame
import os
import random
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
font_color = (255,255,255) # Currently set to white

class GameState(State):
    saved_player_position = None
    current_level_num = 0

    # progression state
    level_sequence = utils.get_level_sequence()
    if not level_sequence:
        raise ValueError("No levels found in level_data.json")
    level_index = 0
    current_level_name = level_sequence[level_index]
    current_level_data = utils.load_level(current_level_name)
    pending_level_index = None
    waiting_for_upgrade = False

    enemy_hit_count = 0
    lives = 3

    def on_enter(self, app):
        self.app = app
        pygame.init()
        pygame.mixer.init(devicename="pygame.mixer.get_dev_info()")
        
        # reset upgrade-tuned stats at run start
        settings.bullet_spd = settings.DEFAULT_BULLET_SPEED
        settings.bullet_cooldown = settings.DEFAULT_BULLET_COOLDOWN

        # Sets the background color, and loads lives_icon
        self.bg_color = (0, 0, 0)
        self.lives_icon = pygame.image.load(os.path.join(asset_folder, "icon_lives.png"))
        self.lives_icon.set_colorkey(utils.SHEET_BG)

        # Loads UI Fonts
        self.score_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf",26)
        self.lives_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf",20)
        self.countdown_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf",180)

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

        # Spawns Level
        self.enemy_ships.empty()
        self.bg_image = utils.build_level(
            level_name=self.current_level_name,
            enemy_ships=self.enemy_ships
        )
        self.current_level_num += 1

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
        self.player_invincible = False
        self.player_invincible_timer = 0.0

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

        if self.player_invincible:
            self.player_invincible_timer -= dt
            if self.player_invincible_timer <= 0:
                self.player_invincible = False
                self.player_invincible_timer = 0.0

        play_area = pygame.Rect(0, 0, app.width, app.height)
        self.player.rect.clamp_ip(play_area)

        player_pos = (self.player.rect.centerx, self.player.rect.centery)
        self.enemy_ships.update(player_pos=player_pos)

        # for enemy in self.enemy_ships:
        #     if not hasattr(enemy, "move_timer"):
        #         enemy.pos = pygame.Vector2(enemy.rect.x, enemy.rect.y)
        #         enemy.move_timer = random.uniform(1.0, 3.0)
        #         enemy.pause_timer = 0
        #         enemy.velocity = pygame.Vector2(
        #             random.uniform(-30, 30),
        #             random.uniform(40, 80)
        #         )
        #         enemy.shoot_cooldown = random.uniform(2.0, 4.0)
        #         enemy.can_shoot = False

        #     if enemy.pause_timer > 0:
        #         enemy.pause_timer -= dt
        #     else:
        #         enemy.pos += enemy.velocity * dt
        #         enemy.rect.x = int(enemy.pos.x)
        #         enemy.rect.y = int(enemy.pos.y)

        #         enemy.move_timer -= dt

        #         if enemy.move_timer <= 0:
        #             if random.random() < 0.4:
        #                 enemy.pause_timer = random.uniform(0.5, 1.5)
        #             else:
        #                 enemy.velocity = pygame.Vector2(
        #                     random.uniform(-30, 30),
        #                     random.uniform(40, 80)
        #                 )

        #             enemy.move_timer = random.uniform(1.0, 3.0)

        # for enemy in self.enemy_ships:
        #     if enemy.rect.top > app.height:
        #         enemy.pos.y = -enemy.rect.height
        #         enemy.pos.x = random.randint(0, app.width - enemy.rect.width)
        #         enemy.rect.x = int(enemy.pos.x)
        #         enemy.rect.y = int(enemy.pos.y)

        #     if enemy.rect.left < 0:
        #         enemy.pos.x = 0
        #         enemy.velocity.x *= -1
        #         enemy.rect.x = int(enemy.pos.x)

        #     elif enemy.rect.right > app.width:
        #         enemy.pos.x = app.width - enemy.rect.width
        #         enemy.velocity.x *= -1
        #         enemy.rect.x = int(enemy.pos.x)

        # Refresh bullet hitboxes after bullets move
        self.bullet_hitboxes = utils.extract_hitboxes(self.enemy_bullets)


        # Enemy auto-fire logic for basic enemies
        for enemy in self.enemy_ships:
            if isinstance(enemy, entities.Basic_Enemy):
                enemy.shoot_cooldown -= dt
                if enemy.shoot_cooldown <= 0 and not enemy.can_shoot:
                    enemy.can_shoot = True

                if enemy.can_shoot:
                    enemy.shoot(self.enemy_bullets)
                    enemy.shoot_cooldown = random.uniform(3.0, 5.0)
                    enemy.can_shoot = False

        # Update player shooting cooldown
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
            True,
            True
        )

        self.enemy_hitboxes = utils.extract_hitboxes(self.enemy_ships)

        if not self.player_invincible and (
            self.player.check_collisions(self.enemy_hitboxes) or
            self.player.check_collisions(self.bullet_hitboxes)
        ):
            if hasattr(app, "testing") and app.testing:
                app.change_state(DeathState("You Died", self.enemy_hit_count))
                return

            pygame.sprite.spritecollide(self.player, self.enemy_ships, False)
            pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)

            self.lives -= 1
            # Sets Invinicibility
            self.player_invincible = True
            self.player_invincible_timer = 1.0
            # Resets player position
            self.player.rect.center = self.player_start_pos
            self.player.hitbox.center = self.player_start_pos

            if self.lives <= 0:
                app.change_state(DeathState("You Died", self.enemy_hit_count))
                sfx_player_boom = pygame.mixer.Sound("assets/sfx_ogg/p_boom.ogg")
                pygame.mixer.Sound.play(sfx_player_boom)
                return

        # Score tracking for hits
        if collisions:
            for bullet, enemies in collisions.items():
                for enemy in enemies:
                    if hasattr(enemy, "take_damage"):
                        enemy.take_damage(1)
                        self.enemy_hit_count += 1
                        if hasattr(enemy, "health") and enemy.health <= 0:
                            enemy.kill()
                            sfx_boom = pygame.mixer.Sound("assets/sfx_ogg/en_boom.ogg")
                            pygame.mixer.Sound.play(sfx_boom)

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
        for enemy in self.enemy_ships:
            if hasattr(enemy, "draw_health_bar"):
                enemy.draw_health_bar(screen)
        self.ally_bullets.draw(screen)
        self.enemy_bullets.draw(screen)
        
        font_file = os.path.join(asset_folder, "fonts/PressStart2P-vaV7.ttf")

        # Draws Text for Readiness Countdown
        if self.countdown_active:
            count = int(self.countdown) + 1  # makes it show 3,2,1

            if count > 0:
                text = self.countdown_font.render(str(count), True, font_color)
            else:
                text = self.countdown_font.render("GO", True, font_color)

            countdown_rect = text.get_rect(center=(app.width // 2, app.height // 2))
            screen.blit(text, countdown_rect)

        # Draw Score and Level Counters
        counter_text = self.score_font.render(f"Score: {self.enemy_hit_count}", True, font_color)
        screen.blit(counter_text, (10, 10))
        level_text = self.score_font.render(
            f"Level: {self.level_index + 1}",
            True,
            font_color
        )
        screen.blit(level_text, (10, 45))

        #pygame.draw.rect(screen, (0,0,255), self.player.hitbox)
        #if len(self.enemy_hitboxes) > 0:
        #    pygame.draw.rect(screen, (0,0,255), self.enemy_hitboxes[0])
        #if len(self.bullet_hitboxes) > 0:
        #    pygame.draw.rect(screen, (0,0,255), self.bullet_hitboxes[0])

        # Draw Lives Counter
        live_count = self.lives_font.render(f"x{self.lives}", True, font_color)
        screen.blit(self.lives_icon,(20, screen.get_height() - 45))
        screen.blit(live_count, (60, screen.get_height() - 35))

