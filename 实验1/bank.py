import threading
from queue import Queue

class Customer:
    def __init__(self, customer_id, arrival_time, service_time):
        self.customer_id = customer_id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.begin_service_time = None
        self.end_service_time = None
        self.server_id = None
class Server:
    def __init__(self, server_id):
        self.server_id = server_id
        self.working = None

#信号量
customer_semaphore = threading.Semaphore(0)
server_semaphore = threading.Semaphore(0)
#锁
mutex = threading.Lock()
time_lock = threading.Lock()
#全局时间
global_time = 0
def server_work(server,customer_quene):
    global global_time
    while True:
        customer_semaphore.acquire()
        with mutex:
            if not customer_quene.empty():
                customer = customer_quene.get()
        server.working = True
        with time_lock:
            customer.begin_service_time = global_time
        customer.server_id = server.server_id
        service_end_time = global_time + customer.service_time

        while global_time < service_end_time:
            pass

        with time_lock:
            customer.end_service_time = global_time

        server.working = False
        print(f"顾客 {customer.customer_id} 到达时间： {customer.arrival_time}, "
              f"开始服务时间： {customer.begin_service_time}, 离开时间： {customer.end_service_time}, "
              f"服务人员编号： {server.server_id}")
        server_semaphore.release()

def customer_arrival(customer,customer_quene):
    global global_time
    while global_time < customer.arrival_time:
        pass
    with mutex:
        customer_quene.put(customer)
    customer_semaphore.release()
    server_semaphore.acquire()

def bank_work(servers,customers):
    customer_quene = Queue()

    server_threads = []
    customer_threads = []

    for server in servers:
        server_thread = threading.Thread(target=server_work, args=(server, customer_quene))
        server_thread.start()
        server_threads.append(server_thread)

    for customer in customers:
        customer_thread = threading.Thread(target=customer_arrival, args=(customer, customer_quene))
        customer_thread.start()
        customer_threads.append(customer_thread)

    global global_time

    total_time = max([customer.arrival_time + customer.service_time for customer in customers])

    for time in range(total_time+1):
        with time_lock:
            global_time = time
        threading.Event().wait(0.1)
        '''
            print('time:',time,'total_time:',global_time,time==total_time)
            if time == total_time:
                return 0
        '''

    for customer_thread in customer_threads:
        customer_thread.join()
    for server_thread in server_threads:
        server_thread.join()



def read_customers_from_file(filename):
    customers = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            customer_id = int(parts[0])
            arrival_time = int(parts[1])
            service_time = int(parts[2])
            customers.append(Customer(customer_id, arrival_time, service_time))
    return customers

customers = read_customers_from_file('test_data.txt')
servers = [Server(1), Server(2)]
bank_work(servers, customers)

