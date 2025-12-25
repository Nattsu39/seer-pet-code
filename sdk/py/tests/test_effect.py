"""测试效果处理函数"""

import pytest

from petcode.effect import (
    EffectParam,
    EffectType,
    effect_to_param,
    get_effect_type,
    param_to_effect,
)
from seerbp.petcode.v1.message_pb2 import PetInfo


class TestEffectType:
    """测试效果类型枚举"""

    def test_effect_type_values(self):
        """测试效果类型的值"""
        assert EffectType.NONE == 0
        assert EffectType.GENERAL == 1
        assert EffectType.ITEM == 2
        assert EffectType.VARIATION == 4
        assert EffectType.SOULMARK == 5
        assert EffectType.TEAM_TECH == 7
        assert EffectType.OTHER == 99

    def test_effect_type_is_int_enum(self):
        """测试效果类型是 IntEnum"""
        assert isinstance(EffectType.GENERAL, int)
        assert EffectType.GENERAL.value == 1

    def test_effect_type_comparison(self):
        """测试效果类型比较"""
        assert EffectType.NONE < EffectType.GENERAL
        assert EffectType.GENERAL < EffectType.ITEM
        assert EffectType.OTHER > EffectType.TEAM_TECH


class TestGetEffectType:
    """测试获取效果类型函数"""

    def test_get_effect_type_none(self):
        """测试无效果类型"""
        result = get_effect_type(0)
        assert result == EffectType.NONE

    def test_get_effect_type_general(self):
        """测试特性类型"""
        result = get_effect_type(1)
        assert result == EffectType.GENERAL

    def test_get_effect_type_item(self):
        """测试道具效果类型"""
        result = get_effect_type(2)
        assert result == EffectType.ITEM

    def test_get_effect_type_variation(self):
        """测试异能特质类型"""
        result = get_effect_type(4)
        assert result == EffectType.VARIATION

    def test_get_effect_type_soulmark(self):
        """测试魂印类型"""
        result = get_effect_type(5)
        assert result == EffectType.SOULMARK

    def test_get_effect_type_team_tech(self):
        """测试战队科技类型"""
        result = get_effect_type(7)
        assert result == EffectType.TEAM_TECH

    def test_get_effect_type_unknown(self):
        """测试未知类型返回 OTHER"""
        unknown_values = [3, 6, 8, 10, 100, 999, -1]
        for value in unknown_values:
            result = get_effect_type(value)
            assert result == EffectType.OTHER


class TestEffectToParam:
    """测试效果转换为参数函数"""

    def test_effect_to_param_basic(self):
        """测试基本的效果转参数"""
        effect = PetInfo.Effect(id=67, status=1, args=[1, 5])
        param = effect_to_param(effect)

        assert isinstance(param, EffectParam)
        assert param.type == EffectType.GENERAL
        assert param.name == "67_1_5"

    def test_effect_to_param_no_args(self):
        """测试无参数的效果"""
        effect = PetInfo.Effect(id=100, status=1, args=[])
        param = effect_to_param(effect)

        assert param.type == EffectType.GENERAL
        assert param.name == "100"

    def test_effect_to_param_single_arg(self):
        """测试单个参数的效果"""
        effect = PetInfo.Effect(id=200, status=4, args=[10])
        param = effect_to_param(effect)

        assert param.type == EffectType.VARIATION
        assert param.name == "200_10"

    def test_effect_to_param_multiple_args(self):
        """测试多个参数的效果"""
        effect = PetInfo.Effect(id=300, status=1, args=[1, 2, 3, 4, 5])
        param = effect_to_param(effect)

        assert param.type == EffectType.GENERAL
        assert param.name == "300_1_2_3_4_5"

    def test_effect_to_param_various_types(self):
        """测试不同类型的效果"""
        test_cases = [
            (PetInfo.Effect(id=1, status=0, args=[]), EffectType.NONE, "1"),
            (PetInfo.Effect(id=2, status=1, args=[1]), EffectType.GENERAL, "2_1"),
            (PetInfo.Effect(id=3, status=2, args=[2]), EffectType.ITEM, "3_2"),
            (PetInfo.Effect(id=4, status=4, args=[3]), EffectType.VARIATION, "4_3"),
            (PetInfo.Effect(id=5, status=5, args=[4]), EffectType.SOULMARK, "5_4"),
            (PetInfo.Effect(id=6, status=7, args=[5]), EffectType.TEAM_TECH, "6_5"),
            (PetInfo.Effect(id=7, status=99, args=[6]), EffectType.OTHER, "7_6"),
        ]

        for effect, expected_type, expected_name in test_cases:
            param = effect_to_param(effect)
            assert param.type == expected_type
            assert param.name == expected_name

    def test_effect_to_param_large_numbers(self):
        """测试大数值的效果"""
        effect = PetInfo.Effect(id=999999, status=1, args=[100000, 200000])
        param = effect_to_param(effect)

        assert param.type == EffectType.GENERAL
        assert param.name == "999999_100000_200000"


class TestParamToEffect:
    """测试参数转换为效果函数"""

    def test_param_to_effect_basic(self):
        """测试基本的参数转效果"""
        param = EffectParam(type=EffectType.GENERAL, name="67_1_5")
        effect = param_to_effect(param)

        assert isinstance(effect, PetInfo.Effect)
        assert effect.id == 67
        assert effect.status == 1
        assert list(effect.args) == [1, 5]

    def test_param_to_effect_no_args(self):
        """测试无参数的转换"""
        param = EffectParam(type=EffectType.GENERAL, name="100")
        effect = param_to_effect(param)

        assert effect.id == 100
        assert effect.status == 1
        assert len(effect.args) == 0

    def test_param_to_effect_single_arg(self):
        """测试单个参数的转换"""
        param = EffectParam(type=EffectType.VARIATION, name="200_10")
        effect = param_to_effect(param)

        assert effect.id == 200
        assert effect.status == 4
        assert list(effect.args) == [10]

    def test_param_to_effect_multiple_args(self):
        """测试多个参数的转换"""
        param = EffectParam(type=EffectType.GENERAL, name="300_1_2_3_4_5")
        effect = param_to_effect(param)

        assert effect.id == 300
        assert effect.status == 1
        assert list(effect.args) == [1, 2, 3, 4, 5]

    def test_param_to_effect_various_types(self):
        """测试不同类型的参数转换"""
        test_cases = [
            (EffectParam(type=EffectType.NONE, name="1"), 1, 0, []),
            (EffectParam(type=EffectType.GENERAL, name="2_1"), 2, 1, [1]),
            (EffectParam(type=EffectType.ITEM, name="3_2"), 3, 2, [2]),
            (EffectParam(type=EffectType.VARIATION, name="4_3"), 4, 4, [3]),
            (EffectParam(type=EffectType.SOULMARK, name="5_4"), 5, 5, [4]),
            (EffectParam(type=EffectType.TEAM_TECH, name="6_5"), 6, 7, [5]),
            (EffectParam(type=EffectType.OTHER, name="7_6"), 7, 99, [6]),
        ]

        for param, expected_id, expected_status, expected_args in test_cases:
            effect = param_to_effect(param)
            assert effect.id == expected_id
            assert effect.status == expected_status
            assert list(effect.args) == expected_args

    def test_param_to_effect_large_numbers(self):
        """测试大数值的参数转换"""
        param = EffectParam(type=EffectType.GENERAL, name="999999_100000_200000")
        effect = param_to_effect(param)

        assert effect.id == 999999
        assert effect.status == 1
        assert list(effect.args) == [100000, 200000]


class TestEffectConversionRoundtrip:
    """测试效果转换往返"""

    def test_effect_param_roundtrip_basic(self):
        """测试基本的往返转换"""
        original = PetInfo.Effect(id=67, status=1, args=[1, 5])
        param = effect_to_param(original)
        restored = param_to_effect(param)

        assert restored.id == original.id
        assert restored.status == original.status
        assert list(restored.args) == list(original.args)

    def test_param_effect_roundtrip_basic(self):
        """测试参数到效果的往返转换"""
        original = EffectParam(type=EffectType.GENERAL, name="67_1_5")
        effect = param_to_effect(original)
        restored = effect_to_param(effect)

        assert restored.type == original.type
        assert restored.name == original.name

    def test_roundtrip_various_effects(self):
        """测试各种效果的往返转换"""
        test_effects = [
            PetInfo.Effect(id=1, status=0, args=[]),
            PetInfo.Effect(id=100, status=1, args=[10]),
            PetInfo.Effect(id=200, status=2, args=[20, 30]),
            PetInfo.Effect(id=300, status=4, args=[1, 2, 3]),
            PetInfo.Effect(id=400, status=5, args=[5]),
            PetInfo.Effect(id=500, status=7, args=[10, 20, 30, 40]),
        ]

        for original in test_effects:
            param = effect_to_param(original)
            restored = param_to_effect(param)

            assert restored.id == original.id
            assert restored.status == original.status
            assert list(restored.args) == list(original.args)

    def test_roundtrip_chain(self):
        """测试连续往返转换"""
        original = PetInfo.Effect(id=67, status=1, args=[1, 5])

        # 多次转换
        for _ in range(5):
            param = effect_to_param(original)
            original = param_to_effect(param)

        # 验证数据仍然正确
        assert original.id == 67
        assert original.status == 1
        assert list(original.args) == [1, 5]


class TestEffectParam:
    """测试 EffectParam 类"""

    def test_effect_param_creation(self):
        """测试 EffectParam 创建"""
        param = EffectParam(type=EffectType.GENERAL, name="67_1_5")

        assert param.type == EffectType.GENERAL
        assert param.name == "67_1_5"

    def test_effect_param_is_namedtuple(self):
        """测试 EffectParam 是 NamedTuple"""
        param = EffectParam(type=EffectType.GENERAL, name="67_1_5")

        # NamedTuple 的特性
        assert hasattr(param, '_fields')
        assert param._fields == ('type', 'name')

    def test_effect_param_immutable(self):
        """测试 EffectParam 不可变"""
        param = EffectParam(type=EffectType.GENERAL, name="67_1_5")

        with pytest.raises(AttributeError):
            param.type = EffectType.ITEM

    def test_effect_param_indexing(self):
        """测试 EffectParam 索引访问"""
        param = EffectParam(type=EffectType.GENERAL, name="67_1_5")

        assert param[0] == EffectType.GENERAL
        assert param[1] == "67_1_5"

    def test_effect_param_unpacking(self):
        """测试 EffectParam 解包"""
        param = EffectParam(type=EffectType.GENERAL, name="67_1_5")
        effect_type, name = param

        assert effect_type == EffectType.GENERAL
        assert name == "67_1_5"

    def test_effect_param_equality(self):
        """测试 EffectParam 相等性"""
        param1 = EffectParam(type=EffectType.GENERAL, name="67_1_5")
        param2 = EffectParam(type=EffectType.GENERAL, name="67_1_5")
        param3 = EffectParam(type=EffectType.ITEM, name="67_1_5")

        assert param1 == param2
        assert param1 != param3


class TestEdgeCases:
    """测试边界情况"""

    def test_effect_with_zero_values(self):
        """测试零值效果"""
        effect = PetInfo.Effect(id=0, status=0, args=[0, 0])
        param = effect_to_param(effect)
        restored = param_to_effect(param)

        assert restored.id == 0
        assert restored.status == 0
        assert list(restored.args) == [0, 0]

    def test_effect_with_negative_args(self):
        """测试负数参数的效果"""
        effect = PetInfo.Effect(id=100, status=1, args=[-1, -5, -10])
        param = effect_to_param(effect)

        # name 会包含负数
        assert param.name == "100_-1_-5_-10"

        restored = param_to_effect(param)
        assert list(restored.args) == [-1, -5, -10]

    def test_param_with_complex_name(self):
        """测试复杂名称的参数"""
        param = EffectParam(type=EffectType.GENERAL, name="12345_0_-1_999_100000")
        effect = param_to_effect(param)

        assert effect.id == 12345
        assert list(effect.args) == [0, -1, 999, 100000]

    def test_unknown_status_roundtrip(self):
        """测试未知 status 的往返转换"""
        effect = PetInfo.Effect(id=100, status=888, args=[1, 2])
        param = effect_to_param(effect)

        # 未知 status 应该被标记为 OTHER
        assert param.type == EffectType.OTHER

        restored = param_to_effect(param)
        # status 应该恢复为 OTHER 的值 (99)
        assert restored.status == 99
        assert restored.id == 100
        assert list(restored.args) == [1, 2]

