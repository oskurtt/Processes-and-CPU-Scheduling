from utils import copy_process_list, print_ready_queue
import heapq
from collections import deque



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
            if not p.hasRunIO:
                print(f"time {time}ms: Process {p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
                p.hasRunIO = True
            else:
                print(f"time {time}ms: Process {p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")
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
            if len(p.cpu_burst_times) > 1:
                print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} bursts to go [Q <empty>]")
            else: 
                print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} burst to go [Q <empty>]")

            print(f"time {time}ms: Process {p.name} switching out of CPU; blocking on I/O until time {p.arrival_time}ms [Q <empty>]")
        else:
            if len(p.cpu_burst_times) > 1:
                print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} bursts to go [Q{print_ready_queue(ready)}]")
            else:
                print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} burst to go [Q{print_ready_queue(ready)}]")

            print(f"time {time}ms: Process {p.name} switching out of CPU; blocking on I/O until time {p.arrival_time}ms [Q{print_ready_queue(ready)}]")

        time += tcs//2

    print(f"time {time}ms: Simulator ended for FCFS [Q <empty>]")

    return time


