from utils import copy_process_list, print_ready_queue, Stats
import heapq
from collections import deque



def fcfs(original_processes, tcs):


    stats = Stats()
    stats.algorithm = "FCFS"
    

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
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
                p.hasRunIO = True
            else:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")
            #time += p.cpu_burst_times[0]

        while all:
            _, _, next_p = all[0]
        
            if next_p.arrival_time <= time:
                
                ready.append(next_p)
                heapq.heappop(all)

                if not next_p.hasRunIO:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
                    next_p.hasRunIO = True
                    
                else:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")
                    
            else:
                break            

        time += tcs//2
        if p.is_cpu_intensive:
            stats.num_context_switches[1] += 1
        else:
            stats.num_context_switches[2] += 1
        stats.num_context_switches[0] += 1
        
        p = ready.popleft()
        cpu_runtime = p.cpu_burst_times.popleft()

        while all:
            _, _, next_p = all[0]
        
            if next_p.arrival_time < time:
                
                ready.append(next_p)
                heapq.heappop(all)

                if not next_p.hasRunIO:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
                    next_p.hasRunIO = True
                    

                else:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")
                    
            else:
                break
        
        if time < 10000:
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
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
                    next_p.hasRunIO = True

                elif next_p.arrival_time < 10000:
                    print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")
                    
            else:
                break

        if len(p.cpu_burst_times) == 0:
            if not ready:
                print(f"time {time}ms: Process {p.name} terminated [Q <empty>]")
            else:
                print(f"time {time}ms: Process {p.name} terminated [Q{print_ready_queue(ready)}]")

        elif not ready:
            if time < 10000:
                if len(p.cpu_burst_times) > 1:
                    print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} bursts to go [Q <empty>]")
                else: 
                    print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} burst to go [Q <empty>]")

                print(f"time {time}ms: Process {p.name} switching out of CPU; blocking on I/O until time {p.arrival_time}ms [Q <empty>]")

        else:
            if time < 10000:
                if len(p.cpu_burst_times) > 1:
                    print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} bursts to go [Q{print_ready_queue(ready)}]")
                else:
                    print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} burst to go [Q{print_ready_queue(ready)}]")

                print(f"time {time}ms: Process {p.name} switching out of CPU; blocking on I/O until time {p.arrival_time}ms [Q{print_ready_queue(ready)}]")

        time += tcs//2

    print(f"time {time}ms: Simulator ended for FCFS [Q <empty>]")

    stats.avg_wait_time = (time - sum(all_bursts) - ((stats.num_context_switches[0]) * tcs))/time

    try:
        stats.cpu_util = sum(all_bursts)/time
    except:
        stats.cpu_util = 0


    
        
    return stats


