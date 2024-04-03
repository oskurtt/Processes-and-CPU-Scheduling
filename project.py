import sys
import random
import math
import string
from utils import Rand48
from utils import Process
import heapq
from collections import deque
from typing import List


rand48 = Rand48()
alpahbet = string.ascii_uppercase


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



def fcfs(original_processes, tcs):
    time = 0
    #Copy the processes:
    processes = copy_process_list(original_processes)

    all = []
    ready = deque([])

    for p in processes:
        heapq.heappush(all, (p.arrival_time, p.name, p))
        
    print("time 0ms: Simulator started for FCFS [Q <empty>]")


    while (all or ready):
        #If running queue is empty:
            #Pop the next proccess and jump to that arrival time
        #Else, after finishing current process, pick next thing in waiting queue
        
        if (not ready):
            _, _, p = heapq.heappop(all)
            ready.append(p)
            time = p.arrival_time #Since nothing is in the waiting_queue, jump ahead to the next arrival time
            #time += tcs//2
            print(f"time {time}ms: Process {p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
            p.hasRunIO = True
            #time += p.cpu_burst_times[0]            

        time += tcs//2
        p = ready.popleft()
        cpu_runtime = p.cpu_burst_times.popleft()
        if not ready:
            print(f"time {time}ms: Process {p.name} started using the CPU for {cpu_runtime}ms burst [Q <empty>]")
        else:
            print(f"time {time}ms: Process {p.name} started using the CPU for {cpu_runtime}ms burst [Q{print_ready_queue(ready)}]")
        time += cpu_runtime

        #Update this process: Add back to all queue or finish
        if p.cpu_burst_times:

            #Add this process back to the all queue with updated arrival time
            p.arrival_time = time + p.io_burst_times.popleft()+tcs//2
            heapq.heappush(all, (p.arrival_time, p.name, p))


        while all:
            _, _, next_p = all[0]
    
            if next_p.arrival_time < time:
                
                ready.append(next_p)
                heapq.heappop(all)

                if not next_p.hasRunIO:
                    print(f"time {next_p.arrival_time}ms: Process {next_p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
                    next_p.hasRunIO = True
                else:
                    print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")
                    
            else:
                break

        if len(p.cpu_burst_times) == 0:
            if not ready:
                print(f"time {time}ms: Process {p.name} terminated [Q <empty>]")
            else:
                print(f"time {time}ms: Process {p.name} terminated [Q{print_ready_queue(ready)}]")


        elif not ready:
            print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} bursts to go [Q <empty>]")
            print(f"time {time}ms: Process {p.name} switching out of CPU; blocking on I/O until time {p.arrival_time}ms [Q <empty>]")
        else:
            print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} bursts to go [Q{print_ready_queue(ready)}]")
            print(f"time {time}ms: Process {p.name} switching out of CPU; blocking on I/O until time {p.arrival_time}ms [Q{print_ready_queue(ready)}]")

        time += tcs//2

    print(f"time {time}ms: Simulator ended for FCFS [Q <empty>]")

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

    print("\n<<< PROJECT PART II -- t_cs=6ms; alpha=0.90; t_slice=128ms >>>")
    fcfs(processes, tcs)
    # sjf()
    # srt()
    # rr()

    
main()
