"""Demonstration of concurrent independent async tasks and bounded concurrency."""
import asyncio
import time

async def simulated_tool(name: str, delay: float, semaphore: asyncio.Semaphore):
    async with semaphore:
        await asyncio.sleep(delay)
        return f"{name} completed in about {delay:.1f}s"

async def main():
    semaphore = asyncio.Semaphore(3)  # Bound concurrent work.
    started = time.perf_counter()
    results = await asyncio.gather(
        simulated_tool("search A", 1.0, semaphore),
        simulated_tool("search B", 1.4, semaphore),
        simulated_tool("API request", 0.8, semaphore),
    )
    for result in results:
        print(result)
    print(f"Total wall time: {time.perf_counter() - started:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
