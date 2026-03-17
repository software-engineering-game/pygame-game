from states import game_state
"""
level
   background
   enemy types
   waves
      wave 1
         shape of waves
      wave 2
      etc
   boss fights
   possible upgrades
"""

test_level = {
   "level_num":         -666,
   "bg_img":            "asteroid_background.png",
   "enemy_types":       [game_state.Basic_Enemy, game_state.Bomber_Enemy],
   "sprite_sheets":     ["enemy_basic.png", "enemy_bomber.png"],
   "wave_position":     (12, 4),
   "wave_size":         ()
}


first_wave = {
   "level_num":         1,
   "bg_img":            "asteroid_background.png",
   "enemy_types":       [game_state.Basic_Enemy],
   "sprite_sheets":     ["enemy_basic.png", "enemy_bomber.png"],
   "wave_position":     (12, 4),
   "wave_size":         (6,2)
}

# Level for showcasing the swarm enemy type
swarm_wave = {
   "level_num":         1,
   "bg_img":            "asteroid_background.png",
   "enemy_types":       [game_state.Basic_Enemy],
   "sprite_sheets":     ["enemy_basic.png", "enemy_bomber.png"],
   "wave_position":     (12, 4),
   "wave_size":         (6,2)
}
