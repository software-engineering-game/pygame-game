import os
import sys
import json
import tempfile
import pygame

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

os.chdir(PROJECT_ROOT)

from states import utils

pygame.init()
pygame.display.set_mode((1, 1))


def test_validate_level_dict_rejects_non_dict():
    ok, err = utils.validate_level_dict([])
    assert ok is False
    assert err is not None


def test_validate_level_dict_rejects_empty_waves():
    ok, err = utils.validate_level_dict({"bg_img": "background_asteroids.png", "waves": []})
    assert ok is False


def test_validate_level_dict_accepts_minimal_valid():
    level = utils.default_custom_level_dict()
    ok, err = utils.validate_level_dict(level)
    assert ok is True
    assert err is None


def test_editor_model_roundtrip():
    bg = "background_test.png"
    waves = [
        {"enemy_type": "Swarm_Enemy", "cols": 4, "rows": 1},
        {"enemy_type": "Bomber_Enemy", "cols": 2, "rows": 2},
    ]
    level_dict = utils.editor_model_to_level_dict(waves, bg)
    ok, err = utils.validate_level_dict(level_dict)
    assert ok is True

    bg2, waves2 = utils.editor_model_from_level_dict(level_dict)
    assert bg2 == bg
    assert len(waves2) == 2
    assert waves2[0]["enemy_type"] == "Swarm_Enemy"
    assert waves2[0]["cols"] == 4
    assert waves2[1]["rows"] == 2


def test_build_level_from_dict_spawns_enemies():
    level = utils.default_custom_level_dict()
    group = pygame.sprite.Group()
    utils.build_level_from_dict(level, group, level_label="test")
    assert len(group.sprites()) > 0


def test_load_custom_level_from_temp_file():
    data = utils.default_custom_level_dict()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
        json.dump(data, f)

    try:
        loaded, err = utils.load_custom_level_from_path(path)
        assert err is None
        assert loaded is not None
        assert loaded["bg_img"] == data["bg_img"]
    finally:
        os.unlink(path)


def test_friendly_name_for_slot_path():
    assert utils.friendly_name_for_custom_path("/x/custom_levels/slot_03.json") == "Slot 3"


def test_list_valid_custom_level_paths_respects_directory(tmp_path):
    old_dir = utils.CUSTOM_LEVELS_DIR
    utils.CUSTOM_LEVELS_DIR = str(tmp_path)
    # Block legacy migration into this tmp dir (would copy repo custom_level.json).
    (tmp_path / "slot_01.json").write_text("{}")
    try:
        assert utils.list_valid_custom_level_paths() == []
        bad = tmp_path / "bad.json"
        bad.write_text('{"not": "valid"}')
        assert utils.list_valid_custom_level_paths() == []
        good_path = tmp_path / "slot_01.json"
        data = utils.default_custom_level_dict()
        good_path.write_text(json.dumps(data))
        paths = utils.list_valid_custom_level_paths()
        assert len(paths) == 1
        assert os.path.basename(paths[0]) == "slot_01.json"
    finally:
        utils.CUSTOM_LEVELS_DIR = old_dir


def test_save_custom_level_writes_valid_json():
    data = utils.default_custom_level_dict()
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "custom_level.json")
        utils.save_custom_level_to_path(data, path)
        with open(path, "r", encoding="utf-8") as f:
            roundtrip = json.load(f)
        ok, _ = utils.validate_level_dict(roundtrip)
        assert ok is True
