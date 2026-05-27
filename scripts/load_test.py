#!/usr/bin/env python3

import asyncio
import aiohttp
import time
import argparse

async def simulate_pod(session, url, pod_id):
    start = time.time()
    payload = {
        "task": f"Load test task {pod_id}",
        "domain": "engineering"
    }
    try:
        async with session.post(f"{url}/execute", json=payload) as response:
            await response.json()
            return time.time() - start
    except Exception as e:
        print(f"Pod {pod_id} failed: {e}")
        return -1

async def run_load_test(url, num_pods):
    print(f"Starting load test with {num_pods} concurrent pods against {url}...")
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [simulate_pod(session, url, i) for i in range(num_pods)]
        results = await asyncio.gather(*tasks)
    
    total_time = time.time() - start_time
    successful = [r for r in results if r > 0]
    
    print("\n--- Load Test Results ---")
    print(f"Total time: {total_time:.2f}s")
    print(f"Successful Pods: {len(successful)}/{num_pods}")
    if successful:
        print(f"Avg Response Time: {sum(successful)/len(successful):.2f}s")
        print(f"Max Response Time: {max(successful):.2f}s")
        print(f"Min Response Time: {min(successful):.2f}s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:5000", help="API URL")
    parser.add_argument("--pods", type=int, default=50, help="Number of concurrent pods")
    args = parser.parse_args()
    
    asyncio.run(run_load_test(args.url, args.pods))
