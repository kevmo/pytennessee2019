from datetime import datetime

import appdaemon.plugins.hass.hassapi as hass
from whispers.sinkhole import threesix as hole

# How many seconds between executions?
INTERVAL = 20

# How many times should the name be requested to no longer
# be considered a "whisper"
WHISPER_DEFINITION = 50


def get_hostnames(hole_list):
    value = [x[0] for x in hole_list if x[1] < WHISPER_DEFINITION]
    return value


def get_counts(hole_list):
    value = [x[1] for x in hole_list if x[1] < WHISPER_DEFINITION]
    return value


class PyTennessee(hass.Hass):
    def initialize(self):
        now = datetime.now()
        self.tls = self.args["tls"]
        self.verify_tls = self.args["verify_tls"]
        self.schema = self.args["schema"]
        self.auth = self.args["auth"]
        self.host = self.args["host"]

        self.log("Hello PyTennessee 2019!  Thank you for this opportunity!")
        self.log(f"Executing at {now}")
        self.run_every(self.fetch_whispers, now, INTERVAL)

    def fetch_whispers(self, kwargs=None):
        conn = hole.SinkholeQueryData(
            tls=self.tls,
            schema=self.schema,
            verify_tls=self.verify_tls,
            auth=self.auth,
            host=self.host,
        )
        records = conn.order_data()
        hostnames = get_hostnames(records)
        counts = get_counts(records)
        self.call_service(
            "variable/set_variable",
            variable="whispers",
            value="defined",
            attributes={"hostnames": hostnames, "counts": counts},
        )
        now = datetime.now()
        self.log(f"Finished execution at {now}")

