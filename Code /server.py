
import time

from pybus.codings.base_someipclasses import *
from pybus.dut_env_simulations.MYSRRLEnv_sim import SRRLEnvSimulation
from pybus.random_generator import RandomGenerator

LOG = logging.getLogger("example_srrl")

def main():
    env_sim = SRRLEnvSimulation()
    env_sim.initialize(offer_npdu_tunnel=False)

    field: SomeIpFieldProvider = env_sim.get_provided_service_by_name(
            "ActivationWireExtDiag"
        ).get_field_by_name("informationExtDiag")

    value = field.get_field_value
    value.statusConnectionEthOBD = 1
    value.statusActivationWireOBD = 1
    value.groupID[0] = 0
    value.groupID[1] = 1
    value.groupID[5] = 5

    env_sim.start()

    time.sleep(2)
    for i in range(100):
        time.sleep(2)
        value = RandomGenerator.get(type(value))
        field.update_field_value(value)
        print("Value :",value.groupID[2])
        field.notify()

    #env_sim.stop()

    

if __name__ == "__main__":
    main()
