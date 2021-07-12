from queue import PriorityQueue
import numpy as np
from numpy import random
import math
import timeit
import matplotlib.pyplot as plt


def get_arrival():
    return round((-np.log(1 - np.random.uniform(low=0.0, high=1.0))) * landa, 3)


def get_service_time(miu):
    return math.floor((-np.log(1 - np.random.uniform(low=0.0, high=1.0))) * miu)


def get_next(number_in_system):
    if number_in_system == max_number:
        return (0, float('inf'), float('inf'))
    out = (4 - get_level(), math.floor(reception_current_time + get_arrival()), get_leave_time())
    return out


def get_part_number():
    num_list = []
    for i in range(0, n):
        num_list.append(i)
    return np.random.choice(num_list)  # assumes a uniform distribution


def get_leave_time():
    return round(random.exponential(scale=1 / alpha), 3)
    # return round((-np.log(1 - np.random.uniform(low=0.0, high=1.0)) / alpha), 3)


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


def add_to_parts(num, element, reception_service_time):
    # element: priority, arrival_time, leave_time
    pq_parts[num][element[0]].append((element[1], element[2], reception_service_time))

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


customer_arrivals_x = []
customer_arrivals_t = []

start = timeit.default_timer()
max_number = 100 + 1  ##10^7 + 1 bayad beshe fk knm
reception_current_time = 0
n, landa, reception_miu, alpha = map(float, input().split())
n = int(n)
pq_parts = []
parts_length_x = []
parts_length_t = []
for i in range(0, n):
    pq_parts.append([])
    for j in range(5):
        pq_parts[i].append([])
    parts_length_t.append([])
    parts_length_x.append([])
miu_staffs = []
for i in range(0, n):
    inputs = [*map(float, input().split())]
    miu_staffs.append(inputs)
customer_response_time = [0, 0, 0, 0, 0]  # reception_service_time + parts_service_time
all_response_times = [[], [], [], [], []]
all_waiting_times = [[], [], [], [], []]
customer_waiting_time_in_queue = [0, 0, 0, 0, 0]
customer_num_level = [0, 0, 0, 0, 0]
reception_state = False
all_arrival_times = []
reception_departure = float('inf')
next_reception_arrival = get_next(0)
all_arrival_times.append(next_reception_arrival[1])
reception_q = Queue([reception_miu], "poisson")
reception_q.number_in_system += 1
in_system = 0
customer_num_level[4 - next_reception_arrival[0]] += 1
while reception_q.number_in_system < max_number:
    #  reception_q.print_q()
    t = min(next_reception_arrival[1], reception_departure)
    reception_q.wait_time_in_queue += (reception_q.number_in_queue * (t - reception_current_time))
    reception_current_time = t
    if next_reception_arrival[1] < reception_departure:
        reception_q.arrivals += 1
        reception_q.number_in_system += 1
        in_system += 1
        if len(customer_arrivals_t) > 0 and customer_arrivals_t[len(customer_arrivals_t) - 1] == reception_current_time:
            customer_arrivals_x[len(customer_arrivals_x) - 1] = in_system
        else:
            customer_arrivals_x.append(in_system)
            customer_arrivals_t.append(reception_current_time)
        if reception_q.number_in_queue == 0 and not reception_state:  # reception is idle
            reception_service_time = get_service_time(reception_miu)
            if next_reception_arrival[2] + next_reception_arrival[1] >= reception_current_time + reception_service_time:
                reception_q.service_time += reception_service_time
                reception_departure = reception_current_time + reception_service_time
                customer_response_time[4 - next_reception_arrival[0]] += reception_service_time
                part_number = get_part_number()
                add_to_parts(part_number, next_reception_arrival,reception_service_time)
                reception_state = True
                next_reception_arrival = get_next(reception_q.number_in_system)
                all_arrival_times.append(next_reception_arrival[1])
                customer_num_level[4 - next_reception_arrival[0]] += 1
            else:
                in_system -= 1
                if len(customer_arrivals_t) > 0 and customer_arrivals_t[
                    len(customer_arrivals_t) - 1] == reception_current_time:
                    customer_arrivals_x[len(customer_arrivals_x) - 1] = in_system
                else:
                    customer_arrivals_x.append(in_system)
                    customer_arrivals_t.append(reception_current_time)
                reception_q.left_person += 1
                customer_waiting_time_in_queue[4 - next_reception_arrival[0]] += next_reception_arrival[2]
                all_waiting_times[4 - next_reception_arrival[0]].append(next_reception_arrival[2])
        else:  # reception is busy
            reception_q.add_queue(next_reception_arrival)
            reception_q.number_in_queue += 1
            reception_q.waited_number += 1
            next_reception_arrival = get_next(reception_q.number_in_system)
            all_arrival_times.append(next_reception_arrival[1])
            customer_num_level[4 - next_reception_arrival[0]] += 1
    else:
        reception_q.serviced_person_number += 1
        in_system -= 1
        if len(customer_arrivals_t) > 0 and customer_arrivals_t[len(customer_arrivals_t) - 1] == reception_current_time:
            customer_arrivals_x[len(customer_arrivals_x) - 1] = in_system
        else:
            customer_arrivals_x.append(in_system)
            customer_arrivals_t.append(reception_current_time)
        if reception_q.number_in_queue > 0:
            w = reception_q.get_queue()
            reception_service_time = get_service_time(reception_miu)
            if reception_current_time + reception_service_time <= w[2] + w[1]:
                part_number = get_part_number()
                add_to_parts(part_number, w,reception_service_time)
                reception_q.service_time += reception_service_time
                reception_departure = reception_current_time + reception_service_time
                customer_response_time[4 - w[0]] += reception_service_time
                reception_q.number_in_queue -= 1
            else:
                # in_system -= 1
                # customer_arrivals_x.append(in_system)
                # customer_arrivals_t.append(reception_current_time)
                reception_q.number_in_queue -= 1
                reception_q.left_person += 1
                customer_waiting_time_in_queue[4 - w[0]] += w[2]
                all_waiting_times[4 - w[0]].append(w[2])
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
parts_current_time = min(all_arrival_times)
parts_total_service_time = 0
parts_left_person = 0
for i in range(0, n):
    counter = 0
    for j in range(5):
        counter += len(pq_parts[i][j])
        pq_parts[i][j].sort(key=lambda a: a[0])
    num_parts.append(counter)
    total_num_in_parts += counter
    staff_state.append([])
    staff_departure.append([])
    for j in range(0, len(miu_staffs[i])):
        staff_state[i].append([])
        staff_departure[i].append([])
    for j in range(0, len(miu_staffs[i])):
        staff_state[i][j] = False
        staff_departure[i][j] = float('inf')

while True:
    """
    print("\n", parts_current_time)
    for i in range(0, n):
        print("---->", pq_parts[i])
    """
    for i in range(0, n):
        if num_parts[i] != 0:
            for j in range(0, len(miu_staffs[i])):  # update states
                if staff_departure[i][j] <= parts_current_time:
                    staff_state[i][j] = False
                # staff_departure[i][j] = float('inf')
            for j in range(0, len(miu_staffs[i])):
                for k in range(5):
                    if len(pq_parts[i][k]) > 0 and pq_parts[i][k][0][0] <= parts_current_time \
                            and not staff_state[i][j]:  # staff is idle
                        customer = pq_parts[i][k][0]
                        pq_parts[i][k].remove(customer)
                        num_parts[i] -= 1
                        total_num_in_parts -= 1
                        staff_service_time = get_service_time(miu_staffs[i][j])
                        if customer[1] >= parts_current_time + staff_service_time - customer[0]:
                            parts_total_service_time += staff_service_time
                            staff_state[i][j] = True
                            staff_departure[i][j] = parts_current_time + staff_service_time
                            # departure_times.append(customer[0])
                            departure_times.append(staff_departure[i][j])
                            customer_waiting_time_in_queue[4 - k] += parts_current_time - customer[0]
                            all_waiting_times[4 - k].append(parts_current_time - customer[0])
                            customer_response_time[4 - k] += staff_service_time
                            all_response_times[4 - k].append(customer[2] + staff_service_time)
                        else:
                            parts_left_person += 1
                            customer_waiting_time_in_queue[4 - k] += customer[1]
                            all_waiting_times[4 - k].append(customer[1])
        l_counter = 0
        for j in range(0, 5):
            for element in pq_parts[i][j]:
                if element[0] <= parts_current_time:
                    l_counter += 1
        parts_length_x[i].append(l_counter)
        parts_length_t[i].append(parts_current_time)
    if len(departure_times) != 0 or len(all_arrival_times) != 0:
        x = y = float('inf')
        if len(all_arrival_times) > 0:
            x = min(all_arrival_times)
        if len(departure_times) > 0:
            y = min(departure_times)
        parts_current_time = min(x, y)
        if parts_current_time in departure_times:
            departure_times.remove(parts_current_time)
        if parts_current_time in all_arrival_times:
            all_arrival_times.remove(parts_current_time)
    if total_num_in_parts == 0:
        break

print("length of reception queue: ", reception_q.waited_number)
print("average length of parts queue: [", end=' ')
lengths = parts_length_x.copy()
for i in range(0, n):
    print(sum(lengths[i]) / len(lengths[i]), end=' ')
print("]")
print("parts_left_person:", parts_left_person)
print("total left person: ", reception_q.left_person + parts_left_person)
if sum(customer_num_level) > 0:
    print("average time in system ",
          (sum(customer_waiting_time_in_queue) + sum(customer_response_time)) / sum(customer_num_level))
else:
    print("average time in system: 0 ")
average_time_in_sys = [0, 0, 0, 0, 0]
for i in range(0, 5):
    if customer_num_level[i] != 0:
        average_time_in_sys[i] = (customer_waiting_time_in_queue[i] + customer_response_time[i]) / customer_num_level[i]
print("average time in system in each level:", average_time_in_sys)
print("total_waiting_time_in_queues ", sum(customer_waiting_time_in_queue))
print("total_waiting_time_in_queues in each level: ", customer_waiting_time_in_queue)
print("average waiting time ", sum(customer_waiting_time_in_queue) / sum(customer_num_level))
average_waiting_time_in_queues = [0, 0, 0, 0, 0]
for i in range(0, 5):
    if customer_num_level[i] != 0:
        average_waiting_time_in_queues[i] = customer_waiting_time_in_queue[i] / customer_num_level[i]
print("average waiting time in queues in each level:", average_waiting_time_in_queues)
print("total response time ", sum(customer_response_time))
print("response time in each level:", customer_response_time)
stop = timeit.default_timer()
print('Execution Time: ', stop - start)

figure, axis = plt.subplots(1, 2)
axis[0].plot(customer_arrivals_t, customer_arrivals_x)
axis[0].set_title("Arrivals")

for i in range(0, n):
    axis[1].plot(parts_length_t[i], parts_length_x[i])
axis[1].set_title("Queue")

plt.show()
for i in range(5):
    plt.hist(all_response_times[i], bins=50)
    plt.gca().set(title=('Frequency Histogram For Response Time, Level:', i), ylabel='Frequency')
    plt.show()
for i in range(5):
    plt.hist(all_waiting_times[i], bins=50)
    plt.gca().set(title=('Frequency Histogram For Waiting Time, Level:', i), ylabel='Frequency')
    plt.show()
"""
2 100 15 0.05
1 2
3
3 1 3 1
3 2
3
4 1


2 10 5 0.05
10 11
10
"""