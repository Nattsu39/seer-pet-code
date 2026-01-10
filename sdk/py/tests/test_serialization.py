"""测试序列化和反序列化函数"""

import base64

import petcode
import pytest
from seerbp.petcode.v1.message_pb2 import PetCodeMessage


class TestBinarySerialization:
    """测试二进制序列化"""

    def test_to_binary_basic(self, sample_petcode_message):
        """测试基本的二进制序列化"""
        binary = petcode.to_binary(sample_petcode_message)
        assert isinstance(binary, bytes)
        assert len(binary) > 0

    def test_from_binary_basic(self, sample_petcode_message):
        """测试基本的二进制反序列化"""
        binary = petcode.to_binary(sample_petcode_message)
        restored = petcode.from_binary(binary)

        assert isinstance(restored, PetCodeMessage)
        assert restored.server == sample_petcode_message.server
        assert restored.display_mode == sample_petcode_message.display_mode
        assert len(restored.pets) == len(sample_petcode_message.pets)

    def test_binary_roundtrip(self, sample_petcode_message):
        """测试二进制序列化往返转换"""
        binary = petcode.to_binary(sample_petcode_message)
        restored = petcode.from_binary(binary)

        # 验证完整性
        assert restored.pets[0].id == sample_petcode_message.pets[0].id
        assert restored.pets[0].level == sample_petcode_message.pets[0].level
        assert (
            restored.pets[0].ability_total.hp
            == sample_petcode_message.pets[0].ability_total.hp
        )
        assert restored.pets[0].skills == sample_petcode_message.pets[0].skills

    def test_binary_compression(self, sample_petcode_message):
        """测试二进制数据被压缩"""
        binary = petcode.to_binary(sample_petcode_message)
        uncompressed = sample_petcode_message.SerializeToString()

        # 压缩后的数据应该更小（对于足够大的数据）
        # 注意：对于很小的数据，压缩可能会增加大小
        assert len(binary) <= len(uncompressed) + 100  # 允许一些压缩开销

    def test_from_binary_invalid_data(self):
        """测试使用无效数据进行反序列化"""
        with pytest.raises(Exception):  # gzip 或 protobuf 解析异常
            petcode.from_binary(b'invalid_data')

    def test_binary_empty_message(self):
        """测试空消息的序列化"""
        empty_msg = PetCodeMessage()
        binary = petcode.to_binary(empty_msg)
        restored = petcode.from_binary(binary)

        assert isinstance(restored, PetCodeMessage)
        assert restored.server == PetCodeMessage.Server.SERVER_UNSPECIFIED


class TestBase64Serialization:
    """测试 Base64 序列化"""

    def test_to_base64_basic(self, sample_petcode_message):
        """测试基本的 Base64 序列化"""
        b64_str = petcode.to_base64(sample_petcode_message)
        assert isinstance(b64_str, str)
        assert len(b64_str) > 0

    def test_to_base64_valid_format(self, sample_petcode_message):
        """测试 Base64 字符串格式有效"""
        b64_str = petcode.to_base64(sample_petcode_message)
        # 应该可以被 base64 解码
        try:
            base64.b64decode(b64_str)
        except Exception as e:
            pytest.fail(f'Base64 字符串格式无效: {e}')

    def test_from_base64_basic(self, sample_petcode_message):
        """测试基本的 Base64 反序列化"""
        b64_str = petcode.to_base64(sample_petcode_message)
        restored = petcode.from_base64(b64_str)

        assert isinstance(restored, PetCodeMessage)
        assert restored.server == sample_petcode_message.server
        assert restored.display_mode == sample_petcode_message.display_mode

    def test_base64_roundtrip(self, sample_petcode_message):
        """测试 Base64 序列化往返转换"""
        b64_str = petcode.to_base64(sample_petcode_message)
        restored = petcode.from_base64(b64_str)

        # 验证完整性
        assert restored.pets[0].id == sample_petcode_message.pets[0].id
        assert restored.pets[0].level == sample_petcode_message.pets[0].level
        assert restored.pets[0].nature == sample_petcode_message.pets[0].nature
        assert list(restored.pets[0].skills) == list(
            sample_petcode_message.pets[0].skills
        )

    def test_from_base64_invalid_string(self):
        """测试使用无效 Base64 字符串进行反序列化"""
        with pytest.raises(Exception):  # base64 解码或 gzip/protobuf 解析异常
            petcode.from_base64('invalid!!!base64')

    def test_base64_empty_message(self):
        """测试空消息的 Base64 序列化"""
        empty_msg = PetCodeMessage()
        b64_str = petcode.to_base64(empty_msg)
        restored = petcode.from_base64(b64_str)

        assert isinstance(restored, PetCodeMessage)
        assert len(restored.pets) == 0


class TestDictSerialization:
    """测试字典序列化"""

    def test_to_dict_basic(self, sample_petcode_message):
        """测试基本的字典序列化"""
        data = petcode.to_dict(sample_petcode_message)
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_to_dict_structure(self, sample_petcode_message):
        """测试字典结构"""
        data = petcode.to_dict(sample_petcode_message)

        # 验证主要字段存在
        assert 'server' in data
        assert 'displayMode' in data
        assert 'pets' in data
        assert isinstance(data['pets'], list)

    def test_from_dict_basic(self, sample_petcode_message):
        """测试基本的字典反序列化"""
        data = petcode.to_dict(sample_petcode_message)
        restored = petcode.from_dict(data)

        assert isinstance(restored, PetCodeMessage)
        assert restored.server == sample_petcode_message.server
        assert restored.display_mode == sample_petcode_message.display_mode

    def test_dict_roundtrip(self, sample_petcode_message):
        """测试字典序列化往返转换"""
        data = petcode.to_dict(sample_petcode_message)
        restored = petcode.from_dict(data)

        # 验证完整性
        assert restored.pets[0].id == sample_petcode_message.pets[0].id
        assert restored.pets[0].level == sample_petcode_message.pets[0].level
        assert restored.pets[0].dv == sample_petcode_message.pets[0].dv

    def test_from_dict_partial_data(self):
        """测试使用部分数据进行字典反序列化"""
        partial_data = {
            'server': 'SERVER_OFFICIAL',
            'displayMode': 'DISPLAY_MODE_PVP',
        }
        msg = petcode.from_dict(partial_data)

        assert msg.server == PetCodeMessage.Server.SERVER_OFFICIAL
        assert msg.display_mode == PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP
        assert len(msg.pets) == 0

    def test_dict_empty_message(self):
        """测试空消息的字典序列化"""
        empty_msg = PetCodeMessage()
        data = petcode.to_dict(empty_msg)
        restored = petcode.from_dict(data)

        assert isinstance(restored, PetCodeMessage)


class TestCrossFormatConversion:
    """测试跨格式转换"""

    def test_binary_to_base64_consistency(self, sample_petcode_message):
        """测试二进制和 Base64 的一致性"""
        binary = petcode.to_binary(sample_petcode_message)
        b64_str = petcode.to_base64(sample_petcode_message)

        # Base64 解码后应该等于二进制数据
        decoded_binary = base64.b64decode(b64_str)
        assert binary == decoded_binary

    def test_all_formats_roundtrip(self, sample_petcode_message):
        """测试所有格式的往返转换"""
        # Binary
        binary = petcode.to_binary(sample_petcode_message)
        from_binary = petcode.from_binary(binary)

        # Base64
        b64_str = petcode.to_base64(sample_petcode_message)
        from_b64 = petcode.from_base64(b64_str)

        # Dict
        data = petcode.to_dict(sample_petcode_message)
        from_dict = petcode.from_dict(data)

        # 验证所有格式恢复的消息一致
        assert from_binary.pets[0].id == from_b64.pets[0].id == from_dict.pets[0].id
        assert from_binary.server == from_b64.server == from_dict.server

    def test_format_conversion_chain(self, sample_petcode_message):
        """测试格式转换链"""
        # 原始 -> Base64 -> 二进制 -> Base64 -> 字典 -> 最终
        b64_1 = petcode.to_base64(sample_petcode_message)
        msg_1 = petcode.from_base64(b64_1)

        binary = petcode.to_binary(msg_1)
        msg_2 = petcode.from_binary(binary)

        data = petcode.to_dict(msg_2)
        final = petcode.from_dict(data)

        # 验证数据完整性
        assert final.pets[0].id == sample_petcode_message.pets[0].id
        assert final.pets[0].level == sample_petcode_message.pets[0].level


class TestEdgeCases:
    """测试边界情况"""

    def test_large_pet_list(self):
        """测试大量宠物列表的序列化"""
        from seerbp.petcode.v1.message_pb2 import PetAbilityValue, PetInfo

        pets = []
        for i in range(6):  # 创建 6 只宠物
            pets.append(
                PetInfo(
                    id=3842 + i,
                    level=100,
                    dv=31,
                    ability_total=PetAbilityValue(
                        hp=100,
                        attack=120,
                        defense=80,
                        special_attack=90,
                        special_defense=85,
                        speed=110,
                    ),
                )
            )

        msg = PetCodeMessage(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            pets=pets,
        )

        # 测试所有序列化方式
        binary = petcode.to_binary(msg)
        restored_binary = petcode.from_binary(binary)
        assert len(restored_binary.pets) == 6

        b64 = petcode.to_base64(msg)
        restored_b64 = petcode.from_base64(b64)
        assert len(restored_b64.pets) == 6

        data = petcode.to_dict(msg)
        restored_dict = petcode.from_dict(data)
        assert len(restored_dict.pets) == 6

    def test_unicode_in_message(self):
        """测试包含 Unicode 字符的消息"""
        # Protobuf 消息本身不包含字符串字段，但测试字典转换
        msg = PetCodeMessage(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
        )

        # 字典序列化应该能处理 Unicode
        data = petcode.to_dict(msg)
        restored = petcode.from_dict(data)
        assert restored.server == msg.server

    def test_special_values(self):
        """测试特殊值"""
        from seerbp.petcode.v1.message_pb2 import PetAbilityValue, PetInfo

        # 测试 0 值
        pet = PetInfo(
            id=0,
            level=1,
            dv=0,
            ability_total=PetAbilityValue(
                hp=0, attack=0, defense=0, special_attack=0, special_defense=0, speed=0
            ),
        )

        msg = PetCodeMessage(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            pets=[pet],
        )

        # 测试序列化
        binary = petcode.to_binary(msg)
        restored = petcode.from_binary(binary)
        assert restored.pets[0].dv == 0
        assert restored.pets[0].id == 0

    def test_battle_fires_serialization(self):
        """测试战斗火焰的序列化"""
        msg = PetCodeMessage(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            battle_fires=[
                PetCodeMessage.BattleFire.BATTLE_FIRE_GREEN,
                PetCodeMessage.BattleFire.BATTLE_FIRE_GOLD,
            ],
        )

        # Base64 往返测试
        b64 = petcode.to_base64(msg)
        restored = petcode.from_base64(b64)
        assert len(restored.battle_fires) == 2
        assert PetCodeMessage.BattleFire.BATTLE_FIRE_GREEN in restored.battle_fires
        assert PetCodeMessage.BattleFire.BATTLE_FIRE_GOLD in restored.battle_fires

        # Dict 往返测试
        data = petcode.to_dict(msg)
        assert 'battleFires' in data
        assert len(data['battleFires']) == 2
        restored_dict = petcode.from_dict(data)
        assert len(restored_dict.battle_fires) == 2
