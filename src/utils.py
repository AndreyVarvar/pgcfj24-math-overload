def bound(low: int, high: int, i: int):
    return min(max(i, low), high)


class Timer():
    def __init__(self, 
                 periods: list[int],
                 loop: bool):
        self.periods = periods

        if len(periods) == 0:
            raise Exception("Timer must have at least 1 period")

        self.loop = loop

        self.time = 0
        self.current_period = 0

        self.percent = 0

    def tick(self, dt):
        self.time += dt
        self.percent = self.time / self.periods[self.current_period]
        
        changed = False

        while self.current_period < len(self.periods) and self.time > self.periods[self.current_period]:
            changed = True
            self.time -= self.periods[self.current_period]
            self.current_period += 1
            if self.current_period >= len(self.periods) and self.loop:
                self.current_period = 0
        
        return changed

    def reset(self):
        self.current_period = 0
        self.time = 0


def smoothstep(goal, pos, dt):
    pass
