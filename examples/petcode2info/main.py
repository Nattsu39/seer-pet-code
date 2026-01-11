import asyncio
import base64

from google.protobuf import json_format
from petcode import PetCodeMessage, from_binary
from petcode.create_and_read import (
    read_mintmark,
)
from petcode.effect import EffectType, effect_to_param, get_effect_type
from seerapi import SeerAPI
from seerapi_models import (
    Nature,
    Pet,
    PetEffect,
    Skill,
    Soulmark,
    TypeCombination,
    VariationEffect,
)
from seerbp.petcode.v1.message_pb2 import MintmarkInfo


class DataFetcher:
    def __init__(self):
        self.client = SeerAPI()

    async def close(self):
        await self.client.aclose()

    async def fetch_pet_data(self, pet_id: int) -> Pet:
        return await self.client.get('pet', id=pet_id)

    async def fetch_skills(self, skill_ids: list[int]) -> dict[int, Skill]:
        skills = {}
        for sid in skill_ids:
            skill = await self.client.get('skill', id=sid)
            skills[sid] = skill

        return skills

    async def fetch_skill(self, skill_id: int) -> Skill:
        return await self.client.get('skill', id=skill_id)

    async def fetch_element_type(self, type_id: int) -> TypeCombination:
        return await self.client.get('element_type_combination', id=type_id)

    async def fetch_battle_effect_name(self, effect_id: int) -> str:
        return (await self.client.get('battle_effect', id=effect_id)).name

    async def fetch_pet_effect(self, effect_string: str) -> PetEffect:
        named_data = await self.client.get_by_name('pet_effect', name=effect_string)
        return next(iter(named_data.data.values()))

    async def fetch_variation_effect(self, effect_string: str) -> VariationEffect:
        named_data = await self.client.get_by_name('pet_variation', name=effect_string)
        return next(iter(named_data.data.values()))

    async def fetch_soulmark(self, effect_string: str) -> Soulmark:
        named_data = await self.client.get_by_name('soulmark', name=effect_string)
        return next(iter(named_data.data.values()))

    async def fetch_nature(self, nature_id: int) -> Nature:
        return await self.client.get('nature', id=nature_id)

    async def fetch_mintmark(self, mintmark_id: int):
        return await self.client.get('mintmark', id=mintmark_id)

    async def fetch_equip(self, suit_id: int):
        return await self.client.get('equip', id=suit_id)

    async def fetch_title(self, title_id: int):
        return await self.client.get('title', id=title_id)


FIRE_NAMES = {
    PetCodeMessage.BattleFire.BATTLE_FIRE_GREEN: '绿色火焰',
    PetCodeMessage.BattleFire.BATTLE_FIRE_BLUE: '蓝色火焰',
    PetCodeMessage.BattleFire.BATTLE_FIRE_PURPLE: '紫色火焰',
    PetCodeMessage.BattleFire.BATTLE_FIRE_GOLD: '金色火焰',
}


async def main(base64string: str):
    data_fetcher = DataFetcher()
    binary = base64.b64decode(base64string)
    message = from_binary(binary)
    print(f'服务器: {message.server}')
    print(f'显示模式: {message.display_mode}')
    pet_msg = message.pets[0]
    pet = await data_fetcher.fetch_pet_data(pet_msg.id)
    nature = await data_fetcher.fetch_nature(pet_msg.nature)
    skills = await data_fetcher.fetch_skills(list(pet_msg.skills))

    infos = [
        f'精灵名称：{pet.name}',
        f'精灵等级：{pet_msg.level}',
        f'精灵个体值：{pet_msg.dv}',
        f'精灵性格：{nature.name}',
        f'精灵额外体力上限：{pet_msg.extra_hp}',
    ]

    infos.append('精灵学习力：')
    for key, value in json_format.MessageToDict(pet_msg.evs).items():
        infos.append(f'  - {key}: {value}')

    infos.append('精灵携带的技能：')
    for skill in skills.values():
        infos.append(f'  - {skill.name}')

    infos.append('精灵特效：')
    for eff in pet_msg.effects:
        effect_type = get_effect_type(eff.status)
        param = effect_to_param(eff).name
        if effect_type == EffectType.GENERAL:
            general_effect = await data_fetcher.fetch_pet_effect(param)
            infos.append(
                f'  - 特性: {general_effect.name}LV{general_effect.star_level}, idx: {general_effect.id}'
            )
        elif effect_type == EffectType.SOULMARK:
            soulmark = await data_fetcher.fetch_soulmark(param)
            infos.append(f'  - 魂印id: {soulmark.id}')
        elif effect_type == EffectType.VARIATION:
            variation_effect = await data_fetcher.fetch_variation_effect(param)
            infos.append(f'  - 异能特质: {variation_effect.name}')

    infos.append('精灵装备的刻印：')
    for m in pet_msg.mintmarks:
        mintmark = read_mintmark(m)
        mintmark_info = await data_fetcher.fetch_mintmark(mintmark.id)
        infos.append(f'  - {mintmark_info.name}')
        if (
            isinstance(mintmark, MintmarkInfo.Universal)
            and mintmark.gem.bind_skill_id
            and mintmark.gem.gem_id
        ):
            infos.append(f'    - 宝石: {mintmark.gem.gem_id}')
            skill = await data_fetcher.fetch_skill(mintmark.gem.bind_skill_id)
            infos.append(f'    - 绑定技能: {skill.name}')

    infos.append('精灵携带的战斗道具：')
    for item in pet_msg.pet_items:
        infos.append(f'  - {item}')

    infos.append('精灵的抗性信息：')
    resistance = pet_msg.resistance
    infos.append(
        f'  - 暴击抗性: {resistance.hurt.crit} 固定伤害抗性: {resistance.hurt.regular} '
        f'百分比伤害抗性: {resistance.hurt.precent}'
    )

    for item in resistance.ctl:
        state_name = await data_fetcher.fetch_battle_effect_name(item.state_id)
        infos.append(f'  - 状态: {state_name} 抵抗概率: {item.percent}')

    for item in resistance.weak:
        state_name = await data_fetcher.fetch_battle_effect_name(item.state_id)
        infos.append(f'  - 状态: {state_name} 抵抗概率: {item.percent}')

    infos.append('精灵的额外能力值加成：')
    for item in pet_msg.ability_bonus:
        infos.append(f'  - 类型：{item.type}')
        for key, value in json_format.MessageToDict(item.value).items():
            infos.append(
                f'    - {key}: 固定加成：{value.get("value", 0)}, 百分比加成：{value.get("percent", 0)}%'
            )

    infos.append(f'精灵携带的皮肤：{pet_msg.skin_id}')
    infos.append(f'精灵是否神谕觉醒：{pet_msg.is_awaken}')

    infos.append('精灵的能力值总和：')
    for key, value in json_format.MessageToDict(pet_msg.ability_total).items():
        infos.append(f'  - {key}: {value}')

    infos.append('')
    infos.append('用户的套装信息：')
    for item in message.seer_set.equips:
        infos.append(f'  - {(await data_fetcher.fetch_equip(item)).name}')

    title_name = '无'
    if message.seer_set.title_id != 0:
        title_name = (await data_fetcher.fetch_title(message.seer_set.title_id)).name
    infos.append(f'用户的称号：{title_name}')

    infos.append('用户的战斗火焰：')
    if len(message.battle_fires) > 0:
        for item in message.battle_fires:
            infos.append(f'  - {FIRE_NAMES[item]}')
    else:
        infos.append('  - 无')

    print('\n'.join(infos))

    await data_fetcher.close()


if __name__ == '__main__':
    base64string: str = input('请输入 PetCode: ')
    asyncio.run(main(base64string))
