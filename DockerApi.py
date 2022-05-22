import docker
from datetime import datetime

class DockerApi:
    def __init__(self):
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    def start_container_events(self):
        events = self.client.events(since=datetime.now(), filters={'status': u'start'}, decode=True)
        for event in events:
            try:
                if event['status'] == u'start':
                    yield event
            except KeyError:
                None
            except OSError:
                events.close()
            except StopIteration:
                events.close()

    def containers(self):
        return self.client.containers.list()

    def containers_labels(self):
        result = dict()
        for container in self.containers():
            result[container.name] = list(container.labels.items())
        return result
