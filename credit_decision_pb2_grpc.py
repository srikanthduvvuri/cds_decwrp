# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import credit_decision_pb2 as credit__decision__pb2


class CreditDecisionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.EvaluateApplication = channel.unary_unary(
                '/CreditDecisionService/EvaluateApplication',
                request_serializer=credit__decision__pb2.CreditDecisionRequest.SerializeToString,
                response_deserializer=credit__decision__pb2.CreditDecision.FromString,
                )


class CreditDecisionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def EvaluateApplication(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CreditDecisionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'EvaluateApplication': grpc.unary_unary_rpc_method_handler(
                    servicer.EvaluateApplication,
                    request_deserializer=credit__decision__pb2.CreditDecisionRequest.FromString,
                    response_serializer=credit__decision__pb2.CreditDecision.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'CreditDecisionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CreditDecisionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def EvaluateApplication(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CreditDecisionService/EvaluateApplication',
            credit__decision__pb2.CreditDecisionRequest.SerializeToString,
            credit__decision__pb2.CreditDecision.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
