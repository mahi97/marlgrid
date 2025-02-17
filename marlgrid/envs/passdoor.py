from ..base import MultiGridEnv, MultiGrid
from ..objects import *


class PassMultiGrid(MultiGridEnv):
    mission = "get to the green square"
    metadata = {}

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = MultiGrid((width, height))

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place a goal in the bottom-right corner
        # self.put_obj(Goal(color="green", reward=1), width - 2, height - 2)

        # Create a vertical splitting wall
        # splitIdx = self._rand_int(2, width - 2)
        splitIdx = width // 2
        self.grid.vert_wall(splitIdx, 0)

        # Place the agent at a random position and orientation
        # on the left side of the splitting wall
        # self.place_agent(size=(splitIdx, height))

        # Place a door in the wall
        # doorIdx = self._rand_int(1, width - 2)
        doorIdx = width // 2 - 3
        d1 = Door(color="yellow", state=Door.states.locked)
        self.put_obj(d1, splitIdx, doorIdx)

        doorIdx = width // 2 + 3
        d2 = Door(color="red", state=Door.states.locked)
        self.put_obj(d2, splitIdx, doorIdx)

        # Place a yellow key on the left side
        # self.place_obj(obj=Key("yellow"), top=(0, 0), size=(splitIdx, height))

        b1 = Button("yellow")
        b2 = Button("red")
        self.place_obj(obj=b1, top=(width // 4, height - 5), size=(3, 3))
        self.place_obj(obj=b2, top=(3 * width // 4 - 3, 5), size=(3, 3))

        self.agent_spawn_kwargs = {'top': (0, 0), 'size': (width // 2, height // 2)}

        b1.signal.connect(d2.switch)
        b2.signal.connect(d1.switch)

        s1 = Switch("yellow")
        self.place_obj(obj=s1, top=(width // 4, height - 5), size=(3, 3))
        s2 = Switch("red")
        self.place_obj(obj=s2, top=(3 * width // 4 - 3, 5), size=(3, 3))
        s1.signal.connect(d2.switch)
        s2.signal.connect(d1.switch)

    def done(self):
        cnt = 0
        for agent in self.agents:
            if agent.pos[0] > self.width // 2 + 1:
                cnt += 1
        return cnt >= 2

    def reward(self):
        cnt = 0
        for agent in self.agents:
            if agent.pos[0] > self.width // 2:
                cnt += 1
        return cnt >= 2 * 1000
