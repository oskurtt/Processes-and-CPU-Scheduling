import sys
import random
import math
import string
from utils import Rand48
from utils import Process
import heapq

rand48 = Rand48()
alpahbet = string.ascii_uppercase


def copy_process_list(process_list):
    
    ret = []

    for p in process_list:
        new_p = Process()
        ret.append(p.copy(new_p))
        
    return ret


def fcfs(original_processes, tcs):
    time = 0
    #Copy the processes:
    processes = copy_process_list(original_processes)

    time = 0

    all = []
    waiting = []

    for p in processes:
        heapq.heappush(all, (p.arrival_time, p.name, p))
        
    print("time 0ms: Simulator started for FCFS [Q <empty>]")



    while (pq):

        #If running queue is empty:
            #Pop the next proccess and jump to that arrival time
        #Else, after finishing current process, pick next thing in waiting queue

        p_time, name, p = heapq.heappop(pq)
        if (len(waiting) == 0):
            time = p_time #Since nothing is in the waiting_queue, jump ahead to the next arrival time
            time += tcs//2
            #Add back to queue with new arrival time = 
        else:
            time += p.next_

        #Check if there is anything to add to waiting_queue



        time += tcs//2

    return time



def next_exp(lamda, upper_bound):
    iterations = 1000000
    i = 0
    while i < iterations:
        r = rand48.drand()
        x = (- (math.log(r)) / lamda)

        if ( x > upper_bound ):
            continue
        i += 1

        return x

    
def main():

    processes = []

    """
    FIRST PART START

    """
    try:
        n = int(sys.argv[1])
        ncpu = int(sys.argv[2])
        seed = int(sys.argv[3])
        lamda = float(sys.argv[4])
        upper_bound = int(sys.argv[5])
        tcs = int(sys.argv[6])
        alpha = float(sys.argv[7])
        t_slice = int(sys.argv[8])

    except Exception as e:
        print(f"ERROR: {e}")
        return 0
    
    rand48.srand(seed)
    if (ncpu > 1 or ncpu == 0):
        print(f"<<< PROJECT PART I -- process set (n={n}) with {ncpu} CPU-bound processes >>>")
    else:
        print(f"<<< PROJECT PART I -- process set (n={n}) with {ncpu} CPU-bound process >>>")

    for i in range(n):

        #initialize an empty process class

        process = Process()
        process.name = alpahbet[i]
        
        arrival_time = math.floor(next_exp(lamda, upper_bound))
        process.arrival_time = arrival_time

        num_cpu_burst = math.ceil(rand48.drand()*64)

        if i < (n - ncpu):
            print(f"I/O-bound process {alpahbet[i]}: arrival time {arrival_time}ms; {num_cpu_burst} CPU bursts")
            process.is_cpu_intensive = True
        else:
            print(f"CPU-bound process {alpahbet[i]}: arrival time {arrival_time}ms; {num_cpu_burst} CPU bursts")
            process.is_cpu_intensive = False

        
        for j in range(num_cpu_burst):
            cpu_burst_time = math.ceil(next_exp(lamda, upper_bound))
                
            if j != num_cpu_burst - 1:
                io_burst_time = math.ceil(next_exp(lamda, upper_bound)) * 10

            if not (i < (n - ncpu)):
                cpu_burst_time = cpu_burst_time*4
                io_burst_time = math.floor(io_burst_time/8)
            
            #print()
            # if (j == num_cpu_burst - 1):
            #     #print(f"--> CPU burst {cpu_burst_time}ms", end = '')
            # else:
            if (j < num_cpu_burst - 1):
                #print(f"--> CPU burst {cpu_burst_time}ms --> I/O burst {io_burst_time}ms", end = '')
                process.io_burst_times.append(io_burst_time)
            process.cpu_burst_times.append(cpu_burst_time)

        #print()
        processes.append(process)


    """
    FIRST PART ENDED

    """

    #print("Part2")


    fcfs(processes, tcs)
    # sjf()
    # srt()
    # rr()

    
main()
