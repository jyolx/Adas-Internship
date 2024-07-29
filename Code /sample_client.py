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
myapp = myruntime.create_application("App_two")
condition_var = threading.Condition()

def run():
    condition_var.acquire()
    condition_var.wait()
    print("Going")
    mygroup=set()
    mygroup.add(SAMPLE_EVENT_GRP_ID)
    myapp.request_event(SAMPLE_SERVICE_ID,
                        SAMPLE_INSTANCE_ID,
                        SAMPLE_EVENT_ID,
                        mygroup,
                        vsomeip_bindings.event_type_e.ET_EVENT,
                        vsomeip_bindings.reliability_type_e.RT_UNRELIABLE)
    myapp.subscribe(SAMPLE_SERVICE_ID,SAMPLE_INSTANCE_ID,SAMPLE_EVENT_GRP_ID,SAMPLE_MAJOR,SAMPLE_EVENT_ID)
    print("Subscribed")
    myapp.register_message_handler(SAMPLE_SERVICE_ID,SAMPLE_INSTANCE_ID,SAMPLE_EVENT_ID,on_message)
    print("After on message")
    condition_var.release()
    while(1):
     pass
    

def on_avail(ser,ins,avail):
    condition_var.acquire()
    print("Service",hex(ser),"Instance",hex(ins),"is",avail)
    if(avail):
        condition_var.notify()
    condition_var.release()

def on_message(message):
    print("Message received")
    payload_bytes = bytes(message.get_payload().get_data())
    print("Message :",len(payload_bytes))

def main():
    myapp.init()
    myapp.request_service(SAMPLE_SERVICE_ID,SAMPLE_INSTANCE_ID,SAMPLE_MAJOR,SAMPLE_MINOR)
    myapp.register_availability_handler(SAMPLE_SERVICE_ID,SAMPLE_INSTANCE_ID,on_avail,SAMPLE_MAJOR,SAMPLE_MINOR)
    
    thread1=threading.Thread(target = run)
    thread1.start()
    myapp.start()
    #time.sleep(1)


main()