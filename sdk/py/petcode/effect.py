from enum import IntEnum
from typing import NamedTuple

from seerbp.petcode.v1.message_pb2 import PetInfo


class EffectType(IntEnum):
    NONE = 0
    GENERAL = 1
    ITEM = 2

    VARIATION = 4
    SOULMARK = 5
    TEAM_TECH = 7
    OTHER = 99


class EffectParam(NamedTuple):
    """特效的参数化表示，用于生成 SeerAPI 请求 URL

    将 PetInfo.Effect 对象转换为 URL 友好的格式，方便在 API 请求中传递特效信息。

    Attributes:
        type: 特效类型（GENERAL/VARIATION/SOULMARK 等）
        name: 特效的字符串表示，格式为 "id_arg1_arg2_..."
    """
    type: EffectType
    name: str


def effect_to_param(effect: PetInfo.Effect) -> EffectParam:
    """将 PetInfo.Effect 对象转换为 EffectParam

    用于将 Protobuf 的 Effect 对象转换为适合 URL 传递的参数格式。
    特效类型从 status 字段提取，id 和 args 拼接为字符串。

    Args:
        effect: PetInfo.Effect 对象

    Returns:
        EffectParam 对象，包含特效类型和字符串表示

    Example:
        >>> effect = PetInfo.Effect(id=67, status=1, args=[1, 5])
        >>> param = effect_to_param(effect)
        >>> param.type  # EffectType.GENERAL
        >>> param.name  # "67_1_5"
    """
    type_ = get_effect_type(effect.status)
    name = '_'.join([str(effect.id), *[str(arg) for arg in effect.args]])
    return EffectParam(type=type_, name=name)


def param_to_effect(param: EffectParam) -> PetInfo.Effect:
    """将 EffectParam 转换回 PetInfo.Effect 对象

    用于将 URL 传递的特效参数还原为 Protobuf 的 Effect 对象。
    从 name 字符串中解析出 id 和 args，从 type 中恢复 status。

    Args:
        param: EffectParam 对象

    Returns:
        PetInfo.Effect 对象

    Example:
        >>> param = EffectParam(type=EffectType.GENERAL, name="67_1_5")
        >>> effect = param_to_effect(param)
        >>> effect.id  # 67
        >>> effect.status  # 1
        >>> effect.args  # [1, 5]
    """
    return PetInfo.Effect(
        id=int(param.name.split('_')[0]),
        status=param.type.value,
        args=[int(arg) for arg in param.name.split('_')[1:]],
    )


def get_effect_type(status: int):
    try:
        return EffectType(status)
    except ValueError:
        return EffectType.OTHER
