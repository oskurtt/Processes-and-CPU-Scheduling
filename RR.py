from utils import copy_process_list, print_ready_queue, Stats, get_avg
import heapq
from collections import deque
import math

def rr(original_processes, tcs, tslice):
    
    stats = Stats()
    stats.algorithm = "RR"
    

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

    for p in processes:
        if p.is_cpu_intensive:
            cpu_wait_times[p.name] = []
        else:
            io_wait_times[p.name] = []
        all_wait_times[p.name] = []



    time = 0
    processes = copy_process_list(original_processes)

    all = []
    ready = deque([])

    for p in processes:
        heapq.heappush(all, (p.arrival_time, p.name, p))
        
    print("time 0ms: Simulator started for RR [Q <empty>]")


    while (all or ready):

        #print(time)
        
        if (not ready):
            _, _, p = heapq.heappop(all)
            ready.append(p)
            time = p.arrival_time
            if not p.hasRunIO:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
                p.hasRunIO = True
            else:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")

            all_wait_times[p.name].append(time)
            if (p.is_cpu_intensive):
                cpu_wait_times[p.name].append(time)
            else:
                io_wait_times[p.name].append(time)


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

                all_wait_times[next_p.name].append(next_p.arrival_time)
                if (next_p.is_cpu_intensive):
                    cpu_wait_times[next_p.name].append(next_p.arrival_time)
                else:
                    io_wait_times[next_p.name].append(next_p.arrival_time)
                    
            else:
                break

        p = ready.popleft()
        time += tcs//2
        preemption_time = time + tslice
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
                else:
                    if next_p.arrival_time < 10000:
                        print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")

                all_wait_times[next_p.name].append(next_p.arrival_time)
                if (next_p.is_cpu_intensive):
                    cpu_wait_times[next_p.name].append(next_p.arrival_time)
                else:
                    io_wait_times[next_p.name].append(next_p.arrival_time)
                    
            else:
                break

        all_wait_times[p.name].append(time-tcs//2)
        if (p.is_cpu_intensive):
            cpu_wait_times[p.name].append(time-tcs//2)
        else:
            io_wait_times[p.name].append(time-tcs//2)

        if time < 10000:
            if p.time_elapsed == 0:
                if not ready:
                    print(f"time {time}ms: Process {p.name} started using the CPU for {cpu_runtime}ms burst [Q <empty>]")
                else:
                    print(f"time {time}ms: Process {p.name} started using the CPU for {cpu_runtime}ms burst [Q{print_ready_queue(ready)}]")
            else:
                if ready:
                    print(f"time {time}ms: Process {p.name} started using the CPU for remaining {cpu_runtime}ms of {cpu_runtime+p.time_elapsed}ms burst [Q{print_ready_queue(ready)}]")
                else:
                    print(f"time {time}ms: Process {p.name} started using the CPU for remaining {cpu_runtime}ms of {cpu_runtime+p.time_elapsed}ms burst [Q <empty>]")

        
        #time += cpu_runtime

        # if p.cpu_burst_times:

        #     p.arrival_time = time + p.io_burst_times.popleft()+tcs//2
        #     heapq.heappush(all, (p.arrival_time, p.name, p))

        if time + cpu_runtime <= preemption_time:
            time += cpu_runtime
            if p.cpu_burst_times:
                p.arrival_time = time + p.io_burst_times.popleft()+tcs//2
                heapq.heappush(all, (p.arrival_time, p.name, p))

            while all:
                _, _, next_p = all[0]
        
                if next_p.arrival_time < time:
                    
                    ready.append(next_p)
                    heapq.heappop(all)

                    if not next_p.hasRunIO:
                        if time < 10000:
                            print(f"time {next_p.arrival_time}ms: Process {next_p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
                        next_p.hasRunIO = True
                    else:
                        if time < 10000:
                            print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")

                    all_wait_times[next_p.name].append(next_p.arrival_time)
                    if (next_p.is_cpu_intensive):
                        cpu_wait_times[next_p.name].append(next_p.arrival_time)
                    else:
                        io_wait_times[next_p.name].append(next_p.arrival_time)
                        
                else:
                    break
                    
            p.time_elapsed = 0
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
        else:




            #while not ready and cpu_runtime > 0:
            while True:
                burst_time = min(tslice, cpu_runtime)
                cpu_runtime -= burst_time
                time += burst_time

                p.time_elapsed += burst_time

                while all:
                    _, _, next_p = all[0]
            
                    if next_p.arrival_time < time:
                        
                        ready.append(next_p)
                        heapq.heappop(all)

                        if not next_p.hasRunIO:
                            if time < 10000:
                                print(f"time {next_p.arrival_time}ms: Process {next_p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
                            next_p.hasRunIO = True
                        else:
                            if time < 10000:
                                print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")

                        all_wait_times[next_p.name].append(next_p.arrival_time)
                        if (next_p.is_cpu_intensive):
                            cpu_wait_times[next_p.name].append(next_p.arrival_time)
                        else:
                            io_wait_times[next_p.name].append(next_p.arrival_time)
                            
                    else:
                        break

                if (ready or cpu_runtime == 0):
                    break
                if time < 10000:
                    print(f"time {time}ms: Time slice expired; no preemption because ready queue is empty [Q <empty>]")


            if cpu_runtime > 0: 
                if time < 10000:
                    print(f"time {time}ms: Time slice expired; preempting process {p.name} with {cpu_runtime}ms remaining [Q{print_ready_queue(ready)}]")

                if p.is_cpu_intensive:
                    stats.num_prem[2]+=1
                else:
                    stats.num_prem[1]+=1
                stats.num_prem[0]+=1

                #This proc will be added to the the ready queue tcs//2 after preemption. Check special case where something arrives before then

                while all:
                    _, _, next_p = all[0]

                    #print(time)
                    #print(all[0])
                    #print(next_p.arrival_time)
                    #print(next_p.arrival_time < time + tcs//2)
                    #print(next_p.arrival_time, time)
                
                    if next_p.arrival_time < time + tcs//2:

                        #print("SPECIAL CASE HERE!!")
                        
                        ready.append(next_p)
                        heapq.heappop(all)

                        if not next_p.hasRunIO:
                            if time < 10000:
                                print(f"time {next_p.arrival_time}ms: Process {next_p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
                            next_p.hasRunIO = True
                        else:
                            if time < 10000:
                                print(f"time {next_p.arrival_time}ms: Process {next_p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")

                        all_wait_times[next_p.name].append(next_p.arrival_time)
                        if (next_p.is_cpu_intensive):
                            cpu_wait_times[next_p.name].append(next_p.arrival_time)
                        else:
                            io_wait_times[next_p.name].append(next_p.arrival_time)
                            
                    else:
                        break

                p.cpu_burst_times.appendleft(cpu_runtime)
                ready.append(p)

                all_wait_times[p.name].append(time+tcs//2)
                if (p.is_cpu_intensive):
                    cpu_wait_times[p.name].append(time+tcs//2)
                else:
                    io_wait_times[p.name].append(time+tcs//2)

            elif cpu_runtime == 0 and p.cpu_burst_times:
                p.time_elapsed = 0
                p.arrival_time = time + p.io_burst_times.popleft()+tcs//2
                heapq.heappush(all, (p.arrival_time, p.name, p))
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

            elif cpu_runtime == 0 and not p.cpu_burst_times:
                if len(p.cpu_burst_times) == 0:
                    if not ready:
                        print(f"time {time}ms: Process {p.name} terminated [Q <empty>]")
                    else:
                        print(f"time {time}ms: Process {p.name} terminated [Q{print_ready_queue(ready)}]")

            time += tcs//2


    print(f"time {time}ms: Simulator ended for RR [Q <empty>]", end='')

    try:
        stats.cpu_util = math.ceil((sum(all_bursts)/time)*100*1000)/1000
    except:
        stats.cpu_util = 0

    stats.avg_wait_time[0] = get_avg(all_wait_times, len(all_bursts))
    stats.avg_wait_time[1] = get_avg(io_wait_times, len(io_bursts))
    stats.avg_wait_time[2] = get_avg(cpu_wait_times, len(cpu_bursts))

    stats.avg_turn_time[0] = stats.avg_wait_time[0] + tcs*(stats.num_context_switches[0]/len(all_bursts)) + stats.cpu_burst_time[0]
    stats.avg_turn_time[1] = stats.avg_wait_time[1] + tcs*(stats.num_context_switches[1]/len(io_bursts)) + stats.cpu_burst_time[1]
    stats.avg_turn_time[2] = stats.avg_wait_time[2] + tcs*(stats.num_context_switches[2]/len(cpu_bursts)) + stats.cpu_burst_time[2]


    return stats


