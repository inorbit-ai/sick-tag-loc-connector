from sick_tag_loc_connector.src.connector import SickTagConnector


class SickTagLocMasterController:
    def __init__(self):
        self.connectors = []

    def create_connector(self, connector_config):
        connector = SickTagConnector(connector_config)
        self.connectors.append(connector)
        return connector

    def start_all(self):
        for connector in self.connectors:
            connector.start()

    def stop_all(self):
        for connector in self.connectors:
            connector.stop()
