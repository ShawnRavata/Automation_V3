from rx import operators as ops, combine_latest
from rx.subject import Subject

from missions.BaseMission import BaseMission


class Mission(BaseMission):
    def __init__(self, rize_obs, pump_controller, end_mission_callback, scheduler):
        self.end_mission_callback = end_mission_callback

        self.pump_controller = pump_controller
        self.pump_command = Subject()
        self.pump_command.pipe(
            ops.observe_on(scheduler),
            ops.subscribe_on(scheduler),
        ).subscribe(self.pump_controller.handle, scheduler)

        self.well_25 = rize_obs.pipe(
            ops.map(lambda rize_data: rize_data["IMPEDANCE 25"]),
            ops.map(Mission._get_impedance_state),
        )
        self.well_26 = rize_obs.pipe(
            ops.map(lambda rize_data: rize_data["IMPEDANCE 26"]),
            ops.map(Mission._get_impedance_state),
        )
        self.well_27 = rize_obs.pipe(
            ops.map(lambda rize_data: rize_data["IMPEDANCE 27"]),
            ops.map(Mission._get_impedance_state),
        )
        combine_latest(self.well_25, self.well_26, self.well_27, rize_obs).pipe(
            ops.distinct_until_changed(lambda x: x[0] + x[1] + x[2]),
        ).subscribe(self.handle)

    def handle(self, wells):
        well_25, well_26, well_27, baseline = wells
        print(well_25, well_26, well_27)
        if well_25 is "AIR":
            self.pump_command.on_next("WITHDRAW")
        if well_25 is "LIQUID" and well_27 is "AIR":
            self.pump_command.on_next("SLOW")
        if well_25 is "LIQUID" and well_27 is "LIQUID":
            self.pump_command.on_next("INFUSE")
        if well_25 is "LIQUID" and well_26 is "LIQUID" and well_27 is "AIR":
            self.end_mission_callback(baseline)

    @staticmethod
    def _get_impedance_state(impedance):
        if impedance > 100_000:
            return "AIR"
        elif impedance > 7_500:
            return "RESIDUE"
        elif impedance > 1_000:
            return "LIQUID"
        else:
            return "ERROR"
