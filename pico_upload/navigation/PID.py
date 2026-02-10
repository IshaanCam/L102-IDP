import utime
class PID:
    def __init__ (self, Kp, Ki, Kd, output_limits = (-100, 100)):
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.min_out, self.max_out = output_limits
        self.I = 0.0
        self.e_prev = 0
        self.t_prev = utime.ticks_ms()
        # self.t_prev = int(utime.time() * 1000)
    
    def update(self, e):
        t = utime.ticks_ms()
        # t = int(utime.time() * 1000)
        dt = utime.ticks_diff(t, self.t_prev) / 1000.0   # dividing by 1000 to convert to seconds
        # dt = (t - self.t_prev) / 1000
        self.t_prev = t
        if dt <= 0:
            dt = 0.001  # protection from divide by 0 error
        
        self.I += e * dt
        D = (e - self.e_prev) / dt
        self.e_prev = e

        update = self.Kp * e + self.Ki * self.I + self.Kd * D

        if update < self.min_out: 
            return self.min_out
        if update > self.max_out:
            return self.max_out
        return update
