from utils import copy_process_list, print_heapq_ready_queue
import heapq
from collections import deque
import math

import struct
import math


## converts a double precision python "float" into a single precision c "float" and back again
def c_float(x):
    return struct.unpack("f", struct.pack("f",float(x)))[0]

def srt(original_processes, tcs, alpha, lamda):
    time = 0
    #Copy the processes:
    processes = copy_process_list(original_processes)

    for proc in processes:
        proc.estimatedNext = math.ceil(c_float(1/lamda))

    all = []
    ready = []

    p = None

    for p in processes:
        heapq.heappush(all, (p.arrival_time, p.name, p))
        
    print("time 0ms: Simulator started for SRT [Q <empty>]")

    justPreempted = False
    lastP = None

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
                print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) arrived; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
                p.hasRunIO = True
            else:
                print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) completed I/O; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
            

        #p = ready.popleft()

        # if p is None:
        #      time += tcs//2
        #      _, _, p = heapq.heappop(ready)

        time += tcs//2
        start_time = time
        _, _, p = heapq.heappop(ready)
            
        cpu_runtime = p.cpu_burst_times.popleft()
        
        if p.time_elapsed == 0:
            if not ready:
                print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) started using the CPU for {cpu_runtime}ms burst [Q <empty>]")
            else:
                print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) started using the CPU for {cpu_runtime}ms burst [Q{print_heapq_ready_queue(ready)}]")
        else:
            print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) started using the CPU for remaining {cpu_runtime}ms of {cpu_runtime+p.time_elapsed}ms burst [Q{print_heapq_ready_queue(ready)}]")



        preemption = False
        p_remaining = cpu_runtime

        while not preemption and p_remaining != 0:

            time = start_time + cpu_runtime

            if all:
                time = min(start_time + cpu_runtime, all[0][2].arrival_time)
            

            time_elapsed = time - start_time
            p_remaining = cpu_runtime - time_elapsed

            while all:
                _, _, next_p = all[0]
            
                if next_p.arrival_time <= time:
                    
                    #ready.append(next_p)
                    heapq.heappush(ready, (next_p.estimatedNext, next_p.name, next_p))
                    heapq.heappop(all)

                    #if (time == 141494):
                        #print(p.name, cpu_runtime, time_elapsed, p.time_elapsed)


                    if (ready and p.estimatedNext - time_elapsed - p.time_elapsed > ready[0][2].estimatedNext-ready[0][2].time_elapsed):
                        if not p.hasRunIO:
                            print(f"time {time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) arrived; preempting {p.name} [Q{print_heapq_ready_queue(ready)}]")
                            p.hasRunIO = True
                        else:
                            print(f"time {time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) completed I/O; preempting {p.name} [Q{print_heapq_ready_queue(ready)}]")
                    else:
                        if not next_p.hasRunIO:
                            print(f"time {next_p.arrival_time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) arrived; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
                            next_p.hasRunIO = True
                        else:
                            print(f"time {next_p.arrival_time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) completed I/O; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
                        
                else:
                    break

            if (ready and p.estimatedNext - time_elapsed - p.time_elapsed > ready[0][2].estimatedNext-ready[0][2].time_elapsed):
                #Premmption code
                #print("PREEMPTION!!!")
                #print(p.estimatedNext, time_elapsed)
                #print(ready[0][2].estimatedNext, ready[0][2].time_elapsed)

                #Add p back into the ready queue
                p.cpu_burst_times.insert(0, p_remaining) #add p_remaining as most recent element
                p.time_elapsed += time_elapsed
                heapq.heappush(ready, (p.estimatedNext-p.time_elapsed, p.name, p))
                #justPreempted = True
                #lastP = p.name
                
                #_, _, p = heapq.heappop(ready)
                time += tcs//2
                break

            #Update this process: Add back to all queue or finish

            if p.cpu_burst_times and p_remaining == 0:

                #print("before setting time_elapsed to zero:", p.time_elapsed)
                #p.time_elapsed = 0

                #Add this process back to the all queue with updated arrival time

                #============== Added for SJF ================
                old_tau = p.estimatedNext # (tau val)
                c_alpha = struct.unpack("f", struct.pack("f",float(alpha)))[0]
                #print(cpu_runtime, p.time_elapsed)
                p.estimatedNext = (c_alpha * (cpu_runtime + p.time_elapsed) + (1 - c_alpha) * old_tau)
                #=============================================

                p.time_elapsed = 0

                p.arrival_time = time + p.io_burst_times.popleft()+tcs//2
                heapq.heappush(all, (p.arrival_time, p.name, p))



            #time += tcs//2
            
            if p_remaining == 0:

                if len(p.cpu_burst_times) == 0:
                    if not ready:
                        print(f"time {time}ms: Process {p.name} terminated [Q <empty>]")
                    else:
                        print(f"time {time}ms: Process {p.name} terminated [Q{print_heapq_ready_queue(ready)}]")

                elif not ready:
                    if len(p.cpu_burst_times) > 1:
                        print(f"time {time}ms: Process {p.name} (tau {old_tau}ms) completed a CPU burst; {len(p.cpu_burst_times)} bursts to go [Q <empty>]")
                    else: 
                        print(f"time {time}ms: Process {p.name} (tau {old_tau}ms) completed a CPU burst; {len(p.cpu_burst_times)} burst to go [Q <empty>]")

                    print(f"time {time}ms: Recalculating tau for process {p.name}: old tau {old_tau}ms ==> new tau {p.estimatedNext}ms [Q{print_heapq_ready_queue(ready)}]")
                    print(f"time {time}ms: Process {p.name} switching out of CPU; blocking on I/O until time {p.arrival_time}ms [Q <empty>]")
                else:
                    if len(p.cpu_burst_times) > 1:
                        print(f"time {time}ms: Process {p.name} (tau {old_tau}ms) completed a CPU burst; {len(p.cpu_burst_times)} bursts to go [Q{print_heapq_ready_queue(ready)}]")
                    else:
                        print(f"time {time}ms: Process {p.name} (tau {old_tau}ms) completed a CPU burst; {len(p.cpu_burst_times)} burst to go [Q{print_heapq_ready_queue(ready)}]")

                    print(f"time {time}ms: Recalculating tau for process {p.name}: old tau {old_tau}ms ==> new tau {p.estimatedNext}ms [Q{print_heapq_ready_queue(ready)}]")
                    print(f"time {time}ms: Process {p.name} switching out of CPU; blocking on I/O until time {p.arrival_time}ms [Q{print_heapq_ready_queue(ready)}]")
            time += tcs//2
        

    print(f"time {time}ms: Simulator ended for SRT [Q <empty>]")

    return time


