import random
from states import settings
from states import utils
from states import entities
from states.game_state import GameState
from states.upgrade_state import UpgradeState


class EndlessGameState(GameState):
    def on_enter(self, app):
        if getattr(self, "endless_initialized", False):
            return

        self.endless_initialized = True
        self.endless_round = 1

        super().on_enter(app)

    def handle_level_clear(self, app):
        self.waiting_for_upgrade = True
        self.pending_level_index = None
        app.change_state(UpgradeState(app, self))

    def _resume_after_upgrade(self):
        self.pending_level_index = None
        self.waiting_for_upgrade = False

        self.enemy_ships.empty()
        self.enemy_bullets.empty()
        self.ally_bullets.empty()

        self.endless_round += 1
        self.spawn_random_level()

        self.current_level_num += 1

        self.countdown = 1.5
        self.countdown_active = True

    def get_spawn_positions(self, count):
        positions = []

        # Keep enemies in the top third of the screen
        top_y = 70
        max_y = settings.HEIGHT // 3

        x_spacing = 75
        y_spacing = 65

        # Make the formation clustered instead of full-screen wide
        columns = min(7, max(3, count))
        rows = (count + columns - 1) // columns

        formation_width = (columns - 1) * x_spacing
        formation_height = (rows - 1) * y_spacing

        # Pick a random center, but keep the whole cluster on screen
        min_center_x = 80 + formation_width // 2
        max_center_x = settings.WIDTH - 80 - formation_width // 2

        if min_center_x > max_center_x:
            center_x = settings.WIDTH // 2
        else:
            center_x = random.randint(min_center_x, max_center_x)

        start_x = center_x - formation_width // 2
        start_y = random.randint(top_y, max(top_y, max_y - formation_height))

        for row in range(rows):
            for col in range(columns):
                if len(positions) >= count:
                    break

                jitter_x = random.randint(-10, 10)
                jitter_y = random.randint(-8, 8)

                x = start_x + col * x_spacing + jitter_x
                y = start_y + row * y_spacing + jitter_y

                positions.append((x, y))

        random.shuffle(positions)
        return positions

    def spawn_random_level(self):
        difficulty = self.endless_round

        basic_count = min(20, 5 + difficulty * 2)
        swarm_count = min(8, difficulty // 2)
        bomber_count = min(4, difficulty // 3)

        total_enemies = basic_count + swarm_count + bomber_count
        spawn_positions = self.get_spawn_positions(total_enemies)

        basic_frames = utils.load_spritesheet(
            sheet_name="enemy_basic.png",
            frame_width=66,
            frame_height=utils.FRAME_SIZE
        )

        swarm_frames = utils.load_spritesheet(
            sheet_name="enemy_swarm.png",
            frame_width=66,
            frame_height=utils.FRAME_SIZE
        )

        bomber_frames = utils.load_spritesheet(
            sheet_name="enemy_bomber.png",
            frame_width=66,
            frame_height=utils.FRAME_SIZE
        )

        for _ in range(basic_count):
            enemy = entities.Basic_Enemy(
                frames=basic_frames,
                start_pos=spawn_positions.pop()
            )
            self.enemy_ships.add(enemy)

        for _ in range(swarm_count):
            enemy = entities.Swarm_Enemy(
                frames=swarm_frames,
                start_pos=spawn_positions.pop()
            )
            self.enemy_ships.add(enemy)

        for _ in range(bomber_count):
            enemy = entities.Bomber_Enemy(
                frames=bomber_frames,
                start_pos=spawn_positions.pop()
            )
            self.enemy_ships.add(enemy)