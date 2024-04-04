from utils import copy_process_list, print_ready_queue
import heapq
from collections import deque



def rr(original_processes, tcs, tslice):
    time = 0
    processes = copy_process_list(original_processes)

    all = []
    ready = deque([])

    for p in processes:
        heapq.heappush(all, (p.arrival_time, p.name, p))
        
    print("time 0ms: Simulator started for RR [Q <empty>]")


    while (all or ready):
        
        if (not ready):
            _, _, p = heapq.heappop(all)
            ready.append(p)
            time = p.arrival_time
            if not p.hasRunIO:
                print(f"time {time}ms: Process {p.name} arrived; added to ready queue [Q{print_ready_queue(ready)}]")
                p.hasRunIO = True
            else:
                print(f"time {time}ms: Process {p.name} completed I/O; added to ready queue [Q{print_ready_queue(ready)}]")

        time += tcs//2
        preemption_time = time + tslice
        p = ready.popleft()
        cpu_runtime = p.cpu_burst_times.popleft()
        if not ready:
            print(f"time {time}ms: Process {p.name} started using the CPU for {cpu_runtime}ms burst [Q <empty>]")
        else:
            print(f"time {time}ms: Process {p.name} started using the CPU for {cpu_runtime}ms burst [Q{print_ready_queue(ready)}]")
        
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
        else:
            while not ready and cpu_runtime > 0:
                burst_time = min(tslice, cpu_runtime)
                cpu_runtime -= burst_time
                time += burst_time

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
            if cpu_runtime > 0: 
                print(f"time {time}ms: Time slice expired; preempting process {p.name} with {cpu_runtime}ms remaining [Q{print_ready_queue(ready)}]")
                p.cpu_burst_times.appendleft(cpu_runtime)
                ready.append(p)
            elif cpu_runtime == 0 and p.cpu_burst_times:
                p.arrival_time = time + p.io_burst_times.popleft()+tcs//2
                heapq.heappush(all, (p.arrival_time, p.name, p))
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


