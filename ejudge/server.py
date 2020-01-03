from django.conf import settings
from api import api_pb2 as pb
from django.utils import timezone
from google.protobuf import json_format

from handlers import GetSubmission, PostResults

import SimpleXMLRPCServer

class ServerMethods(object):
    def FromJson(self, message_class, json):
        message = message_class()
        json_format.Parse(json, message)
        return message

    def ToJson(self, message):
        return json_format.MessageToJson(message)

    def GetSubmission(self, request_json):
        request = self.FromJson(pb.GetSubmissionRequest,
                request_json)

        response = GetSubmission(request)

        return self.ToJson(response)

    def PostResults(self, request_json):
        request = self.FromJson(pb.PostResultsRequest,
                request_json)

        response = PostResults(request)

        return self.ToJson(response)

class Handler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    def log_message(self, fmt, *args):
        pass

def serve():
    server = SimpleXMLRPCServer.SimpleXMLRPCServer(('0.0.0.0', settings.EJUDGE_SERVER_PORT), requestHandler=Handler, allow_none=True)
    server.register_instance(ServerMethods())
    server.serve_forever()

if __name__ == '__main__':
    serve()
