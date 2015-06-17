import json

class Job(object):
    def __init__(self, kind, data):
        self.kind = kind
        self.data = data

    @classmethod
    def from_json(cls, json_blob):
        map_from = json.loads(json_blob)
        return Job(map_from['kind'], map_from['data'])

    def to_json(self):
        return json.dumps({ 'kind': self.kind, 'data': self.data })
