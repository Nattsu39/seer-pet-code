"""弃用数据转换

将 PetCodeMessage 中已经废弃的字段转换为当前推荐的数据表示，
以兼容仍在使用旧字段的第三方工具产出的数据。
"""

from seerbp.petcode.v1.message_pb2 import (
    PetAbilityBonus,
    PetCodeMessage,
    PetInfo,
)

# 用于承载 extra_hp 的 PetAbilityBonus 加成类型
_BASEVALUE_BONUS_TYPE = PetAbilityBonus.Type.TYPE_BASEVALUE


def _convert_extra_hp(pet: PetInfo) -> None:
    """将 pet.extra_hp 转换为一个全新的 TYPE_BASEVALUE 加成项"""
    if pet.extra_hp == 0:
        return

    bonus = pet.ability_bonus.add()
    bonus.type = _BASEVALUE_BONUS_TYPE
    bonus.value.hp.value = pet.extra_hp
    pet.extra_hp = 0


def convert_deprecated_data(message: PetCodeMessage) -> PetCodeMessage:
    """将消息中的弃用数据转换为新数据（原地修改并返回）

    目前会处理以下弃用字段：

    - ``PetInfo.extra_hp``：转换为 ``ability_bonus`` 中一个全新的
      ``TYPE_BASEVALUE`` 类型的 ``hp`` 固定加成项，不会与已有加成项合并。

    Args:
        message: 待转换的 PetCodeMessage 对象

    Returns:
        转换后的同一个 PetCodeMessage 对象（便于链式调用）

    Example:
        >>> message = from_base64(code)
        >>> convert_deprecated_data(message)
        >>> message.pets[0].extra_hp  # 0
    """
    for pet in message.pets:
        _convert_extra_hp(pet)
    return message
