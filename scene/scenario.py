class Scenario:
    """
    Radar scene containing multiple targets.
    """

    def __init__(self, targets=None):
        self.targets = targets if targets is not None else []
        self.time = 0.0

    def add_target(self, target):
        self.targets.append(target)

    def step(self, dt):
        """
        Advance scene time.
        """
        for tgt in self.targets:
            tgt.propagate(dt)
        self.time += dt

    def get_targets(self):
        """
        Return list of target states for signal generator.
        """
        return [t.get_state() for t in self.targets]

    def __len__(self):
        return len(self.targets)
