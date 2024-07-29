import vsomeip_bindings
import time
import threading

SAMPLE_SERVICE_ID = 0x1234
SAMPLE_INSTANCE_ID = 0x5678
SAMPLE_MAJOR = 2
SAMPLE_MINOR = 1
SAMPLE_EVENT_GRP_ID = 4
SAMPLE_EVENT_ID = 0x0001
myruntime = vsomeip_bindings.runtime.get()
myapp = myruntime.create_application("App_one")

def send_message():
    for i in range(100):
        payload = myruntime.create_payload()
        data = i
        data_bytes = bytes(data)
        payload.set_raw_data(data_bytes)
        myapp.notify(SAMPLE_SERVICE_ID,SAMPLE_INSTANCE_ID,SAMPLE_EVENT_ID,payload,False)
        print(f"Data {i} sent")
        time.sleep(1)

def main():
    myapp.init()
    myapp.offer_service(SAMPLE_SERVICE_ID,SAMPLE_INSTANCE_ID,SAMPLE_MAJOR,SAMPLE_MINOR)
    mygroup = set()
    mygroup.add(SAMPLE_EVENT_GRP_ID)
    myapp.offer_event(SAMPLE_SERVICE_ID,
                      SAMPLE_INSTANCE_ID,
                      SAMPLE_EVENT_ID,
                      mygroup,
                      vsomeip_bindings.event_type_e.ET_EVENT,
                      1000,
                      False,
                      False,
                      None,
                      vsomeip_bindings.reliability_type_e.RT_UNRELIABLE)
    thread1 = threading.Thread(target=send_message)
    thread1.start()
    myapp.start()
    time.sleep(1)


main()