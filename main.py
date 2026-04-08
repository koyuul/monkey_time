"""
    Main entry for Monkey Hour.
"""
import uasyncio as asyncio
from lib.analog_input_manager import AnalogInputManager
from lib.lvgl_manager import LVGLManager
from lib.time_manager import TimeManager


async def _scheduler_loop():
    """Scheduler loop: register async tasks from lib/ here."""
    tasks = []
    
    # Handle LVGL display
    lvgl_manager = LVGLManager()
    tasks.append(asyncio.create_task(lvgl_manager.update_display()))

    # Handle analog input
    analog_input_manager = AnalogInputManager()
    tasks.append(asyncio.create_task(analog_input_manager.poll_inputs()))

    # Handle time management
    time_manager = TimeManager(analog_input_manager.get_i2c())
    analog_input_manager.register_callback(
        0,
        time_manager.set_time,
        (2024, 6, 1, 5, 12, 0, 0, 0))

    while True:
        print("Current time:", time_manager.get_time())
        await asyncio.sleep(1)

def main():
    """Main entry point: initialize hardware, graphics, and start the scheduler loop."""
    asyncio.run(_scheduler_loop())

main()