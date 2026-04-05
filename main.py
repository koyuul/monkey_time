"""
    Main entry for Monkey Hour.
"""
import uasyncio as asyncio
from lib.analog_input_manager import AnalogInputManager
from lib.lvgl_manager import LVGLManager


async def _scheduler_loop():
    """Scheduler loop: register async tasks from lib/ here."""
    tasks = []
    
    # Handle LVGL display
    lvgl_manager = LVGLManager()
    tasks.append(asyncio.create_task(lvgl_manager.update_display()))

    # Handle analog input
    analog_input_manager = AnalogInputManager()
    tasks.append(asyncio.create_task(analog_input_manager.poll_inputs()))

    while True:
        await asyncio.sleep(1)

def main():
    """Main entry point: initialize hardware, graphics, and start the scheduler loop."""
    asyncio.run(_scheduler_loop())

main()