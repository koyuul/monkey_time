"""
    Main entry for Monkey Hour.
"""
# from lib.analog_input_manager import AnalogInputManager
from lib.lvgl_manager import init_lvgl, lvgl_task
import uasyncio as asyncio

async def _scheduler_loop():
    """Scheduler loop: register async tasks from lib/ here."""

    # Handle LVGL display
    asyncio.create_task(lvgl_task())

    # Handle analog input
    # analog_input_manager = AnalogInputManager()
    # asyncio.create_task(analog_input_manager.poll_inputs())

    # keep the scheduler coroutine alive so created tasks keep running
    while True:
        await asyncio.sleep(1)

def start_scheduler():
    """Start the asyncio/uasyncio event loop and run the scheduler loop."""
    asyncio.run(_scheduler_loop())

def main():
    """Main entry point: initialize hardware, graphics, and start the scheduler loop."""
    init_lvgl()
    start_scheduler()

main()