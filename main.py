from copy import deepcopy

import numpy as np
from queue import PriorityQueue


def get_arrival():
    return round(-np.log(1 - np.random.uniform(low=0.0, high=1.0)) / landa, 3)


def get_service_time():
    k = round(-np.log(1 - np.random.uniform(low=0.0, high=1.0)) / m, 3)
    print("service time" + str(k))
    return k


def get_next():
    k = (get_level(), current_time + get_arrival(), get_leave_time())
    return k


def get_part():
    l = []
    for i in range(0, n): l.append(i)
    pa = np.random.choice(l)
    return pa


def get_leave_time():
    l = -np.log(1 - np.random.uniform(low=0.0, high=1.0)) / a
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
    pass


class Queue:
    def __init__(self, means, distribution):
        self.distribution = distribution
        self.clerk_number = len(means)
        self.q = PriorityQueue()
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
        l = (element[0], (element[1], element[2]))
        self.q.put(l)
        self.print_queue.append(l)

    def get_queue(self):
        b = self.q.get()
        return (b[0], b[1][0], b[1][1])

    def delete(self, a):
        pass
        # self.q.get(a)  # todo

    def print_q(self):
        for i in self.print_queue:
            print(i)


inputs = input().split(',')
n = int(inputs[0])
landa = float(inputs[1])
m = float(inputs[2])
a = float(inputs[3])
m_staffs = []
for i in range(0, n):
    inputs = input().split(',')
    number_of_staff = len(inputs)
    staffs = []
    for j in range(0, number_of_staff):
        staffs.append(float(inputs[j]))
    m_staffs.append(staffs)

reception_state = False
current_time = 0
reception_departure = float('inf')
next_reception_arrival = get_next()
reception_q = Queue([m], "poison")
parts = []
for i in range(0, n):
    parts.append(Queue(m_staffs[i], "poison"))

while True:
    reception_q.print_q()
    t = min(next_reception_arrival[1], reception_departure)
    reception_q.wait_time_in_queue += (reception_q.number_in_queue * (t - current_time))
    current_time = t

    if next_reception_arrival[1] < reception_departure:
        reception_q.arrivals += 1
        reception_q.number_in_system += 1

        if reception_q.number_in_queue == 0 and reception_state == False:  # reception is idle
            reception_service_time = get_service_time()
            if next_reception_arrival[2] + next_reception_arrival[1] > current_time + reception_service_time:
                reception_q.service_time += reception_service_time
                reception_departure = current_time + reception_service_time
                p = get_part()
                do_part(p, 0, next_reception_arrival)
                reception_state = True
                print("serviced")
                print(next_reception_arrival)
                next_reception_arrival = get_next()
            else:
                reception_q.left_person += 1

        else:  # reception is busy
            # if next_reception_arrival[2] + next_reception_arrival[1] <= current_time:
            #     reception_q.left_person += 1
            #     reception_q.delete(next_reception_arrival)
            #     print("left1")
            #     print(next_reception_arrival)
            # else:
            # print("queued")
            # print(next_reception_arrival)
            reception_q.add_queue(next_reception_arrival)
            reception_q.number_in_queue += 1
            reception_q.waited_number += 1
            next_reception_arrival = get_next()
    else:
        reception_q.serviced_person_number += 1
        if reception_q.number_in_queue > 0:
            w = reception_q.get_queue()
            reception_service_time = get_service_time()
            if current_time + reception_service_time < w[2] + w[1]:
                print("serviced")
                print(w)
                reception_q.service_time += reception_service_time
                reception_departure = current_time + reception_service_time
                reception_q.number_in_queue -= 1
            else:
                print("left2")
                print(w)
                reception_q.number_in_queue -= 1
                reception_q.left_person += 1
        else:
            reception_departure = float('inf')
            reception_state = False
# what is the staff distribution
# how people choose parts
# termination condition
