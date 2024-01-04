import grpc
import eco_explore_api.grcp.protocols.comentarios_pb2 as comentarios_pb2
import eco_explore_api.grcp.protocols.comentarios_pb2_grpc as comentarios_pb2_grpc
from eco_explore_api.documentdb.schemas import Reseña
import eco_explore_api.constants.response_constants as rcodes
from eco_explore_api.config import GRPC_SERVER_URL


class GrpcServer:
    def __init__(self):
        self.server_address = GRPC_SERVER_URL
        self.channel = grpc.insecure_channel(self.server_address)
        self.client = comentarios_pb2_grpc.ComentariosServiceStub(self.channel)

    def get_comentary(self, id_comentay: str):
        try:
            consulta = comentarios_pb2.ConsultaComentario(id=id_comentay)
            obtener_comentario_respuesta = self.client.ObtenerComentario(consulta)

            if obtener_comentario_respuesta.comentario:
                comentario = obtener_comentario_respuesta.comentario[0]
                ans = Reseña(
                    Comentario=comentario.comentario,
                    Evaluacion=comentario.evaluacion,
                )
                return ans
            else:
                return None
        except Exception as e:
            raise ValueError("Al crear la consulta rpc " + str(e))
