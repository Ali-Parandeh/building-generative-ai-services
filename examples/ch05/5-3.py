import asyncio


async def main():
    print("Before sleeping")
    await asyncio.sleep(3)
    print("After sleeping for 3 seconds")


asyncio.run(main())

"""
Before sleeping
After sleeping for 3 seconds <3>
"""
