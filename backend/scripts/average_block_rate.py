import time

from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS

blockcahin = Blockchain()

times = []

for i in range(1000):
    start_time = time.time_ns()
    blockcahin.add_block(i)
    end_time = time.time_ns()

    time_to_mine = (end_time - start_time) / SECONDS
    times.append(time_to_mine)

    average_time = sum(times) / len(times)

    print(f'New block difficulty: {blockcahin.chain[-1].difficulty}')
    print(f'Time to mine new block: {time_to_mine}s')
    print(f'Average time to add block: {average_time}s\n')