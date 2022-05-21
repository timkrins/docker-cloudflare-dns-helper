import docker

class DockerApi:
    def __init__(self):
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.last_check = None

    def check_events(self):
        self.client.events(since=self.last_check, filters={'status': u'start'}, decode=True)

    def containers(self):
        return self.client.containers.list()

    def containers_labels(self):
        result = dict()
        for container in self.containers():
            result[container.name] = list(container.labels.items())
        return result

