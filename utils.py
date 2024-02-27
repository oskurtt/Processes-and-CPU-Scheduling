class Rand48(object):
    #This code is borrowed from https://stackoverflow.com/questions/7287014/is-there-any-drand48-equivalent-in-python-or-a-wrapper-to-it
    def __init__(self):
        self.n = 0
    def seed(self, seed):
        self.n = seed
    def srand(self, seed):
        self.n = (seed << 16) + 0x330e
    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n
    def drand(self):
        return self.next() / 2**48
    # def lrand(self):
    #     return self.next() >> 17
    # def mrand(self):
    #     n = self.next() >> 16
    #     if n & (1 << 31):
    #         n -= 1 << 32
    #     return n 


class Process:

    def __init__(self, name = "", wait_time = 0, running_time = 0, is_cpu_intensive = False):
        self.name = name
        self.wait_time = wait_time
        self.running_time = running_time
        self.is_cpu_intensive = is_cpu_intensive
        self.cpu_burst_times = []
        self.io_burst_times = []
        self.turnarround_time = 0
        self.wait_time = 0
        self.cpu_utilization = 0




    