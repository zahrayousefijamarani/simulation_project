import numpy as np
from queue import PriorityQueue


def get_arrival():
    return -np.log(1 - np.random.uniform(low=0.0, high=1.0)) / landa


def get_service_time():
    return -np.log(1 - np.random.uniform(low=0.0, high=1.0)) / m


def get_part():
    l = []
    for i in range(0, n): l.append(i)
    pa = np.random.choice(l)
    return pa


def get_leave_time():
    l = -np.log(1 - np.random.uniform(low=0.0, high=1.0)) / a
    return l


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


def do_part(part_number, waited_time):
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

    def add_queue(self, element):
        self.q.put((element[0], (element[1], element[2])))
        self.number_in_queue += 1
        self.waited_number += 1

    def get_queue(self):
        return self.q.get()

    def delete(self, a):
        self.q.get(a)  # todo


inputs = input().split(',')
n = int(inputs[0])
landa = float(inputs[1])
m = float(inputs[2])
a = float(inputs[3])
m_staffs = []
for i in range(0, n):
    inputs = inputs().split(',')
    number_of_staff = len(inputs)
    staffs = []
    for j in range(0, number_of_staff):
        staffs.append(float(inputs[j]))
    m_staffs.append(staffs)

reception_state = False
current_time = 0
reception_departure = float('inf')
next_reception_arrival = (get_level(), get_arrival(), get_leave_time())
reception_q = Queue([m], "poison")
parts = []
for i in range(0, n):
    parts.append(Queue(m_staffs[i], "poison"))

while True:
    t = min(next_reception_arrival[1], reception_departure)
    reception_q.wait_time_in_queue += (reception_q.number_in_queue * (t - current_time))
    current_time = t

    if next_reception_arrival[1] < reception_departure:
        reception_q.arrivals += 1
        reception_q.number_in_system += 1

        if reception_q.number_in_queue == 0 and reception_state == False:  # reception is idle
            reception_service_time = get_service_time()
            reception_q.service_time += reception_service_time
            reception_departure = current_time + reception_service_time
            reception_q.serviced_person_number += 1
            p = get_part()
            do_part(p, 0)
            reception_state = True
            next_reception_arrival = (get_level(), current_time + get_arrival(), get_leave_time())
        else:  # reception is busy
            if next_reception_arrival[2] + next_reception_arrival[1] <= current_time:
                reception_q.left_person += 1
                reception_q.delete(next_reception_arrival)
            else:
                reception_q.add_queue(next_reception_arrival)
                next_reception_arrival = (get_level(), current_time + get_arrival(), get_leave_time())
    else:
        if reception_q.number_in_queue > 0:
            w = reception_q.get_queue()
            if current_time < w[2] + w[1]:
                reception_service_time = get_service_time()
                reception_q.service_time += reception_service_time
                reception_departure = current_time + reception_service_time
                reception_q.number_in_queue -= 1
            else:
                reception_q.left_person += 1
        else:
            reception_departure = float('inf')
            reception_state = False
# what is the staff distribution
# how people choose parts
# termination condition
