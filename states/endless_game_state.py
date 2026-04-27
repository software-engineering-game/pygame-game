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

    def spawn_random_level(self):
        difficulty = self.endless_round

        basic_count = min(20, 5 + difficulty * 2)
        swarm_count = min(8, difficulty // 2)
        bomber_count = min(4, difficulty // 3)

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
                start_pos=(
                    random.randint(80, settings.WIDTH - 80),
                    random.randint(60, 260)
                )
            )
            self.enemy_ships.add(enemy)

        for _ in range(swarm_count):
            enemy = entities.Swarm_Enemy(
                frames=swarm_frames,
                start_pos=(
                    random.randint(80, settings.WIDTH - 80),
                    random.randint(80, 320)
                )
            )
            self.enemy_ships.add(enemy)

        for _ in range(bomber_count):
            enemy = entities.Bomber_Enemy(
                frames=bomber_frames,
                start_pos=(
                    random.randint(100, settings.WIDTH - 100),
                    random.randint(70, 240)
                )
            )
            self.enemy_ships.add(enemy)