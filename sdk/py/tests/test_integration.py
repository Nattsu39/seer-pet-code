"""集成测试 - 测试完整的使用场景"""

import pytest

import petcode
from petcode.create_and_read import (
    create_petcode_message,
    create_state_resist,
    create_universal_mintmark,
)
from petcode.effect import EffectParam, EffectType, effect_to_param, param_to_effect
from seerbp.petcode.v1.message_pb2 import (
    PetAbilityValue,
    PetCodeMessage,
    PetInfo,
    ResistanceInfo,
)


class TestCompleteWorkflow:
    """测试完整的工作流程"""

    def test_create_and_serialize_complete_pet(self):
        """测试创建并序列化完整的宠物配置"""
        # 1. 创建宠物信息
        pet = PetInfo(
            id=3842,
            level=100,
            dv=31,
            ability_total=PetAbilityValue(
                hp=418,
                attack=425,
                defense=349,
                special_attack=367,
                special_defense=355,
                speed=403,
            ),
            evs=PetAbilityValue(
                hp=255, attack=255, defense=255, special_attack=255, special_defense=255, speed=255
            ),
            effects=[PetInfo.Effect(id=67, status=1, args=[1, 5])],
            skills=[24708, 31567, 31568, 31569],
            mintmarks=[create_universal_mintmark(id=40001, level=5)],
            nature=1,
            resistance=ResistanceInfo(
                hurt=ResistanceInfo.Hurt(crit=35, regular=35, precent=35),
                ctl=create_state_resist((1, 55), (2, 18), (3, 10)),
            ),
        )

        # 2. 创建消息
        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=PetCodeMessage.SeerSet(equips=[200001, 300001, 400001]),
            pets=[pet],
        )

        # 3. 序列化为 Base64
        base64_code = petcode.to_base64(message)
        assert isinstance(base64_code, str)
        assert len(base64_code) > 0

        # 4. 反序列化
        restored = petcode.from_base64(base64_code)

        # 5. 验证所有数据
        assert restored.server == PetCodeMessage.Server.SERVER_OFFICIAL
        assert restored.display_mode == PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP
        assert len(restored.pets) == 1
        assert restored.pets[0].id == 3842
        assert restored.pets[0].level == 100
        assert restored.pets[0].ability_total.hp == 418
        assert len(restored.pets[0].skills) == 4
        assert len(restored.pets[0].mintmarks) == 1
        assert restored.pets[0].mintmarks[0].WhichOneof('mintmark') == 'universal'

    def test_multiple_serialization_formats(self):
        """测试使用多种序列化格式"""
        # 创建简单消息
        pet = PetInfo(
            id=3842,
            level=100,
            dv=31,
            ability_total=PetAbilityValue(
                hp=100, attack=120, defense=80, special_attack=90, special_defense=85, speed=110
            ),
        )

        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=PetCodeMessage.SeerSet(),
            pets=[pet],
        )

        # 测试所有序列化格式
        # 1. Binary
        binary = petcode.to_binary(message)
        from_bin = petcode.from_binary(binary)
        assert from_bin.pets[0].id == 3842

        # 2. Base64
        b64 = petcode.to_base64(message)
        from_b64 = petcode.from_base64(b64)
        assert from_b64.pets[0].id == 3842

        # 3. Dict
        data = petcode.to_dict(message)
        from_dict = petcode.from_dict(data)
        assert from_dict.pets[0].id == 3842

        # 所有格式应该产生相同的结果
        assert from_bin.pets[0].level == from_b64.pets[0].level == from_dict.pets[0].level

    def test_effect_processing_workflow(self):
        """测试特效处理工作流"""
        # 1. 创建带特效的宠物
        effects = [
            PetInfo.Effect(id=67, status=1, args=[1, 5]),
            PetInfo.Effect(id=100, status=4, args=[10]),
            PetInfo.Effect(id=200, status=5, args=[]),
        ]

        pet = PetInfo(
            id=3842,
            level=100,
            dv=31,
            ability_total=PetAbilityValue(
                hp=100, attack=120, defense=80, special_attack=90, special_defense=85, speed=110
            ),
            effects=effects,
        )

        # 2. 转换特效为参数
        params = [effect_to_param(effect) for effect in effects]

        assert len(params) == 3
        assert params[0].type == EffectType.GENERAL
        assert params[1].type == EffectType.VARIATION
        assert params[2].type == EffectType.SOULMARK

        # 3. 参数转回特效
        restored_effects = [param_to_effect(param) for param in params]

        for i, effect in enumerate(restored_effects):
            assert effect.id == effects[i].id
            assert list(effect.args) == list(effects[i].args)

    def test_team_configuration_workflow(self):
        """测试队伍配置工作流"""
        # 创建一个6只宠物的队伍
        pets = []
        for i in range(6):
            pet = PetInfo(
                id=3842 + i,
                level=100,
                dv=31,
                ability_total=PetAbilityValue(
                    hp=100 + i * 10,
                    attack=120 + i * 10,
                    defense=80 + i * 10,
                    special_attack=90 + i * 10,
                    special_defense=85 + i * 10,
                    speed=110 + i * 10,
                ),
                mintmarks=[create_universal_mintmark(id=40001 + i, level=5)],
            )
            pets.append(pet)

        # 创建消息
        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=PetCodeMessage.SeerSet(equips=[200001, 300001, 400001]),
            pets=pets,
        )

        # 序列化和反序列化
        base64_code = petcode.to_base64(message)
        restored = petcode.from_base64(base64_code)

        # 验证所有宠物
        assert len(restored.pets) == 6
        for i, pet in enumerate(restored.pets):
            assert pet.id == 3842 + i
            assert pet.ability_total.hp == 100 + i * 10
            assert len(pet.mintmarks) == 1
            assert pet.mintmarks[0].universal.id == 40001 + i


class TestRealWorldScenarios:
    """测试真实世界使用场景"""

    def test_pvp_battle_configuration(self):
        """测试 PVP 战斗配置"""
        # 创建一个完整的 PVP 配置
        pets = []
        for i in range(6):
            pet = PetInfo(
                id=3842 + i,
                level=100,
                dv=31,
                ability_total=PetAbilityValue(
                    hp=400, attack=400, defense=350, special_attack=350, special_defense=350, speed=400
                ),
                evs=PetAbilityValue(
                    hp=255, attack=255, defense=255, special_attack=255, special_defense=255, speed=255
                ),
                skills=[24708 + i * 10, 31567, 31568, 31569],
                mintmarks=[create_universal_mintmark(id=40001, level=5)],
                nature=i % 25,  # 不同性格
            )
            pets.append(pet)

        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=PetCodeMessage.SeerSet(equips=[200001, 300001, 400001]),
            pets=pets,
        )

        # 生成分享码
        share_code = petcode.to_base64(message)

        # 模拟分享：接收方解析分享码
        received = petcode.from_base64(share_code)

        assert received.display_mode == PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP
        assert len(received.pets) == 6
        for i, pet in enumerate(received.pets):
            assert pet.nature == i % 25

    def test_pve_boss_configuration(self):
        """测试 PVE BOSS 配置"""
        # 创建一个 BOSS 战配置
        pet = PetInfo(
            id=3842,
            level=100,
            dv=31,
            ability_total=PetAbilityValue(
                hp=500, attack=450, defense=400, special_attack=450, special_defense=400, speed=350
            ),
            evs=PetAbilityValue(
                hp=255, attack=255, defense=255, special_attack=255, special_defense=255, speed=255
            ),
            effects=[
                PetInfo.Effect(id=67, status=1, args=[1, 5]),
                PetInfo.Effect(id=100, status=1, args=[10]),
            ],
            skills=[24708, 31567, 31568, 31569],
            mintmarks=[create_universal_mintmark(
                id=40001, level=5, gem_id=1800011, bind_skill_id=24708
            )],
            resistance=ResistanceInfo(
                hurt=ResistanceInfo.Hurt(crit=50, regular=50, precent=50),
                ctl=create_state_resist((1, 100), (2, 100), (3, 100)),
            ),
        )

        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_BOSS,
            seer_set=PetCodeMessage.SeerSet(),
            pets=[pet],
        )

        # 保存到文件模拟
        binary = petcode.to_binary(message)
        # 从文件读取模拟
        loaded = petcode.from_binary(binary)

        assert loaded.display_mode == PetCodeMessage.DisplayMode.DISPLAY_MODE_BOSS
        assert len(loaded.pets[0].effects) == 2
        assert len(loaded.pets[0].mintmarks) == 1
        assert loaded.pets[0].mintmarks[0].universal.HasField('gem')

    def test_api_json_exchange(self):
        """测试 API JSON 数据交换"""
        import json

        # 创建配置
        pet = PetInfo(
            id=3842,
            level=100,
            dv=31,
            ability_total=PetAbilityValue(
                hp=100, attack=120, defense=80, special_attack=90, special_defense=85, speed=110
            ),
        )

        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=PetCodeMessage.SeerSet(),
            pets=[pet],
        )

        # 转换为字典，模拟 API 响应
        data = petcode.to_dict(message)

        # 转换为 JSON 字符串
        json_str = json.dumps(data, ensure_ascii=False)
        assert isinstance(json_str, str)

        # 解析 JSON，模拟 API 请求
        parsed_data = json.loads(json_str)
        restored = petcode.from_dict(parsed_data)

        assert restored.pets[0].id == 3842
        assert restored.server == PetCodeMessage.Server.SERVER_OFFICIAL

    def test_database_storage_simulation(self):
        """测试数据库存储模拟"""
        # 创建配置
        pet = PetInfo(
            id=3842,
            level=100,
            dv=31,
            ability_total=PetAbilityValue(
                hp=100, attack=120, defense=80, special_attack=90, special_defense=85, speed=110
            ),
        )

        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=PetCodeMessage.SeerSet(),
            pets=[pet],
        )

        # 序列化为二进制，模拟存入数据库
        binary_data = petcode.to_binary(message)

        # 模拟从数据库读取
        loaded_message = petcode.from_binary(binary_data)

        assert loaded_message.pets[0].id == 3842
        assert loaded_message.pets[0].level == 100


class TestErrorHandlingAndEdgeCases:
    """测试错误处理和边界情况"""

    def test_empty_pet_list(self):
        """测试空宠物列表"""
        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=PetCodeMessage.SeerSet(),
            pets=[],
        )

        # 应该能正常序列化和反序列化
        b64 = petcode.to_base64(message)
        restored = petcode.from_base64(b64)

        assert len(restored.pets) == 0
        assert restored.server == PetCodeMessage.Server.SERVER_OFFICIAL

    def test_minimal_pet_configuration(self):
        """测试最小宠物配置"""
        # 只包含必需字段
        pet = PetInfo(
            id=3842,
            level=1,
        )

        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=PetCodeMessage.SeerSet(),
            pets=[pet],
        )

        b64 = petcode.to_base64(message)
        restored = petcode.from_base64(b64)

        assert restored.pets[0].id == 3842
        assert restored.pets[0].level == 1

    def test_all_server_types(self):
        """测试所有服务器类型"""
        servers = [
            PetCodeMessage.Server.SERVER_OFFICIAL,
            PetCodeMessage.Server.SERVER_TEST,
            PetCodeMessage.Server.SERVER_TAIWAN,
            PetCodeMessage.Server.SERVER_CLASSIC,
        ]

        for server in servers:
            message = create_petcode_message(
                server=server,
                display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
                seer_set=PetCodeMessage.SeerSet(),
                pets=[],
            )

            b64 = petcode.to_base64(message)
            restored = petcode.from_base64(b64)
            assert restored.server == server

    def test_all_display_modes(self):
        """测试所有展示模式"""
        modes = [
            PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            PetCodeMessage.DisplayMode.DISPLAY_MODE_PVE,
            PetCodeMessage.DisplayMode.DISPLAY_MODE_BOSS,
        ]

        for mode in modes:
            message = create_petcode_message(
                server=PetCodeMessage.Server.SERVER_OFFICIAL,
                display_mode=mode,
                seer_set=PetCodeMessage.SeerSet(),
                pets=[],
            )

            b64 = petcode.to_base64(message)
            restored = petcode.from_base64(b64)
            assert restored.display_mode == mode

    def test_data_size_comparison(self):
        """测试不同格式的数据大小"""
        # 创建一个包含多只宠物的消息
        pets = []
        for i in range(6):
            pet = PetInfo(
                id=3842 + i,
                level=100,
                dv=31,
                ability_total=PetAbilityValue(
                    hp=100, attack=120, defense=80, special_attack=90, special_defense=85, speed=110
                ),
                skills=[24708, 31567, 31568, 31569],
            )
            pets.append(pet)

        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=PetCodeMessage.SeerSet(),
            pets=pets,
        )

        # 比较不同格式的大小
        binary = petcode.to_binary(message)
        base64_str = petcode.to_base64(message)
        dict_data = petcode.to_dict(message)

        import json

        json_str = json.dumps(dict_data)

        # Base64 应该比 JSON 更紧凑
        assert len(base64_str) < len(json_str)

        # 二进制应该更小（或相近）
        assert len(binary) <= len(base64_str) * 3 / 4 + 10  # Base64 编码开销
