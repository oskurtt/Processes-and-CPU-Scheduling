from utils import copy_process_list, print_heapq_ready_queue, Stats, get_avg
import heapq
from collections import deque
import math

import struct
import math


## converts a double precision python "float" into a single precision c "float" and back again
def c_float(x):
    return struct.unpack("f", struct.pack("f",float(x)))[0]

def srt(original_processes, tcs, alpha, lamda):

    stats = Stats()
    stats.algorithm = "SRT"
    

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
        #print("NEW ITERATION!!", time)
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
            
            all_wait_times[p.name].append(time)
            if (p.is_cpu_intensive):
                cpu_wait_times[p.name].append(time)
            else:
                io_wait_times[p.name].append(time)


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
                    
                all_wait_times[next_p.name].append(next_p.arrival_time)
                if (next_p.is_cpu_intensive):
                    cpu_wait_times[next_p.name].append(next_p.arrival_time)
                else:
                    io_wait_times[next_p.name].append(next_p.arrival_time)

            else:
                break

        #p = ready.popleft()

        # if p is None:
        #      time += tcs//2
        #      _, _, p = heapq.heappop(ready)

        time += tcs//2
        start_time = time
        #print("JUST TIME!!", time)
        _, _, p = heapq.heappop(ready)

        if p.is_cpu_intensive:
            stats.num_context_switches[2] += 1
        else:
            stats.num_context_switches[1] += 1
        stats.num_context_switches[0] += 1

        while all:
            _, _, next_p = all[0]
        
            if next_p.arrival_time < time:
                
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
                 

                all_wait_times[next_p.name].append(next_p.arrival_time)
                if (next_p.is_cpu_intensive):
                    cpu_wait_times[next_p.name].append(next_p.arrival_time)
                else:
                    io_wait_times[next_p.name].append(next_p.arrival_time)

            else:
                break
            
        cpu_runtime = p.cpu_burst_times.popleft()

        all_wait_times[p.name].append(time-tcs//2)
        if (p.is_cpu_intensive):
            cpu_wait_times[p.name].append(time-tcs//2)
        else:
            io_wait_times[p.name].append(time-tcs//2)
        
        if p.time_elapsed == 0:
            if not ready:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) started using the CPU for {cpu_runtime}ms burst [Q <empty>]")
            else:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) started using the CPU for {cpu_runtime}ms burst [Q{print_heapq_ready_queue(ready)}]")
        else:
            if time < 10000:
                print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) started using the CPU for remaining {cpu_runtime}ms of {cpu_runtime+p.time_elapsed}ms burst [Q{print_heapq_ready_queue(ready)}]")



        preemption = False
        p_remaining = cpu_runtime

        #print("TIME DOWN HERE", time)

        #Handle preemption DURING context switch: "will preempt"

        if (ready and ready[0][2].estimatedNext-ready[0][2].time_elapsed < p.estimatedNext-p.time_elapsed):
            #print("PREEMPTION DURING CONTEXT SWITCH!!!")
            if time < 10000:
                print(f"time {time}ms: Process {ready[0][2].name} (tau {ready[0][2].estimatedNext}ms) will preempt {p.name} [Q{print_heapq_ready_queue(ready)}]")

            if p.is_cpu_intensive:
                stats.num_prem[2]+=1
            else:
                stats.num_prem[1]+=1
            stats.num_prem[0]+=1

            if p.is_cpu_intensive:
                stats.num_context_switches[2] += 1
            else:
                stats.num_context_switches[1] += 1
            stats.num_context_switches[0] += 1

            _, _, p_new = heapq.heappop(ready)
            time += tcs
            start_time = time
            cpu_runtime = p_new.cpu_burst_times.popleft()
            #print("JUST TIME!!", time)


            ''' =============================== UNUSURE ABOUT THIS UPDATE CODE ======================='''
            p.cpu_burst_times.insert(0, p_remaining) #add p_remaining as most recent element
            #p.time_elapsed += time_elapsed
            #print("TIME ELAPSED!",time_elapsed)
            heapq.heappush(ready, (p.estimatedNext-p.time_elapsed, p.name, p))

            all_wait_times[p.name].append(time-tcs//2)
            if (p.is_cpu_intensive):
                cpu_wait_times[p.name].append(time-tcs//2)
            else:
                io_wait_times[p.name].append(time-tcs//2)


            p = p_new


            if p.time_elapsed == 0:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) started using the CPU for {cpu_runtime}ms burst [Q{print_heapq_ready_queue(ready)}]")
            else:
                if time < 10000:
                    print(f"time {time}ms: Process {p.name} (tau {p.estimatedNext}ms) started using the CPU for remaining {cpu_runtime}ms of {cpu_runtime+p.time_elapsed}ms burst [Q{print_heapq_ready_queue(ready)}]")


            all_wait_times[p.name].append(time-tcs//2)
            if (p.is_cpu_intensive):
                cpu_wait_times[p.name].append(time-tcs//2)
            else:
                io_wait_times[p.name].append(time-tcs//2)


        while not preemption and p_remaining != 0:

            time = start_time + cpu_runtime

            if all:
                time = min(start_time + cpu_runtime, all[0][2].arrival_time)
            
            #print("Times ",time, start_time)
            time_elapsed = time - start_time
            #print("After Time elapsed!!",time_elapsed)
            p_remaining = cpu_runtime - time_elapsed

            preemption_happened = False

            while all:
                _, _, next_p = all[0]
                if next_p.arrival_time <= time and p_remaining > 0:                    
                    #ready.append(next_p)
                    heapq.heappush(ready, (next_p.estimatedNext, next_p.name, next_p))
                    heapq.heappop(all)

                    #if (time == 141494):
                        #print(p.name, cpu_runtime, time_elapsed, p.time_elapsed)

                    if (ready and p.estimatedNext - time_elapsed - p.time_elapsed > ready[0][2].estimatedNext-ready[0][2].time_elapsed and not preemption_happened):
                        preemption_happened = True
                        if not p.hasRunIO:
                            if time < 10000:
                                print(f"time {time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) arrived; preempting {p.name} [Q{print_heapq_ready_queue(ready)}]")
                            p.hasRunIO = True
                        else:
                            if time < 10000:
                                print(f"time {time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) completed I/O; preempting {p.name} [Q{print_heapq_ready_queue(ready)}]")
                    else:
                        if not next_p.hasRunIO:
                            if next_p.arrival_time < 10000:
                                print(f"time {next_p.arrival_time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) arrived; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
                            next_p.hasRunIO = True
                        else:
                            if next_p.arrival_time < 10000:
                                print(f"time {next_p.arrival_time}ms: Process {next_p.name} (tau {next_p.estimatedNext}ms) completed I/O; added to ready queue [Q{print_heapq_ready_queue(ready)}]")
                     
                    all_wait_times[next_p.name].append(next_p.arrival_time)
                    if (next_p.is_cpu_intensive):
                        cpu_wait_times[next_p.name].append(next_p.arrival_time)
                    else:
                        io_wait_times[next_p.name].append(next_p.arrival_time)


                else:
                    break

            #print("CHECK FOR PREEMPTION!!!")

            #if ready:
                #print(p.estimatedNext, time_elapsed ,p.time_elapsed)
                #print(ready[0][2].estimatedNext,ready[0][2].time_elapsed)
            #else:
                #print("Nothing to compare!!")

            if (p_remaining > 0 and ready and p.estimatedNext - time_elapsed - p.time_elapsed > ready[0][2].estimatedNext-ready[0][2].time_elapsed):
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

                if p.is_cpu_intensive:
                    stats.num_prem[2]+=1
                else:
                    stats.num_prem[1]+=1
                stats.num_prem[0]+=1
                
                #_, _, p = heapq.heappop(ready)
                time += tcs//2

                all_wait_times[p.name].append(time)
                if (p.is_cpu_intensive):
                    cpu_wait_times[p.name].append(time)
                else:
                    io_wait_times[p.name].append(time)

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
                p.estimatedNext = math.ceil(c_alpha * (cpu_runtime + p.time_elapsed) + (1 - c_alpha) * old_tau)
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


        

    print(f"time {time}ms: Simulator ended for SRT [Q <empty>]")

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


