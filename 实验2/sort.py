import numpy as np
import threading
import queue


data = np.random.randint(0, 1000000, size=1000000)
np.savetxt('random_numbers.txt', data, fmt='%d')

data = np.loadtxt('random_numbers.txt', dtype=int)


# 定义普通快速排序函数
def quicksort(data):
    if len(data) <= 1:
        return data
    else:
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return quicksort(left) + middle + quicksort(right)


# 定义归并两个已排序列表的函数
def merge_sorted_lists(list1, list2):
    merged_list = []
    i, j = 0, 0

    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1

    while i < len(list1):
        merged_list.append(list1[i])
        i += 1

    while j < len(list2):
        merged_list.append(list2[j])
        j += 1

    return merged_list


# 定义任务队列和结果列表
task_queue = queue.Queue()
sorted_parts = []
sorted_parts_lock = threading.Lock()
MAX_THREADS = 20


# 定义多线程快速排序函数
def parallel_quicksort(data, threshold=1000):
    if len(data) <= threshold:
        sorted_data = quicksort(data)
        with sorted_parts_lock:
            sorted_parts.append(sorted_data)
    else:
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]

        task_queue.put(left)
        task_queue.put(right)

        with sorted_parts_lock:
            sorted_parts.append(middle)


def worker():
    while not task_queue.empty():
        try:
            data_chunk = task_queue.get_nowait()
            parallel_quicksort(data_chunk)
        except queue.Empty:
            break


task_queue.put(data)

threads = []
for _ in range(MAX_THREADS):
    thread = threading.Thread(target=worker)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()


def merge_all_parts(parts):
    while len(parts) > 1:
        new_parts = []
        for i in range(0, len(parts), 2):
            if i + 1 < len(parts):
                merged = merge_sorted_lists(parts[i], parts[i + 1])
                new_parts.append(merged)
            else:
                new_parts.append(parts[i])
        parts = new_parts
    return parts[0] if parts else []


# 归并排序结果
sorted_data = merge_all_parts(sorted_parts)

# 将排序后的数据保存到文件中
np.savetxt('sorted_numbers.txt', sorted_data, fmt='%d')

print("完成排序，结果保存在'sorted_numbers.txt'")