import time

from ahc.Ahc import ComponentModel
from ahc.Ahc import ComponentRegistry
from ahc.Ahc import EventTypes
from ahc.Ahc import Event
from ahc.Ahc import GenericMessage
from ahc.Ahc import GenericMessageHeader
from ahc.Routing.DSR.MonteCarloExperiment.DataCollector import DataCollector


class ApplicationComponent(ComponentModel):
    def __init__(self, component_name, component_id):
        super(ApplicationComponent, self).__init__(component_name, component_id)

    def send_data(self, dst):

        print("send_data...")

        src = self.componentinstancenumber

        data = "Data send by " + \
               self.componentname + \
               "-" +\
               str(self.componentinstancenumber)

        message_header = GenericMessageHeader("", self.componentname + "-" + str(src),
                                              self.componentname + "-" + str(dst))
        message_payload = data
        message = GenericMessage(message_header, message_payload)

        event = Event(self, EventTypes.MFRT, message)
        self.send_down(event)

    def process_message(self, data: str) -> None:
        print(f"I am {self.componentname}-{self.componentinstancenumber}, data received = {data}\n")

    def on_message_from_bottom(self, eventobj: Event):
        data = eventobj.eventcontent.payload
        self.process_message(data)

        # MonteCarloAddition
        DataCollector().end_sim()
