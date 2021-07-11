from queue import PriorityQueue
import numpy as np
import math
import timeit


def get_arrival():
    return round((-np.log(1 - np.random.uniform(low=0.0, high=1.0))) * landa, 3)


def get_service_time(miu):
    return math.floor((-np.log(1 - np.random.uniform(low=0.0, high=1.0))) * miu)


def get_next(number_in_system):
    if number_in_system == max_number:
        return (0, float('inf'), float('inf'))
    return (4 - get_level(), math.floor(reception_current_time + get_arrival()), get_leave_time())


def get_part():
    num_list = []
    for i in range(0, n):
        num_list.append(i)
    return np.random.choice(num_list)  # assumes a uniform distribution


def get_leave_time():
    return round((-np.log(1 - np.random.uniform(low=0.0, high=1.0)) / alpha), 3)


def get_level():
    v = np.random.uniform(low=0.0, high=1.0)
    if v < 0.50:
        return 0
    if v < 0.70:
        return 1
    if v < 0.85:
        return 2
    if v < 0.95:
        return 3
    else:
        return 4


def add_to_parts(num, element):
    new_element = (element[0], (element[1], element[2]))  # priority, arrival_time, leave_time
    pq_parts[num].put(new_element)


class Queue:
    def __init__(self, means, distribution):
        self.distribution = distribution
        self.clerk_number = len(means)
        self.priority_queue = PriorityQueue()
        self.means = means
        self.number_in_queue = 0
        self.wait_time_in_queue = 0
        self.waited_number = 0
        self.service_time = 0
        self.serviced_person_number = 0
        self.left_person = 0
        self.arrivals = 0
        self.number_in_system = 0
        self.print_queue = []

    def add_queue(self, element):
        new_element = (element[0], (element[1], element[2]))
        self.priority_queue.put(new_element)
        self.print_queue.append(new_element)

    def get_queue(self):
        b = self.priority_queue.get()
        return (b[0], b[1][0], b[1][1])

    def delete(self, a):
        pass
        # self.q.get(a)  # todo

    def print_q(self):
        for i in self.print_queue:
            print(i)


start = timeit.default_timer()
max_number = 10 + 1  ##10^7 + 1 bayad beshe fk knm
reception_current_time = 0
n, landa, reception_miu, alpha = map(float, input().split())
n = int(n)
pq_parts = []
for i in range(0, n):
    pq_parts.append(PriorityQueue())
miu_staffs = []
for i in range(0, n):
    inputs = [*map(float, input().split())]
    miu_staffs.append(inputs)
customer_response_time = [0, 0, 0, 0, 0]  # reception_service_time + parts_sevice_time
customer_waiting_time_in_queue = [0, 0, 0, 0, 0]
customer_num_level = [0, 0, 0, 0, 0]
reception_state = False
reception_departure = float('inf')
next_reception_arrival = get_next(0)
reception_q = Queue([reception_miu], "poisson")
reception_q.number_in_system += 1
customer_num_level[4 - next_reception_arrival[0]] += 1
while reception_q.serviced_person_number < max_number:
    #  reception_q.print_q()
    t = min(next_reception_arrival[1], reception_departure)
    reception_q.wait_time_in_queue += (reception_q.number_in_queue * (t - reception_current_time))
    reception_current_time = t
    if next_reception_arrival[1] < reception_departure:
        reception_q.arrivals += 1
        reception_q.number_in_system += 1
        if reception_q.number_in_queue == 0 and not reception_state:  # reception is idle
            reception_service_time = get_service_time(reception_miu)
            if next_reception_arrival[2] + next_reception_arrival[1] >= reception_current_time + reception_service_time:
                reception_q.service_time += reception_service_time
                reception_departure = reception_current_time + reception_service_time
                customer_response_time[4 - next_reception_arrival[0]] += reception_service_time
                part_number = get_part()
                add_to_parts(part_number, next_reception_arrival)
                reception_state = True
                next_reception_arrival = get_next(reception_q.number_in_system)
                customer_num_level[4 - next_reception_arrival[0]] += 1
            else:
                reception_q.left_person += 1
                customer_waiting_time_in_queue[4 - next_reception_arrival[0]] += next_reception_arrival[2]
        else:  # reception is busy
            reception_q.add_queue(next_reception_arrival)
            reception_q.number_in_queue += 1
            reception_q.waited_number += 1
            next_reception_arrival = get_next(reception_q.number_in_system)
            customer_num_level[4 - next_reception_arrival[0]] += 1
    else:
        reception_q.serviced_person_number += 1
        if reception_q.number_in_queue > 0:
            w = reception_q.get_queue()
            reception_service_time = get_service_time(reception_miu)
            if reception_current_time + reception_service_time <= w[2] + w[1]:
                part_number = get_part()
                add_to_parts(part_number, w)
                reception_q.service_time += reception_service_time
                reception_departure = reception_current_time + reception_service_time
                customer_response_time[4 - w[0]] += reception_service_time
                reception_q.number_in_queue -= 1
            else:
                reception_q.number_in_queue -= 1
                reception_q.left_person += 1
                customer_waiting_time_in_queue[4 - w[0]] += w[2]
        else:
            reception_departure = float('inf')
            reception_state = False
print("\ntotal number in reception = ", max_number - 1)
customer_num_level[0] -= 1
print("Number in each level", customer_num_level)
print("reception_left_person: ", reception_q.left_person)
# print("~~start parts~~")
num_parts = []
staff_state = []
staff_departure = []
departure_times = []
total_num_in_parts = 0
parts_current_time = 0
parts_total_service_time = 0
parts_left_person = 0
for i in range(0, n):
    num_parts.append(pq_parts[i].qsize())
    total_num_in_parts += pq_parts[i].qsize()
    staff_state.append([])
    staff_departure.append([])
    for j in range(0, len(miu_staffs[i])):
        staff_state[i].append([])
        staff_departure[i].append([])
    for j in range(0, len(miu_staffs[i])):
        staff_state[i][j] = False
        staff_departure[i][j] = float('inf')
while True:
    # print("\n",parts_current_time)
    # for i in range(0, n):
    # print("---->", pq_parts[i].queue)
    for i in range(0, n):
        if num_parts[i] != 0:
            for j in range(0, len(miu_staffs[i])):  # update states
                if staff_departure[i][j] == parts_current_time:
                    staff_state[i][j] = False
                    staff_departure[i][j] = float('inf')
            for j in range(0, len(miu_staffs[i])):
                if num_parts[i] > 0 and pq_parts[i].queue[0][1][0] <= parts_current_time \
                        and not staff_state[i][j]:  # staff is idle
                    customer = pq_parts[i].get()
                    num_parts[i] -= 1
                    total_num_in_parts -= 1
                    staff_service_time = get_service_time(miu_staffs[i][j])
                    if customer[1][1] >= parts_current_time + staff_service_time - customer[1][0]:
                        parts_total_service_time += staff_service_time
                        staff_state[i][j] = True
                        staff_departure[i][j] = parts_current_time + staff_service_time
                        departure_times.append(customer[1][0])
                        departure_times.append(staff_departure[i][j])
                        customer_waiting_time_in_queue[4 - customer[0]] += parts_current_time - customer[1][0]
                        customer_response_time[4 - customer[0]] += staff_service_time
                        # print("line 199 - serviced in part ", i, "\t", customer)
                    else:
                        parts_left_person += 1
                        customer_waiting_time_in_queue[4 - customer[0]] += customer[1][1]
                        # print("line 204 - left3 in part", i, "\t", customer)
    if len(departure_times) != 0:
        parts_current_time = min(departure_times)
        departure_times.remove(parts_current_time)
    if total_num_in_parts == 0:
        break
print("parts_left_person:", parts_left_person)
print("total number of leavers:", parts_left_person + reception_q.left_person)
print("average time in system ",
      (sum(customer_waiting_time_in_queue) + sum(customer_response_time)) / sum(customer_num_level))
average_time_in_sys = [0, 0, 0, 0, 0]
for i in range(0, 5):
    if customer_num_level[i] != 0:
        average_time_in_sys[i] = (customer_waiting_time_in_queue[i] + customer_response_time[i]) / customer_num_level[i]
print("average time in system:", average_time_in_sys)
print("total_waiting_time_in_queues ", sum(customer_waiting_time_in_queue))
print("total_waiting_time_in_queues", customer_waiting_time_in_queue)
print("average waiting time ", sum(customer_waiting_time_in_queue) / sum(customer_num_level))
average_waiting_time_in_queues = [0, 0, 0, 0, 0]
for i in range(0, 5):
    if customer_num_level[i] != 0:
        average_waiting_time_in_queues[i] = customer_waiting_time_in_queue[i] / customer_num_level[i]
print("average waiting time in queues", average_waiting_time_in_queues)
print("total response time ", sum(customer_response_time))
print("response time", customer_response_time)
stop = timeit.default_timer()
print('Execution Time: ', stop - start)
"""
2 1000 20 21
1 2
3
"""
