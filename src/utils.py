def bound(low: int, high: int, i: int):
    return min(max(i, low), high)


def multi_split(s: str, chars: str):
    split = []
    right = 0
    left = 0

    while left != len(s):
        if s[left] in chars:
            split.append(s[right:left])
            right = left+1
        
        left += 1
    
    split.append(s[right:left])
    
    return split


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

    def tick(self, dt):
        self.time += dt
        
        changed = False

        while self.time > self.periods[self.current_period] and self.current_period < len(self.periods):
            changed = True
            self.time -= self.periods[self.current_period]
            self.current_period += 1
            if self.current_period >= len(self.periods) and self.loop:
                self.current_period = 0
        
        return changed
