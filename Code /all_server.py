
import time

from pybus.codings.base_someipclasses import *
from pybus.dut_env_simulations.SRRLEnv_sim import SRRLEnvSimulation
from pybus.random_generator import RandomGenerator
import logging

LOG = logging.getLogger("example_srrl")

def main():
    env_sim = SRRLEnvSimulation()
    env_sim.initialize(offer_npdu_tunnel=False)

    field: SomeIpFieldProvider = env_sim.get_provided_service_by_name(
            "AmbientTemperature"
        ).get_field_by_name("ambientTemperatureData")

    sending_data = field.get_field_value

    ser = env_sim.get_required_service_by_name(
            "RadarFieldOfView")
    
    srpredetection: SomeIpEventConsumer = ser.get_event_by_name("radarFieldOfView")

    def func_(received_value):
            print(f"received notification ")
            print(f"Recieved Value: {received_value.radarFieldOfView.header.origin.x.value}")

    srpredetection.register_notification_handler(func_)

    def avail(value:bool):
         print("service is :",value)

    ser.register_service_availability_handler(avail)

    env_sim.start()

    time.sleep(2)
    for i in range(100):
        time.sleep(2)
        sending_data = RandomGenerator.get(type(sending_data))
        field.update_field_value(sending_data)
        print("Sent data :",sending_data.qualifier_Quality_FilteredAmbientTemperature)
        field.notify()

    #env_sim.stop()

    

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s:%(message)s', level=logging.INFO,datefmt='%m/%d/%Y %I:%M:%S %p')
    logger.info("Main starting")
    main()
