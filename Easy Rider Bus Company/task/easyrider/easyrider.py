import itertools
import json
import typing
from collections import defaultdict, Counter


class Stop:
    def __init__(self, kwargs):
        self.bus_id = kwargs.get("bus_id")
        self.stop_id = kwargs.get("stop_id")
        self.stop_name = kwargs.get("stop_name")
        self.next_stop = kwargs.get("next_stop")
        self.stop_type = kwargs.get("stop_type")
        self.a_time = kwargs.get("a_time")


def get_start_or_finish_stop_names(stops: typing.List[Stop], stop_type: str) -> typing.List[str]:
    stop_type_stops = set()
    for stop in stops:
        if stop.stop_type == stop_type:
            stop_type_stops.add(stop.stop_name)
    return sorted(list(stop_type_stops))


def get_transfer_stop_names(buses: typing.Dict[int, typing.List[Stop]]) -> typing.List[str]:
    stop_names = [[bus_stop.stop_name for bus_stop in bus_stops] for bus_stops in buses.values()]
    counter = Counter([name for stop in stop_names for name in stop])

    return sorted([k for k, v in counter.items() if v > 1])


def get_buses(stops: typing.List[Stop]) -> typing.Dict[int, typing.List[Stop]]:
    buses = defaultdict(list)
    for stop in stops:
        buses[stop.bus_id].append(stop)
    return buses


if __name__ == "__main__":
    stops = [Stop(s) for s in json.loads(input())]
    buses = get_buses(stops)
    stops_names_on_demand = {s.stop_name for s in stops if s.stop_type == "O"}
    stop_names_to_check = set()

    for stop_name in itertools.chain(
            get_start_or_finish_stop_names(stops, "S"),
            get_transfer_stop_names(buses),
            get_start_or_finish_stop_names(stops, "F")
    ):
        stop_names_to_check.add(stop_name)
    stop_names_wrong = sorted(stops_names_on_demand.intersection(stop_names_to_check))
    print("On demand stops test:")
    if stop_names_wrong:
        print(f"Wrong stop stype: {stop_names_wrong}")
    else:
        print("OK")
