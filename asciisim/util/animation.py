import time

def milliseconds():
    return time.time_ns() // 1000000

class Animation(object):
    def __init__(self, frames: int, frame_ms: int, total_ms: int = 0):
        self.current_frame = 0
        self.frames = frames
        self.frame_ms = frame_ms
        self.last_frame = 0
        self.started = 0
        self.total_ms = total_ms

    @property
    def progress(self):
        if not self.total_ms:
            return 1
        
        ms = milliseconds()
        anim_progress =  (ms - self.started) / self.total_ms

        return min(anim_progress, 1)
        
        
    def start(self):
        ms = milliseconds()
        self.current_frame = 0
        self.last_frame = ms
        self.started = ms
    
    def update(self):
        ms = milliseconds()

        if self.total_ms and ms - self.started > self.total_ms:
            return

        if ms - self.last_frame < self.frame_ms:
            return

        self.last_frame = ms

        if self.current_frame == self.frames - 1:
            self.current_frame = 0
        else:
            self.current_frame += 1
