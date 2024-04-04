from collections import deque
from typing import List
import heapq


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

    def __init__(self, name = "", wait_time = 0, running_time = 0, is_cpu_intensive = False, arrival_time = 0):
        ''' Stuff we get from part1:'''
        self.name = name
        self.is_cpu_intensive = is_cpu_intensive
        self.cpu_burst_times = deque([])
        self.io_burst_times = deque([])
        self.arrival_time = arrival_time
        ''' Stuff we compute in part2:'''
        self.wait_time = wait_time
        self.running_time = running_time
        self.turnarround_time = 0
        self.cpu_utilization = 0
        self.preemptions = 0
        self.hasRunIO = False
        self.estimatedNext = -1 
        self.actualLast = -1
        self.time_elapsed = 0
        self.updated_tau = 0
    
    def copy(self, p: 'Process'):
        p.name = self.name
        p.is_cpu_intensive = self.is_cpu_intensive
        p.cpu_burst_times = deque(list(self.cpu_burst_times))
        p.io_burst_times = deque(list(self.io_burst_times))
        p.wait_time = self.wait_time
        p.running_time = self.running_time
        p.turnarround_time = self.turnarround_time
        p.cpu_utilization = self.cpu_utilization
        p.arrival_time = self.arrival_time
        p.hasRunIO = self.hasRunIO
        p.estimatedNext = self.estimatedNext
        p.actualLast = self.actualLast
        p.time_elapsed = self.time_elapsed
        p.updated_tau = self.updated_tau
        return p


def copy_process_list(process_list):
    
    ret = []

    for p in process_list:
        new_p = Process()
        ret.append(p.copy(new_p))
        
    return ret



def print_ready_queue(q: List[Process]):
    ret = ''
    for p in q:
        ret += ' ' + p.name
        
    return ret


def print_heapq_ready_queue(q: List[Process]):

    if not q:
        return " <empty>"


    ret = ''
    copy = list(q)
    while copy:
        e, _, item = heapq.heappop(copy)
        ret += ' ' + item.name
    return ret




    