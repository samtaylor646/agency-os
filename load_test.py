import asyncio
import httpx
import time
import statistics

URL = "http://localhost:8000/"

async def fetch(client, url):
    start_time = time.time()
    try:
        response = await client.get(url)
        elapsed = time.time() - start_time
        return response.status_code, elapsed
    except Exception as e:
        return 500, time.time() - start_time

async def load_test(num_requests, concurrency):
    print(f"Starting load test: {num_requests} requests, concurrency {concurrency}")
    
    async with httpx.AsyncClient(limits=httpx.Limits(max_connections=concurrency, max_keepalive_connections=concurrency)) as client:
        start_time = time.time()
        
        tasks = []
        for _ in range(num_requests):
            tasks.append(fetch(client, URL))
            
        results = await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
        
        status_codes = [r[0] for r in results]
        times = [r[1] for r in results]
        
        successes = status_codes.count(200)
        failures = len(results) - successes
        
        throughput = num_requests / total_time
        avg_time = statistics.mean(times) * 1000
        p95_time = statistics.quantiles(times, n=20)[18] * 1000 if len(times) > 1 else avg_time
        max_time = max(times) * 1000
        min_time = min(times) * 1000
        
        print("\n--- Load Test Results ---")
        print(f"Total Requests: {num_requests}")
        print(f"Concurrency Level: {concurrency}")
        print(f"Time taken: {total_time:.2f} seconds")
        print(f"Successes: {successes}")
        print(f"Failures: {failures}")
        print(f"Throughput: {throughput:.2f} req/s")
        print(f"Min Response Time: {min_time:.2f} ms")
        print(f"Max Response Time: {max_time:.2f} ms")
        print(f"Average Response Time: {avg_time:.2f} ms")
        print(f"95th Percentile Time: {p95_time:.2f} ms")

if __name__ == "__main__":
    # Test 1: Normal load
    asyncio.run(load_test(100, 10))
    # Test 2: 10x Load
    asyncio.run(load_test(1000, 100))
    # Test 3: Stress Test (Breaking point)
    asyncio.run(load_test(5000, 500))
