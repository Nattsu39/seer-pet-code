"""pytest 配置和共享 fixtures"""

import pytest

from seerbp.petcode.v1.message_pb2 import (
    MintmarkInfo,
    PetAbilityBonus,
    PetAbilityValue,
    PetCodeMessage,
    PetInfo,
    ResistanceInfo,
)


@pytest.fixture
def sample_pet_ability():
    """创建示例精灵能力值"""
    return PetAbilityValue(
        hp=100, attack=120, defense=80, special_attack=90, special_defense=85, speed=110
    )


@pytest.fixture
def sample_pet_effect():
    """创建示例精灵特效"""
    return PetInfo.Effect(id=67, status=1, args=[1, 5])


@pytest.fixture
def sample_resistance():
    """创建示例抗性信息"""
    return ResistanceInfo(
        hurt=ResistanceInfo.Hurt(crit=35, regular=35, precent=35),
        ctl=[
            ResistanceInfo.StateItem(state_id=1, percent=55),
            ResistanceInfo.StateItem(state_id=2, percent=18),
            ResistanceInfo.StateItem(state_id=3, percent=10),
        ],
    )

@pytest.fixture
def sample_pet_ability_bonus():
    """创建示例精灵能力值加成"""
    return PetAbilityBonus(
        type=PetAbilityBonus.TYPE_SPECIAL, value=PetAbilityBonus.Value(
            hp=PetAbilityBonus.ExtraValue(value=100, percent=10),
            attack=PetAbilityBonus.ExtraValue(value=100, percent=11),
            defense=PetAbilityBonus.ExtraValue(percent=12),
            special_attack=PetAbilityBonus.ExtraValue(value=100, percent=13),
            special_defense=PetAbilityBonus.ExtraValue(value=100, percent=14),
            speed=PetAbilityBonus.ExtraValue(percent=15),
        ))

@pytest.fixture
def sample_pet_info(sample_pet_ability, sample_pet_effect, sample_resistance, sample_pet_ability_bonus):
    """创建示例精灵信息"""
    return PetInfo(
        id=3842,
        level=100,
        dv=31,
        ability_total=sample_pet_ability,
        evs=PetAbilityValue(
            hp=85, attack=85, defense=85, special_attack=7, special_defense=8, speed=9
        ),
        effects=[sample_pet_effect],
        skills=[24708, 31567, 31568, 31569],
        mintmarks=[MintmarkInfo(
            universal=MintmarkInfo.Universal(id=40001, level=5)
        )],
        nature=1,
        resistance=sample_resistance,
        is_awaken=False,
        pet_items=[300001, 300002],
        ability_bonus=[sample_pet_ability_bonus],
        skin_id=100001,
    )


@pytest.fixture
def sample_seer_set():
    """创建示例赛尔套装"""
    return PetCodeMessage.SeerSet(
        equips=[200001, 300001, 400001, 500001, 600001],
        title_id=100001,
    )


@pytest.fixture
def sample_petcode_message(sample_pet_info, sample_seer_set):
    """创建示例 PetCode 消息"""
    return PetCodeMessage(
        server=PetCodeMessage.Server.SERVER_OFFICIAL,
        display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
        seer_set=sample_seer_set,
        pets=[sample_pet_info],
    )

