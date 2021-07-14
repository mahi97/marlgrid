from marlgrid.utils.video import GridRecorder
from marlgrid.envs import env_from_config, registered_envs


env_config = {
    "env_class": "PassMultiGrid",
    "grid_size": 31,
    "max_steps": 250,
    # "clutter_density": 0.15,
    # "respawn": True,
    # "ghost_mode": True,
    # "reward_decay": False,
    # "n_bonus_tiles": 3,
    # "initial_reward": True,
    # "penalty": -1.5
}

player_interface_config = {
    "view_size": 7,
    "view_offset": 1,
    "view_tile_size": 11,
    "observe_position": True,
    "observe_orientation": True,
    "observation_style": "rich",
    "see_through_walls": False,
    "color": "prestige"
}

# Add the player/agent config to the environment config (as expected by "env_from_config" below)
env_config['agents'] = [player_interface_config, player_interface_config]


if __name__ == '__main__':
    env = env_from_config(env_config)
    env.max_steps = 400

    env = GridRecorder(env, render_kwargs={"tile_size": 11}, save_root='./')

    obs = env.reset()
    env.recording = True

    count = 0
    done = False

    while not done:
        act = env.action_space.sample()
        obs, rew, done, _ = env.step(act)
        count += 1

    env.export_video("test_minigrid.mp4")
