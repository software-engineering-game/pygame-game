import pygame
from states import settings
from states import utils
from states.base_state import State

ENEMY_ORDER = ("Basic_Enemy", "Swarm_Enemy", "Bomber_Enemy")

LINE_SLOT = 0
LINE_BG = 1
LINE_WAVE = 2
LINE_ENEMY = 3
LINE_COLS = 4
LINE_ROWS = 5
LINE_ADD = 6
LINE_REMOVE = 7
LINE_SAVE = 8
LINE_TEST = 9
LINE_BACK = 10

NUM_LINES = 11


def _enemy_label(enemy_type: str) -> str:
    return enemy_type.replace("_Enemy", "").replace("_", " ")


def _enemy_order_index(enemy_type: str) -> int:
    try:
        return ENEMY_ORDER.index(enemy_type)
    except ValueError:
        return 0


class CustomLevelState(State):
    def __init__(self, previous_state=None):
        self.previous_state = previous_state

    def on_enter(self, app):
        self.menu_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 20)
        self.small_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 14)

        utils.ensure_custom_levels_dir()
        self.edit_slot = max(
            utils.CUSTOM_LEVEL_SLOT_MIN,
            min(utils.CUSTOM_LEVEL_SLOT_MAX, getattr(self, "edit_slot", 1)),
        )
        self._reload_from_slot()

        self.selected = LINE_SLOT
        self.notice = None
        self.notice_timer = 0.0

    def _reload_from_slot(self):
        path = utils.path_for_custom_slot(self.edit_slot)
        loaded, _ = utils.load_custom_level_from_path(path)
        if loaded is not None:
            self.bg_img, self.waves = utils.editor_model_from_level_dict(loaded)
        else:
            template = utils.default_custom_level_dict()
            self.bg_img, self.waves = utils.editor_model_from_level_dict(template)
        if self.waves:
            self.edit_wave = max(
                0, min(getattr(self, "edit_wave", 0), len(self.waves) - 1)
            )
        else:
            self.edit_wave = 0

    def _current_wave(self):
        return self.waves[self.edit_wave]

    def _level_dict_for_save(self):
        return utils.editor_model_to_level_dict(self.waves, self.bg_img)

    def _slot_path(self):
        return utils.path_for_custom_slot(self.edit_slot)

    def handle_event(self, app, event):
        if event.type != pygame.KEYDOWN:
            return

        sfx_menu = pygame.mixer.Sound("assets/sfx_ogg/menu1.ogg")

        def play_menu():
            if settings.SFX_ON:
                pygame.mixer.Sound.play(sfx_menu)

        if event.key == pygame.K_ESCAPE:
            from states.main_menu_state import MainMenuState

            app.change_state(MainMenuState())
            return

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % NUM_LINES
            play_menu()
            return

        if event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % NUM_LINES
            play_menu()
            return

        w = self._current_wave()

        if event.key == pygame.K_LEFT:
            if self.selected == LINE_SLOT:
                self.edit_slot = (
                    utils.CUSTOM_LEVEL_SLOT_MAX
                    if self.edit_slot <= utils.CUSTOM_LEVEL_SLOT_MIN
                    else self.edit_slot - 1
                )
                self._reload_from_slot()
                play_menu()
                return
            if self.selected == LINE_BG:
                opts = list(utils.CUSTOM_BACKGROUND_OPTIONS)
                i = opts.index(self.bg_img) if self.bg_img in opts else 0
                self.bg_img = opts[(i - 1) % len(opts)]
                play_menu()
            elif self.selected == LINE_WAVE:
                self.edit_wave = (self.edit_wave - 1) % len(self.waves)
                play_menu()
            elif self.selected == LINE_ENEMY:
                order = list(ENEMY_ORDER)
                i = _enemy_order_index(w["enemy_type"])
                w["enemy_type"] = order[(i - 1) % len(order)]
                play_menu()
            elif self.selected == LINE_COLS:
                w["cols"] = max(1, w["cols"] - 1)
                play_menu()
            elif self.selected == LINE_ROWS:
                w["rows"] = max(1, w["rows"] - 1)
                play_menu()
            return

        if event.key == pygame.K_RIGHT:
            if self.selected == LINE_SLOT:
                self.edit_slot = (
                    utils.CUSTOM_LEVEL_SLOT_MIN
                    if self.edit_slot >= utils.CUSTOM_LEVEL_SLOT_MAX
                    else self.edit_slot + 1
                )
                self._reload_from_slot()
                play_menu()
                return
            if self.selected == LINE_BG:
                opts = list(utils.CUSTOM_BACKGROUND_OPTIONS)
                i = opts.index(self.bg_img) if self.bg_img in opts else 0
                self.bg_img = opts[(i + 1) % len(opts)]
                play_menu()
            elif self.selected == LINE_WAVE:
                self.edit_wave = (self.edit_wave + 1) % len(self.waves)
                play_menu()
            elif self.selected == LINE_ENEMY:
                order = list(ENEMY_ORDER)
                i = _enemy_order_index(w["enemy_type"])
                w["enemy_type"] = order[(i + 1) % len(order)]
                play_menu()
            elif self.selected == LINE_COLS:
                w["cols"] = min(8, w["cols"] + 1)
                play_menu()
            elif self.selected == LINE_ROWS:
                w["rows"] = min(4, w["rows"] + 1)
                play_menu()
            return

        if event.key == settings.keybind_menu_confirm:
            if self.selected == LINE_ADD:
                if len(self.waves) < 4:
                    self.waves.append(
                        {"enemy_type": "Basic_Enemy", "cols": 3, "rows": 2}
                    )
                    self.edit_wave = len(self.waves) - 1
                    self.notice = "Wave added"
                    self.notice_timer = 2.0
                play_menu()
            elif self.selected == LINE_REMOVE:
                if len(self.waves) > 1:
                    self.waves.pop(self.edit_wave)
                    self.edit_wave = min(self.edit_wave, len(self.waves) - 1)
                    self.notice = "Wave removed"
                    self.notice_timer = 2.0
                play_menu()
            elif self.selected == LINE_SAVE:
                try:
                    utils.save_custom_level_to_path(
                        self._level_dict_for_save(), self._slot_path()
                    )
                    self.notice = "Saved slot {}".format(self.edit_slot)
                    self.notice_timer = 3.0
                except ValueError as e:
                    self.notice = str(e)
                    self.notice_timer = 3.0
                play_menu()
            elif self.selected == LINE_TEST:
                try:
                    utils.save_custom_level_to_path(
                        self._level_dict_for_save(), self._slot_path()
                    )
                    from states.game_state import GameState

                    app.change_state(GameState(custom_level_path=self._slot_path()))
                except ValueError as e:
                    self.notice = str(e)
                    self.notice_timer = 3.0
                    play_menu()
            elif self.selected == LINE_BACK:
                from states.main_menu_state import MainMenuState

                app.change_state(MainMenuState())
                play_menu()

    def update(self, app, dt):
        if self.notice_timer > 0:
            self.notice_timer -= dt
            if self.notice_timer <= 0:
                self.notice = None

    def draw(self, app, screen):
        screen.fill((10, 10, 24))
        title = self.menu_font.render("Make Your Level", True, (255, 255, 100))
        screen.blit(title, (40, 24))

        w = self._current_wave()
        lines = [
            (LINE_SLOT, "Edit slot: {} (1-8)".format(self.edit_slot)),
            (LINE_BG, f"Background: {self.bg_img}"),
            (LINE_WAVE, f"Editing wave: {self.edit_wave + 1} / {len(self.waves)}"),
            (LINE_ENEMY, f"Enemy type: {_enemy_label(w['enemy_type'])}"),
            (LINE_COLS, f"Columns: {w['cols']}"),
            (LINE_ROWS, f"Rows: {w['rows']}"),
            (LINE_ADD, "Add wave (max 4)"),
            (LINE_REMOVE, "Remove this wave"),
            (LINE_SAVE, "Save to file"),
            (LINE_TEST, "Save and test play"),
            (LINE_BACK, "Back to menu"),
        ]

        y = 80
        for line_id, text in lines:
            sel = line_id == self.selected
            prefix = "> " if sel else "  "
            color = (255, 255, 255) if sel else (180, 180, 200)
            surf = self.menu_font.render(prefix + text, True, color)
            screen.blit(surf, (40, y))
            y += 36

        if self.notice:
            n = self.small_font.render(self.notice, True, (120, 255, 160))
            screen.blit(n, (40, app.height - 80))

        hint = self.small_font.render(
            "Up/Down: line  Left/Right: change  Enter: action  Esc: menu",
            True,
            (140, 140, 160),
        )
        screen.blit(hint, (40, app.height - 48))
