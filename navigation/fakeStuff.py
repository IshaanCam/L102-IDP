import threading
import time

class FakeTimer:
    PERIODIC = 0

    def __init__(self, id, mode, callback, freq):
        self.callback = callback
        self.period = 1 / freq
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        while self.running:
            time.sleep(self.period)
            self.callback(self)

    def deinit(self):
        self.running = False

class FakeLineSensor:
    def __init__(self, pattern):
        self.pattern = pattern
        self.i = 0

    def read_value(self):
        val = self.pattern[self.i % len(self.pattern)]
        self.i += 1
        return val

class FakeJunctionSensor:
    def __init__(self, sequence):
        self.sequence = sequence
        self.i = 0

    def read_value(self):
        val = self.sequence[self.i]
        self.i += 1
        return val

class FakeMotor:
    def __init__(self, name):
        self.name = name
        self.speed = 0

    def Forward(self, speed):
        self.speed = speed
        print(f"[MOTOR {self.name}] Forward {speed}")

    def Stop(self):
        self.speed = 0
        print(f"[MOTOR {self.name}] Stop")