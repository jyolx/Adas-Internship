
import time

from pybus.codings.base_someipclasses import *
from pybus.ecu_simulations.MYSRRL_sim import SRRLSimulation

logger = logging.getLogger("__name__")

def main():
    ecu_sim = SRRLSimulation()

    ecu_sim.initialize(offer_npdu_tunnel=False)

    ser = ecu_sim.get_required_service_by_name(
            "ActivationWireExtDiag"
        )

    statusExtDiag_field: SomeIpFieldConsumer = ser.get_field_by_name("informationExtDiag")

    def func_(received_value):
            print(f"received notification ")
            print(f"Value: {received_value.groupID[2]}")

    statusExtDiag_field.register_notification_handler(func_)

    def avail(value:bool):
         print("service is :",value)

    ser.register_service_availability_handler(avail)

    ecu_sim.start()

    time.sleep(100)

if __name__ == "__main__":
    logger.setLevel('DEBUG')
    main()
