from utils import copy_process_list, print_ready_queue
import heapq
from collections import deque



def fcfs(original_processes, tcs):
    time = 0
    #Copy the processes:
    processes = copy_process_list(original_processes)

    #statistics:

    # average CPU burst times for both CPU and IO processes
    average_burst_time = 0
    average_io_burst_time = 0
    average_cpu_burst_time = 0

    average_wait_time = 0
    average_io_wait_time = 0
    average_cpu_wait_time = 0

    average_turnaround_time = 0
    average_io_turnaround_time = 0
    average_cpu_turnaround_time = 0
    turnaround_dict = {}

    cpu_context_switches = 0
    io_context_switches = 0

    io_preemptions = 0
    cpu_preemptions = 0


    all = []
    ready = deque([])

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
        average_wait_time = sum(all_bursts)/len(all_bursts)
    except:
        average_wait_time = 0

    try:
        average_io_wait_time = sum(io_bursts)/len(io_bursts)
    except:
        average_wait_time = 0

    try:
        average_cpu_wait_time = sum(cpu_bursts)/len(cpu_bursts)
    except:
        averate_wait_time = 0
        
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
                # if not p.name in turnaround_dict:
                #     turnaround_dict[p.name] = dict()
                #     turnaround_dict[p.name]['cpu'] = -time
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
                    # if not p.name in turnaround_dict:
                    #     turnaround_dict[p.name] = dict()
                    #     turnaround_dict[p.name]['cpu'] = -time
                else:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")
                    
            else:
                break            

        time += tcs//2
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
                    # if not p.name in turnaround_dict:
                    #     turnaround_dict[p.name] = dict()
                    #     turnaround_dict[p.name]['cpu'] = -time

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
                    # if not p.name in turnaround_dict:
                    #     turnaround_dict[p.name] = dict()
                    #     turnaround_dict[p.name]['cpu'] = -time

                elif next_p.arrival_time < 10000:
                    print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")
                    
            else:
                break

        if len(p.cpu_burst_times) == 0:
            if not ready:
                print(f"time {time}ms: Process {p.name} terminated [Q <empty>]")
            else:
                print(f"time {time}ms: Process {p.name} terminated [Q{print_ready_queue(ready)}]")
            #turnaround_dict[p.name]['cpu'] += time


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

    return time


