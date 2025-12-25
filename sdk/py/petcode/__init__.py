import base64
import gzip

from google.protobuf import json_format

from seerbp.petcode.v1.message_pb2 import PetCodeMessage

from .create_and_read import create_petcode_message


def _compress_with_gzip(binary: bytes, level: int = 1) -> bytes:
    """使用 gzip 压缩二进制数据"""
    return gzip.compress(binary, compresslevel=level)


def _decompress_with_gzip(compressed: bytes) -> bytes:
    """使用 gzip 解压缩二进制数据"""
    return gzip.decompress(compressed)


def to_binary(message: PetCodeMessage) -> bytes:
    """
    将消息序列化为二进制数据，并使用 gzip 压缩
    """
    return _compress_with_gzip(message.SerializeToString())


def from_binary(binary: bytes) -> PetCodeMessage:
    """
    将二进制数据解压缩，并反序列化为消息
    """
    return PetCodeMessage.FromString(_decompress_with_gzip(binary))


def to_base64(message: PetCodeMessage) -> str:
    """
    将消息序列化为二进制数据并压缩，返回数据的 base64
    """
    binary = _compress_with_gzip(message.SerializeToString())
    return base64.b64encode(binary).decode('utf-8')


def from_base64(base64_str: str) -> PetCodeMessage:
    """
    将 base64 数据解码，并反序列化为消息
    """
    binary = base64.b64decode(base64_str)
    return from_binary(binary)


def to_dict(message: PetCodeMessage) -> dict:
    """
    将消息序列化为字典
    """
    return json_format.MessageToDict(message)


def from_dict(data: dict) -> PetCodeMessage:
    """
    将字典反序列化为消息
    """
    return json_format.ParseDict(data, PetCodeMessage())


__all__ = [
    'create_petcode_message',
    'from_base64',
    'from_binary',
    'from_dict',
    'to_base64',
    'to_binary',
    'to_dict',
]
