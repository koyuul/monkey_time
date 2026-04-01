"""
    Main entry for Monkey Hour.
"""
# from lib.lvgl_manager import init_lvgl, lvgl_task
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

    await asyncio.sleep_forever()

def main():
    """Main entry point: initialize hardware, graphics, and start the scheduler loop."""
    asyncio.run(_scheduler_loop())

main()