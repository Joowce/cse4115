from logging import StreamHandler


class MonitoringHandler(StreamHandler):
    def __init__(self, monitoring):
        StreamHandler.__init__(self)
        self.monitoring = monitoring

    def emit(self, record):
        msg = self.format(record)
        self.monitoring.add_queue_data(msg)