from utils import copy_process_list, print_heapq_ready_queue, Stats
import heapq
from collections import deque
import math

import struct
import math


## converts a double precision python "float" into a single precision c "float" and back again
def c_float(x):
    return struct.unpack("f", struct.pack("f",float(x)))[0]

def sjf(original_processes, tcs, alpha, lamda):

    stats = Stats()
    stats.algorithm = "SJF"

    time = 0
    #Copy the processes:
    processes = copy_process_list(original_processes)

    #statistics:


    all = []
    ready = deque([])

    # Calculate the avg burst times
    all_bursts = []
    cpu_bursts = []
    io_bursts = []
    for p in processes:
        heapq.heappush(all, (p.arrival_time, p.name, p))
        for burst_time in p.cpu_burst_times:
            if p.is_cpu_intensive:
                cpu_bursts.append(burst_time)
            else:
                io_bursts.append(burst_time)
            all_bursts.append(burst_time)
    try:
        stats.cpu_burst_time.append(sum(all_bursts)/len(all_bursts))
    except:
        stats.cpu_burst_time.append(0)

    try:
        stats.cpu_burst_time.append(sum(io_bursts)/len(io_bursts))
    except:
        stats.cpu_burst_time.append(0)

    try:
        stats.cpu_burst_time.append(sum(cpu_bursts)/len(cpu_bursts))
    except:
        stats.cpu_burst_time.append(0)
    time = 0
    #Copy the processes:
    processes = copy_process_list(original_processes)

    for proc in processes:
        proc.estimatedNext = math.ceil(c_float(1/lamda))
        #proc.estimatedNext = c_float(1/lamda)
        #proc.estimatedNext = math.ceil(1/lamda)

    all = []
    ready = []

    for p in processes:
        heapq.heappush(all, (p.arrival_time, p.name, p))
        
    print("time 0ms: Simulator started for SJF [Q <empty>]")


    while (all or ready):
        #If running queue is empty:
            #Pop the next proccess and jump to that arrival time
        #Else, after finishing current process, pick next thing in waiting queue
        
        if (not ready):
            _, _, p = heapq.heappop(all)

            heapq.heappush(ready, (p.estimatedNext, p.name, p))
             
            time = p.arrival_time #Since nothing is in the waiting_queue, jump ahead to the next arrival time
            #time += tcs//2
            if not p.hasRunIO:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) arrived; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
                p.hasRunIO = True
            else:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) completed I/O; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
            #time += p.cpu_burst_times[0]  

        while all:
            _, _, next_p = all[0]
        
            if next_p.arrival_time <= time:
                
                #ready.append(next_p)
                heapq.heappush(ready, (next_p.estimatedNext, next_p.name, next_p))
                heapq.heappop(all)

                if not next_p.hasRunIO:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) arrived; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
                    next_p.hasRunIO = True
                else:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) completed I/O; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
                    
            else:
                break          

        time += tcs//2
        if p.is_cpu_intensive:
            stats.num_context_switches[1] += 1
        else:
            stats.num_context_switches[2] += 1
        stats.num_context_switches[0] += 1
        #p = ready.popleft()
        _, _, p = heapq.heappop(ready)


        while all:
            _, _, next_p = all[0]
        
            if next_p.arrival_time <= time:
                
                #ready.append(next_p)
                heapq.heappush(ready, (next_p.estimatedNext, next_p.name, next_p))
                heapq.heappop(all)

                if not next_p.hasRunIO:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) arrived; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
                    next_p.hasRunIO = True
                else:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) completed I/O; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
                    
            else:
                break

        cpu_runtime = p.cpu_burst_times.popleft()
        if not ready:
            if time < 10000:
                print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) started using the CPU for {cpu_runtime}ms burst [Q <empty>]")
        else:
            if time < 10000:
                print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) started using the CPU for {cpu_runtime}ms burst [Q{print_heapq_ready_queue(ready)}]")
        time += cpu_runtime

        #Update this process: Add back to all queue or finish
        if p.cpu_burst_times:

            #Add this process back to the all queue with updated arrival time

            #============== Added for SJF ================
            old_tau = math.ceil(p.estimatedNext) # (tau val)
            c_alpha = struct.unpack("f", struct.pack("f",float(alpha)))[0]
            p.estimatedNext = math.ceil(c_alpha * cpu_runtime + (1.0 - c_alpha) * old_tau)
            #=============================================

            p.arrival_time = time + p.io_burst_times.popleft()+tcs//2
            heapq.heappush(all, (p.arrival_time, p.name, p))


        while all:
            _, _, next_p = all[0]
    
            if next_p.arrival_time <= time:
                
                #ready.append(next_p)
                heapq.heappush(ready, (next_p.estimatedNext, next_p.name, next_p))
                heapq.heappop(all)

                if not next_p.hasRunIO:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) arrived; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
                    next_p.hasRunIO = True
                else:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) completed I/O; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
                    
            else:
                break

        if len(p.cpu_burst_times) == 0:
            if not ready:
                print(f"time {time}ms: Process {p.name} terminated [Q <empty>]")
            else:
                print(f"time {time}ms: Process {p.name} terminated [Q{print_heapq_ready_queue(ready)}]")

        elif not ready:
            if len(p.cpu_burst_times) > 1:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} (tau {old_tau}ms) completed a CPU burst; {len(p.cpu_burst_times)} bursts to go [Q <empty>]")
            else:
                if time < 10000: 
                    print(f"time {time}ms: Process {p.name} (tau {old_tau}ms) completed a CPU burst; {len(p.cpu_burst_times)} burst to go [Q <empty>]")

            if time < 10000:
                print(f"time {time}ms: Recalculating tau for process {p.name}: old tau {old_tau}ms ==> new tau {p.estimatedNext}ms [Q{print_heapq_ready_queue(ready)}]")
                print(f"time {time}ms: Process {p.name} switching out of CPU; blocking on I/O until time {p.arrival_time}ms [Q <empty>]")
        else:
            if len(p.cpu_burst_times) > 1:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} (tau {old_tau}ms) completed a CPU burst; {len(p.cpu_burst_times)} bursts to go [Q{print_heapq_ready_queue(ready)}]")
            else:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} (tau {old_tau}ms) completed a CPU burst; {len(p.cpu_burst_times)} burst to go [Q{print_heapq_ready_queue(ready)}]")

            if time < 10000:
                print(f"time {time}ms: Recalculating tau for process {p.name}: old tau {old_tau}ms ==> new tau {p.estimatedNext}ms [Q{print_heapq_ready_queue(ready)}]")
                print(f"time {time}ms: Process {p.name} switching out of CPU; blocking on I/O until time {p.arrival_time}ms [Q{print_heapq_ready_queue(ready)}]")
        time += tcs//2

    print(f"time {time}ms: Simulator ended for SJF [Q <empty>]")
    return stats


