from utils import copy_process_list, print_ready_queue, Stats, get_avg
import heapq
from collections import deque
import math

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
        stats.cpu_burst_time.append(math.ceil(sum(all_bursts)/len(all_bursts)*1000)/1000)
    except:
        stats.cpu_burst_time.append(0)

    try:
        stats.cpu_burst_time.append(math.ceil(sum(io_bursts)/len(io_bursts)*1000)/1000)
    except:
        stats.cpu_burst_time.append(0)

    try:
        stats.cpu_burst_time.append(math.ceil(sum(cpu_bursts)/len(cpu_bursts)*1000)/1000)
    except:
        stats.cpu_burst_time.append(0)


    all_wait_times = {}
    cpu_wait_times = {}
    io_wait_times = {}

    all_turnaround_times = {}
    cpu_turnaround_times = {}
    io_turnaround_times = {}

    for p in processes:
        if p.is_cpu_intensive:
            cpu_wait_times[p.name] = []
            cpu_turnaround_times[p.name] = []
        else:
            io_wait_times[p.name] = []
            io_turnaround_times[p.name] = []
        all_wait_times[p.name] = []
        all_turnaround_times[p.name] = []
        
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

                all_wait_times[p.name].append(time)
                #all_turnaround_times[p.name].append(time)
                if (p.is_cpu_intensive):
                    cpu_wait_times[p.name].append(time)
                    #cpu_turnaround_times[p.name].append(time)
                else:
                    io_wait_times[p.name].append(time)
                    #io_turnaround_times[p.name].append(time)

            else:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")

                all_wait_times[p.name].append(time)
                if (p.is_cpu_intensive):
                    cpu_wait_times[p.name].append(time)
                else:
                    io_wait_times[p.name].append(time)

            #time += p.cpu_burst_times[0]

        while all:
            _, _, next_p = all[0]
        
            if next_p.arrival_time <= time:
                
                ready.append(next_p)
                heapq.heappop(all)

                if not next_p.hasRunIO:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")


                    all_wait_times[next_p.name].append(next_p.arrival_time)
                    #all_turnaround_times[next_p.name].append(next_p.arrival_time)
                    if (next_p.is_cpu_intensive):
                        cpu_wait_times[next_p.name].append(next_p.arrival_time)
                        #cpu_turnaround_times[next_p.name].append(next_p.arrival_time)
                    else:
                        io_wait_times[next_p.name].append(next_p.arrival_time)
                        #io_turnaround_times[next_p.name].append(next_p.arrival_time)

                    next_p.hasRunIO = True
                    
                else:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")

                    all_wait_times[next_p.name].append(next_p.arrival_time)
                    #all_turnaround_times[next_p.name].append(next_p.arrival_time)
                    if (next_p.is_cpu_intensive):
                        cpu_wait_times[next_p.name].append(next_p.arrival_time)
                        #cpu_turnaround_times[next_p.name].append(next_p.arrival_time)
                    else:
                        io_wait_times[next_p.name].append(next_p.arrival_time)
                        #io_turnaround_times[next_p.name].append(next_p.arrival_time)
                    
            else:
                break            

        time += tcs//2
        
        p = ready.popleft()
        cpu_runtime = p.cpu_burst_times.popleft()

        if p.is_cpu_intensive:
            stats.num_context_switches[2] += 1
        else:
            stats.num_context_switches[1] += 1
        stats.num_context_switches[0] += 1

        while all:
            _, _, next_p = all[0]
        
            if next_p.arrival_time < time:
                
                ready.append(next_p)
                heapq.heappop(all)

                if not next_p.hasRunIO:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
                    next_p.hasRunIO = True

                    all_wait_times[next_p.name].append(next_p.arrival_time)
                    #all_turnaround_times[next_p.name].append(next_p.arrival_time)
                    if (next_p.is_cpu_intensive):
                        cpu_wait_times[next_p.name].append(next_p.arrival_time)
                        #cpu_turnaround_times[next_p.name].append(next_p.arrival_time)
                    else:
                        io_wait_times[next_p.name].append(next_p.arrival_time)
                        #io_turnaround_times[next_p.name].append(next_p.arrival_time)
                    

                else:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")

                    all_wait_times[next_p.name].append(next_p.arrival_time)
                    #all_turnaround_times[next_p.name].append(next_p.arrival_time)
                    if (next_p.is_cpu_intensive):
                        cpu_wait_times[next_p.name].append(next_p.arrival_time)
                        #cpu_turnaround_times[next_p.name].append(next_p.arrival_time)
                    else:
                        io_wait_times[next_p.name].append(next_p.arrival_time)
                        #io_turnaround_times[next_p.name].append(next_p.arrival_time)

                    
            else:
                break

        all_wait_times[p.name].append(time-tcs//2)
        all_turnaround_times[p.name].append(time-tcs//2)

        if (p.is_cpu_intensive):
            cpu_wait_times[p.name].append(time-tcs//2)
            cpu_turnaround_times[p.name].append(time-tcs//2)

        else:
            io_wait_times[p.name].append(time-tcs//2)
            io_turnaround_times[p.name].append(time-tcs//2)

        
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

                    all_wait_times[next_p.name].append(next_p.arrival_time)
                    #all_turnaround_times[next_p.name].append(next_p.arrival_time)
                    if (next_p.is_cpu_intensive):
                        cpu_wait_times[next_p.name].append(next_p.arrival_time)
                        #cpu_turnaround_times[next_p.name].append(next_p.arrival_time)
                    else:
                        io_wait_times[next_p.name].append(next_p.arrival_time)
                        #io_turnaround_times[next_p.name].append(next_p.arrival_time)

                else:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")

                    all_wait_times[next_p.name].append(next_p.arrival_time)
                    #all_turnaround_times[next_p.name].append(next_p.arrival_time)
                    if (next_p.is_cpu_intensive):
                        cpu_wait_times[next_p.name].append(next_p.arrival_time)
                        #cpu_turnaround_times[next_p.name].append(next_p.arrival_time)
                    else:
                        io_wait_times[next_p.name].append(next_p.arrival_time)
                        #io_turnaround_times[next_p.name].append(next_p.arrival_time)

                    
            else:
                break

        if len(p.cpu_burst_times) == 0:
            if not ready:
                print(f"time {time}ms: Process {p.name} terminated [Q <empty>]")
            else:
                print(f"time {time}ms: Process {p.name} terminated [Q{print_ready_queue(ready)}]")

            all_turnaround_times[p.name].append(time+tcs//2)
            if (p.is_cpu_intensive):
                cpu_turnaround_times[p.name].append(time+tcs//2)
            else:
                io_turnaround_times[p.name].append(time+tcs//2)

        elif not ready:
            if time < 10000:
                if len(p.cpu_burst_times) > 1:
                    print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} bursts to go [Q <empty>]")
                else: 
                    print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} burst to go [Q <empty>]")

                print(f"time {time}ms: Process {p.name} switching out of CPU; blocking on I/O until time {p.arrival_time}ms [Q <empty>]")

            all_turnaround_times[p.name].append(time+tcs//2)
            if (p.is_cpu_intensive):
                cpu_turnaround_times[p.name].append(time+tcs//2)
            else:
                io_turnaround_times[p.name].append(time+tcs//2)

        else:
            if time < 10000:
                if len(p.cpu_burst_times) > 1:
                    print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} bursts to go [Q{print_ready_queue(ready)}]")
                else:
                    print(f"time {time}ms: Process {p.name} completed a CPU burst; {len(p.cpu_burst_times)} burst to go [Q{print_ready_queue(ready)}]")

                print(f"time {time}ms: Process {p.name} switching out of CPU; blocking on I/O until time {p.arrival_time}ms [Q{print_ready_queue(ready)}]")

            all_turnaround_times[p.name].append(time+tcs//2)
            if (p.is_cpu_intensive):
                cpu_turnaround_times[p.name].append(time+tcs//2)
            else:
                io_turnaround_times[p.name].append(time+tcs//2)

        time += tcs//2

    print(f"time {time}ms: Simulator ended for FCFS [Q <empty>]")

    #stats.avg_wait_time[0] = (time - sum(all_bursts) - ((stats.num_context_switches[0]) * tcs))/len(all_bursts)

    try:
        stats.cpu_util = math.ceil((sum(all_bursts)/time)*100*1000)/1000
    except:
        stats.cpu_util = 0

    stats.avg_wait_time[0] = get_avg(all_wait_times, len(all_bursts))
    stats.avg_wait_time[1] = get_avg(io_wait_times, len(io_bursts))
    stats.avg_wait_time[2] = get_avg(cpu_wait_times, len(cpu_bursts))

    stats.avg_turn_time[0] = stats.avg_wait_time[0] + tcs + stats.cpu_burst_time[0]
    stats.avg_turn_time[1] = stats.avg_wait_time[1] + tcs + stats.cpu_burst_time[1]
    stats.avg_turn_time[2] = stats.avg_wait_time[2] + tcs + stats.cpu_burst_time[2]
    
        
    return stats


