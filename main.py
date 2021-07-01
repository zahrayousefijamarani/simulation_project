class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def delete(self):
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i] > self.queue[max]:
                    max = i
            item = self.queue[max]
            del self.queue[max]
            return item
        except IndexError:
            print()
            exit()


class Queue:
    def __init__(self, mean, clerk_number):
        self.clerk_number = clerk_number
        self.q = PriorityQueue()
        self.mean = mean
        self.number_in_queue = 0
        self.wait_time_in_queue = 0
        self.service_time = 0
        self.serviced_person_number = 0
        self.left_person = 0

    def arrival(self):
        pass


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
    m_staffs.append((number_of_staff, staffs))

current_time = 0
