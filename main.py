"""
    Main entry for Monkey Hour.
"""
import uasyncio as asyncio
from lib.analog_input_manager import AnalogInputManager
from lib.component_manager import ComponentManager
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
    tasks.append(asyncio.create_task(analog_input_manager.run()))

    # Handle LVGL navigation via analog input
    component_manager = ComponentManager(analog_input_manager, lvgl_manager,)
    component_manager.build_ui()
    tasks.append(asyncio.create_task(component_manager.handle_input()))

    # Handle time management
    time_manager = TimeManager(analog_input_manager.get_i2c())
    print(time_manager.get_time())

    while True:
        await asyncio.sleep(1)

def main():
    """Main entry point: initialize hardware, graphics, and start the scheduler loop."""
    asyncio.run(_scheduler_loop())

main()