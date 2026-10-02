"""测试弃用数据转换函数"""

from petcode.deprecated import convert_deprecated_data
from seerbp.petcode.v1.message_pb2 import (
    PetAbilityBonus,
    PetCodeMessage,
    PetInfo,
)


def _create_message(*pets: PetInfo) -> PetCodeMessage:
    return PetCodeMessage(
        server=PetCodeMessage.Server.SERVER_OFFICIAL,
        display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
        pets=list(pets),
    )


def _find_basevalue_bonus(pet: PetInfo) -> PetAbilityBonus:
    for bonus in pet.ability_bonus:
        if bonus.type == PetAbilityBonus.Type.TYPE_BASEVALUE:
            return bonus
    raise AssertionError('未找到 TYPE_BASEVALUE 加成项')


class TestConvertDeprecatedData:
    """测试弃用数据转换"""

    def test_extra_hp_creates_basevalue_bonus(self):
        """extra_hp 应被转换为新的 TYPE_BASEVALUE 加成"""
        message = _create_message(PetInfo(id=1, extra_hp=20))

        convert_deprecated_data(message)

        pet = message.pets[0]
        assert pet.extra_hp == 0
        assert len(pet.ability_bonus) == 1
        bonus = pet.ability_bonus[0]
        assert bonus.type == PetAbilityBonus.Type.TYPE_BASEVALUE
        assert bonus.value.hp.value == 20
        assert not bonus.value.hp.HasField('percent')

    def test_extra_hp_creates_new_bonus_without_merging(self):
        """即使已存在 TYPE_BASEVALUE 加成，也应新增一个全新加成项"""
        message = _create_message(
            PetInfo(
                id=1,
                extra_hp=20,
                ability_bonus=[
                    PetAbilityBonus(
                        type=PetAbilityBonus.Type.TYPE_BASEVALUE,
                        value=PetAbilityBonus.Value(
                            hp=PetAbilityBonus.ExtraValue(value=5, percent=10)
                        ),
                    )
                ],
            )
        )

        convert_deprecated_data(message)

        pet = message.pets[0]
        assert pet.extra_hp == 0
        assert len(pet.ability_bonus) == 2
        existing = pet.ability_bonus[0]
        assert existing.value.hp.value == 5
        assert existing.value.hp.percent == 10
        created = pet.ability_bonus[1]
        assert created.type == PetAbilityBonus.Type.TYPE_BASEVALUE
        assert created.value.hp.value == 20
        assert not created.value.hp.HasField('percent')

    def test_extra_hp_zero_does_nothing(self):
        """extra_hp 为 0 时不应产生任何改动"""
        message = _create_message(PetInfo(id=1))

        convert_deprecated_data(message)

        pet = message.pets[0]
        assert pet.extra_hp == 0
        assert len(pet.ability_bonus) == 0

    def test_preserves_other_bonus_types(self):
        """转换不应影响其他类型的加成项"""
        message = _create_message(
            PetInfo(
                id=1,
                extra_hp=20,
                ability_bonus=[
                    PetAbilityBonus(type=PetAbilityBonus.Type.TYPE_TEAM_TECH),
                ],
            )
        )

        convert_deprecated_data(message)

        pet = message.pets[0]
        assert len(pet.ability_bonus) == 2
        assert pet.ability_bonus[0].type == PetAbilityBonus.Type.TYPE_TEAM_TECH
        created = pet.ability_bonus[1]
        assert created.type == PetAbilityBonus.Type.TYPE_BASEVALUE
        assert created.value.hp.value == 20

    def test_multiple_pets(self):
        """应转换所有精灵"""
        message = _create_message(
            *[PetInfo(id=i, extra_hp=10 * i) for i in range(1, 4)]
        )

        convert_deprecated_data(message)

        for i, pet in enumerate(message.pets, start=1):
            assert pet.extra_hp == 0
            assert _find_basevalue_bonus(pet).value.hp.value == 10 * i

    def test_returns_same_message(self):
        """应原地修改并返回同一个消息对象"""
        message = _create_message(PetInfo(id=1, extra_hp=1))

        assert convert_deprecated_data(message) is message

    def test_empty_pets(self):
        """空精灵列表不应报错"""
        message = _create_message()

        assert convert_deprecated_data(message) is message
        assert len(message.pets) == 0
