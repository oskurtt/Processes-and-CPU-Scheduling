from collections import deque
from typing import List
import heapq
import math


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


def get_three_digit_floot(num):
    return math.ceil(num*1000)/1000

class Stats:

    def __init__(self, algorithm="", cpu_util=0.0):
        self.algorithm = algorithm
        self.cpu_util = cpu_util
        self.cpu_burst_time = []
        self.avg_wait_time = [0, 0, 0]
        self.avg_turn_time = [0, 0, 0]
        self.num_context_switches = [0, 0, 0]
        self.num_prem = [0, 0, 0]

    def get_as_string(self):
        result = ""
        result += f"Algorithm {self.algorithm}\n"
        result += "-- CPU utilization: {:.3f}%\n".format(get_three_digit_floot(self.cpu_util))
        result += "-- average CPU burst time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n".format(get_three_digit_floot(self.cpu_burst_time[0]), get_three_digit_floot(self.cpu_burst_time[1]), get_three_digit_floot(self.cpu_burst_time[2]))
        result += "-- average wait time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n".format(get_three_digit_floot(self.avg_wait_time[0]), get_three_digit_floot(self.avg_wait_time[1]), get_three_digit_floot(self.avg_wait_time[2]))
        result += "-- average turnaround time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n".format(get_three_digit_floot(self.avg_turn_time[0]), get_three_digit_floot(self.avg_turn_time[1]), get_three_digit_floot(self.avg_turn_time[2]))
        result += f"-- number of context switches: {self.num_context_switches[0]} ({self.num_context_switches[1]}/{self.num_context_switches[2]})\n"
        result += f"-- number of preemptions: {self.num_prem[0]} ({self.num_prem[1]}/{self.num_prem[2]})\n"
        return result

    

def get_avg(input_dict, denom):
    total_bursts = denom
    total_duration = 0

    for bursts in input_dict.values():
        # Extract bursts for each process
        process_bursts = [bursts[i:i+2] for i in range(0, len(bursts), 2)]

        # Calculate total bursts and total duration for the process
        total_duration += sum(end - start for start, end in process_bursts)

    # Calculate the average burst duration across all processes
    if total_bursts != 0:
        average_burst_duration = total_duration / total_bursts
    else:
        average_burst_duration = 0  # Avoid division by zero if there are no bursts

    #print(total_bursts)
    return average_burst_duration


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




# def print_stats(algorithm_name, cpu_util, avg_burst_time_num, avg_burst_time_denom, avg_wait_time_num, avg_wait_time_denom,avg_turn_time_num, avg_turn_time_denom, num_context_switches, num_prem):

#     print(f"Algorithm {algorithm_name}")
#     print(f"-- CPU utilization: {:.3f}%".formate(cpu_util))
#     print(f"-- average CPU burst time: {:.3f} ms ({:3f} ms/{:.3f} ms)".format(avg_burst_time_num/avg_burst_time_denom, avg_burst_time_num, avg_burst_time_denom))
#     print(f"-- average wait time: {:.3f} ms ({:.3f} ms/{:.3f} ms)".format(avg_wait_time_num/avg_wait_time_denom, avg_wait_time_num, avg_wait_time_denom))
#     print("-- average turnaround time: {:.3f} ms ({:.3f} ms/{:.3f} ms)".format(avg_turn_time_num/avg_turn_time_denom, avg_turn_time_num, avg_turn_time_denom))

    

# -- number of context switches: 89 (60/29)
# -- number of preemptions: 0 (0/0)


def calculate_statistics(fcfs_param, sjf_param, srt_param, rr_param):

    print_algo(fcfs_param[0], fcfs_param[1], fcfs_param[2], fcfs_param[3], fcfs_param[4], fcfs_param[5], fcfs_param[6])
    print()

    print(sjf_param[0], sjf_param[1], sjf_param[2], sjf_param[3], sjf_param[4], sjf_param[5], sjf_param[6])
    print()


    print(srt_param[0], srt_param[1], srt_param[2], srt_param[3], srt_param[4], srt_param[5], srt_param[6])
    print()

    print(rr_param[0], rr_param[1], rr_param[2], rr_param[3], rr_param[4], rr_param[5], rr_param[6])
    print()




    """
    rt    


srt


Algorithm SJF
-- CPU utilizatirr_param[0], rr_param[1], rr_param[2], rr_param[3], rr_param[4], rr_param[5], rr_param[6]on: 84.062%
-- average CPU burst time: 3067.776 ms (4071.000 ms/992.138 ms)
-- average wait time: 804.540 ms (229.584 ms/1994.104 ms)
-- average turnaround time: 3876.315 ms (4304.584 ms/2990.242 ms)
-- number of context switches: 89 (60/29)
-- number of preemptions: 0 (0/0)

Algorithm SRT
-- CPU utilization: 83.112%
-- average CPU burst time: 3067.776 ms (4071.000 ms/992.138 ms)
-- average wait time: 542.686 ms (290.800 ms/1063.828 ms)
-- average turnaround time: 3614.911 ms (4366.467 ms/2059.966 ms)
-- number of context switches: 99 (70/29)
-- number of preemptions: 10 (10/0)

Algorithm RR
-- CPU utilization: 81.436%
-- average CPU burst time: 3067.776 ms (4071.000 ms/992.138 ms)
-- average wait time: 588.686 ms (398.067 ms/983.069 ms)
-- average turnaround time: 3668.236 ms (4479.134 ms/1990.518 ms)
-- number of context switches: 262 (151/111)
-- number of preemptions: 173 (91/82)


    """

