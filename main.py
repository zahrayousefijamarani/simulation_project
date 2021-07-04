import numpy as np
from queue import PriorityQueue
import math


def get_arrival():
    return round(-np.log(1 - np.random.uniform(low=0.0, high=1.0)) / landa, 3)


def get_service_time(miu):
    k = round(-np.log(1 - np.random.uniform(low=0.0, high=1.0)) / miu, 3)
    #  print("line12-service time" + str(k))
    return k


def get_next():
    if total_number == max_number:
        return (0, float('inf'), float('inf'))
    n = (get_level(), current_time + get_arrival(), get_leave_time())
    print("line17-get next func= ", n)
    return n


def get_part():
    l = []
    for i in range(0, n): l.append(i)
    pa = np.random.choice(l)
    return pa


def get_leave_time():
    l = -np.log(1 - np.random.uniform(low=0.0, high=1.0)) / alpha
    return round(l, 3)


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


def do_part(part_number, waited_time, element):
    print("line48 part = ", part_number)
    new_element = (element[0], (element[1], element[2], waited_time))  # priority, arrival_time, lave_time, waited_time
    pq_parts[part_number].put(new_element)


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


total_number = 0
max_number = 20  ##10^7 bayad beshe
current_time = 0
inputs = input().split(',')
n = int(inputs[0])
landa = float(inputs[1])
miu = float(inputs[2])
alpha = float(inputs[3])

pq_parts = []

for i in range(0, n):
    pq_parts.append(PriorityQueue())

miu_staffs = []
for i in range(0, n):
    inputs = [*map(float, input().split())]
    miu_staffs.append(inputs)
print(miu_staffs)

reception_state = False
reception_departure = float('inf')
next_reception_arrival = get_next()
total_number += 1
reception_q = Queue([miu], "poisson")
reception_q.number_in_system += 1

while reception_q.serviced_person_number < max_number:
    reception_q.print_q()
    t = min(next_reception_arrival[1], reception_departure)
    print("line116\nline118 t = ", t)
    reception_q.wait_time_in_queue += (reception_q.number_in_queue * (t - current_time))
    current_time = t

    if next_reception_arrival[1] < reception_departure:
        reception_q.arrivals += 1
        reception_q.number_in_system += 1
        total_number += 1

        if reception_q.number_in_queue == 0 and not reception_state:  # reception is idle
            reception_service_time = get_service_time(miu)
            if next_reception_arrival[2] + next_reception_arrival[1] > current_time + reception_service_time:
                reception_q.service_time += reception_service_time
                reception_departure = current_time + reception_service_time
                part_number = get_part()
                do_part(part_number, 0, next_reception_arrival)
                reception_state = True
                print("line 134 service time - serviced", reception_service_time, next_reception_arrival)
                next_reception_arrival = get_next()

            else:
                reception_q.left_person += 1

        else:  # reception is busy
            reception_q.add_queue(next_reception_arrival)
            reception_q.number_in_queue += 1
            reception_q.waited_number += 1
            next_reception_arrival = get_next()
    else:
        reception_q.serviced_person_number += 1
        if reception_q.number_in_queue > 0:
            w = reception_q.get_queue()
            reception_service_time = get_service_time(miu)
            if current_time + reception_service_time < w[2] + w[1]:
                print("line 160 - serviced ", w)
                part_number = get_part()
                do_part(part_number, current_time + reception_service_time - w[1], w)  # check she parameter2sh
                reception_q.service_time += reception_service_time
                reception_departure = current_time + reception_service_time
                reception_q.number_in_queue -= 1
            else:
                print("line167- left2\t", w)
                reception_q.number_in_queue -= 1
                reception_q.left_person += 1
        else:
            reception_departure = float('inf')
            reception_state = False

# what is the staff distribution
# how people choose parts
# termination condition
print("total number = ", max_number)
print("Number of leavers = ", reception_q.left_person)
print("\n\n~~start parts~~")
num_parts = []
staff_state = []
staff_departure = []
departure_times = []
i_list = []
j_list = []
count = 0
parts_current_time = 0
parts_total_service_time = 0
parts_left_person = 0
for i in range(0, n):
    num_parts.append(pq_parts[i].qsize())
    count += pq_parts[i].qsize()
    staff_state.append([])
    staff_departure.append([])
    for j in range(0, len(miu_staffs[i])):
        staff_state[i].append([])
        staff_departure[i].append([])
    for j in range(0, len(miu_staffs[i])):
        staff_state[i][j] = False
        staff_departure[i][j] = float('inf')

while True:
    for i in range(0, n):
        if num_parts[i] != 0:
            for j in range(0, len(miu_staffs[i])):  # update states
                if abs(staff_departure[i][j] - parts_current_time) < 0.00000000001:
                    staff_state[i][j] = False

            for j in range(0, len(miu_staffs[i])):
                if num_parts[i] > 0 and not staff_state[i][j]:  # staff is idle
                    customer = pq_parts[i].get()
                    num_parts[i] -= 1
                    count -= 1
                    staff_service_time = get_service_time(miu_staffs[i][j])
                    if customer[1][1] > customer[1][2] + parts_current_time + staff_service_time:
                        parts_total_service_time += staff_service_time
                        staff_state[i][j] = True
                        staff_departure[i][j] = parts_current_time + staff_service_time
                        i_list.append(str(i))
                        j_list.append(str(j))
                        departure_times.append(staff_departure[i][j])
                    #    print("line 220 - serviced in part ", i)
                    #    print("linr221- ", customer)
                    else:
                        parts_left_person += 1
                    #  print("line 224 - left3 in part", i)
                #     print("line225- ", customer)

    if len(departure_times) != 0:
        parts_current_time = min(departure_times)
        departure_times.remove(parts_current_time)
    if count == 0:
        break

print("end parts")
