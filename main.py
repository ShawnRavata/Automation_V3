import multiprocessing

from rx.scheduler import ThreadPoolScheduler
from rx.subject import Subject

from LoggerController import LoggerController
from Rize import RizeSimulation, Rize
from missions.MissionOne.Mission import Mission
from missions.MissionOne.PumpController import PumpController

optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

rize_subject = Subject()

logger_controller = LoggerController()
rize_subject.subscribe(logger_controller.consume)


def mission_one_end(baseline):
    print(baseline)
    rize_subject.on_completed()


mission_one = Mission(rize_subject, PumpController(), mission_one_end, pool_scheduler)

is_simulation = True
if is_simulation:
    rize = RizeSimulation()
else:
    rize = Rize()

while rize.is_on():
    try:
        rize_subject.on_next(rize.read_line())
    except:
        print("Bad stuff happening in Rize output")
        pass
