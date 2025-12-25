from typing import overload

from seerbp.petcode.v1.message_pb2 import (
    MintmarkInfo,
    PetAbilityValue,
    PetCodeMessage,
    PetInfo,
    ResistanceInfo,
)


def create_skill_mintmark(id: int):
    return MintmarkInfo(skill=MintmarkInfo.Skill(id=id))


def create_ability_mintmark(id: int):
    return MintmarkInfo(ability=MintmarkInfo.Ability(id=id))


@overload
def create_universal_mintmark(
    id: int, level: int, *, ability: PetAbilityValue | None = None
) -> MintmarkInfo: ...
@overload
def create_universal_mintmark(
    id: int,
    level: int,
    *,
    gem_id: int,
    bind_skill_id: int,
    ability: PetAbilityValue | None = None,
) -> MintmarkInfo: ...


def create_universal_mintmark(
    id: int,
    level: int,
    *,
    gem_id: int | None = None,
    bind_skill_id: int | None = None,
    ability: PetAbilityValue | None = None,
) -> MintmarkInfo:
    gem = None
    if gem_id is not None and bind_skill_id is not None:
        gem = MintmarkInfo.Universal.GemItem(gem_id=gem_id, bind_skill_id=bind_skill_id)
    return MintmarkInfo(
        universal=MintmarkInfo.Universal(
            id=id,
            level=level,
            gem=gem,
            ability=ability,
        )
    )


def create_quanxiao_mintmark(id: int, *, skill_mintmark_id: int):
    return MintmarkInfo(
        quanxiao=MintmarkInfo.Quanxiao(id=id, skill_mintmark_id=skill_mintmark_id)
    )


def read_mintmark(
    mintmark: MintmarkInfo,
) -> (
    MintmarkInfo.Skill
    | MintmarkInfo.Ability
    | MintmarkInfo.Universal
    | MintmarkInfo.Quanxiao
):
    if mintmark.WhichOneof('mintmark') == 'skill':
        return mintmark.skill
    elif mintmark.WhichOneof('mintmark') == 'ability':
        return mintmark.ability
    elif mintmark.WhichOneof('mintmark') == 'universal':
        return mintmark.universal
    elif mintmark.WhichOneof('mintmark') == 'quanxiao':
        return mintmark.quanxiao
    else:
        raise ValueError(f'Unknown mintmark type: {mintmark.WhichOneof("mintmark")}')


def create_state_resist(
    args1: tuple[int, int],
    args2: tuple[int, int],
    args3: tuple[int, int],
) -> tuple[
    ResistanceInfo.StateItem, ResistanceInfo.StateItem, ResistanceInfo.StateItem
]:
    return (
        ResistanceInfo.StateItem(state_id=args1[0], percent=args1[1]),
        ResistanceInfo.StateItem(state_id=args2[0], percent=args2[1]),
        ResistanceInfo.StateItem(state_id=args3[0], percent=args3[1]),
    )


def create_petcode_message(
    server: PetCodeMessage.Server,
    display_mode: PetCodeMessage.DisplayMode,
    seer_set: PetCodeMessage.SeerSet,
    pets: list[PetInfo],
) -> PetCodeMessage:
    return PetCodeMessage(
        server=server,
        display_mode=display_mode,
        seer_set=seer_set,
        pets=pets,
    )
