class BankersAlgorithm:
    def __init__(self, available, max_demand, allocation):
        self.available = available
        self.max_demand = max_demand
        self.allocation = allocation
        self.num_processes = len(max_demand)
        self.num_resources = len(available)
        self.need = self.Need()

    def Need(self):
        need = []
        for i in range(self.num_processes):
            need.append([self.max_demand[i][j] - self.allocation[i][j] for j in range(self.num_resources)])
        return need

    def is_safe(self):
        work = self.available[:]
        finish = [False] * self.num_processes
        safe_sequence = []

        while len(safe_sequence) < self.num_processes:
            allocated = False
            for i in range(self.num_processes):
                if not finish[i]:
                    if all(self.need[i][j] <= work[j] for j in range(self.num_resources)):
                        for k in range(self.num_resources):
                            work[k] += self.allocation[i][k]
                        finish[i] = True
                        safe_sequence.append(i)
                        allocated = True
            if not allocated:
                return False, []
        return True, safe_sequence

    def request_resources(self, process_id, request):
        # 检查请求是否满足需求和可用资源
        if all(request[i] <= self.need[process_id][i] for i in range(self.num_resources)) and \
                all(request[i] <= self.available[i] for i in range(self.num_resources)):
            # 假设分配资源
            for i in range(self.num_resources):
                self.available[i] -= request[i]
                self.allocation[process_id][i] += request[i]
                self.need[process_id][i] -= request[i]

            safe, _ = self.is_safe()
            if not safe:
                for i in range(self.num_resources):
                    self.available[i] += request[i]
                    self.allocation[process_id][i] -= request[i]
                    self.need[process_id][i] += request[i]
                return False
            return True
        else:
            return False


available = [3, 3, 2]
max_demand = [
    [7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]
]
allocation = [
    [0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]
]
ba = BankersAlgorithm(available, max_demand, allocation)

# 测试样例
#成功请求样例
result = ba.request_resources(1, [1, 0, 2])
print("Request result:", result)
print("Available:", ba.available)
print("Allocation:", ba.allocation)
print("Need:", ba.need)

#请求资源失败（资源不足）
result = ba.request_resources(4, [3, 3, 0])
print("Request result:", result)
print("Available:", ba.available)
print("Allocation:", ba.allocation)
print("Need:", ba.need)

# 请求资源失败（不安全状态）
result = ba.request_resources(0, [0, 2, 0])
print("Request result:", result)
print("Available:", ba.available)
print("Allocation:", ba.allocation)
print("Need:", ba.need)


