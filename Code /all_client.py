
import time

from pybus.codings.base_someipclasses import *
from pybus.ecu_simulations.SRRL_sim import SRRLSimulation
from pybus.random_generator import RandomGenerator
import logging

logger = logging.getLogger("__name__")

def main():
    ecu_sim = SRRLSimulation()
    ecu_sim.initialize(offer_npdu_tunnel=False)

    srprefiled: SomeIpEventProvider = ecu_sim.get_provided_service_by_name("RadarFieldOfView"
                                    ).get_event_by_name("radarFieldOfView")
    
    sending_data = srprefiled.get_event_value

    ser = ecu_sim.get_required_service_by_name(
            "AmbientTemperature")

    field: SomeIpFieldConsumer = ser.get_field_by_name("ambientTemperatureData")

    def func_(received_value):
            print(f"received notification ")
            print(f"Recieved Value: {received_value.qualifier_Quality_FilteredAmbientTemperature}")

    field.register_notification_handler(func_)

    def avail(value:bool):
         print("service is :",value)

    ser.register_service_availability_handler(avail)

    ecu_sim.start()

    generator = RandomGenerator()

    time.sleep(2)
    for i in range(100):
        time.sleep(2)
        sending_data = generator.get_random_value(type(sending_data))
        srprefiled.update_event_value(sending_data)
        print("Sent data :",sending_data.radarFieldOfView.header.origin.x.value)
        srprefiled.notify()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s:%(message)s', level=logging.INFO,datefmt='%m/%d/%Y %I:%M:%S %p')
    logger.info("Main starting")
    main()
