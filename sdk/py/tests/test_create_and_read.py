"""测试辅助创建和读取函数"""

from petcode.create_and_read import (
    create_ability_mintmark,
    create_petcode_message,
    create_quanxiao_mintmark,
    create_skill_mintmark,
    create_state_resist,
    create_universal_mintmark,
    read_mintmark,
)
import pytest
from seerbp.petcode.v1.message_pb2 import (
    MintmarkInfo,
    PetAbilityValue,
    PetCodeMessage,
    ResistanceInfo,
)


class TestSkillMintmark:
    """测试技能刻印创建"""

    def test_create_skill_mintmark_basic(self):
        """测试基本的技能刻印创建"""
        mintmark = create_skill_mintmark(id=50001)

        assert isinstance(mintmark, MintmarkInfo)
        assert mintmark.WhichOneof('mintmark') == 'skill'
        assert mintmark.skill.id == 50001

    def test_create_skill_mintmark_various_ids(self):
        """测试不同 ID 的技能刻印"""
        ids = [50001, 50002, 50100, 59999]
        for test_id in ids:
            mintmark = create_skill_mintmark(id=test_id)
            assert mintmark.skill.id == test_id

    def test_skill_mintmark_read(self):
        """测试读取技能刻印"""
        mintmark = create_skill_mintmark(id=50001)
        data = read_mintmark(mintmark)

        assert isinstance(data, MintmarkInfo.Skill)
        assert data.id == 50001


class TestAbilityMintmark:
    """测试能力刻印创建"""

    def test_create_ability_mintmark_basic(self):
        """测试基本的能力刻印创建"""
        mintmark = create_ability_mintmark(id=60001)

        assert isinstance(mintmark, MintmarkInfo)
        assert mintmark.WhichOneof('mintmark') == 'ability'
        assert mintmark.ability.id == 60001

    def test_create_ability_mintmark_various_ids(self):
        """测试不同 ID 的能力刻印"""
        ids = [60001, 60002, 60100, 69999]
        for test_id in ids:
            mintmark = create_ability_mintmark(id=test_id)
            assert mintmark.ability.id == test_id

    def test_ability_mintmark_read(self):
        """测试读取能力刻印"""
        mintmark = create_ability_mintmark(id=60001)
        data = read_mintmark(mintmark)

        assert isinstance(data, MintmarkInfo.Ability)
        assert data.id == 60001


class TestUniversalMintmark:
    """测试全能刻印创建"""

    def test_create_universal_mintmark_basic(self):
        """测试基本的全能刻印创建"""
        mintmark = create_universal_mintmark(id=40001, level=5)

        assert isinstance(mintmark, MintmarkInfo)
        assert mintmark.WhichOneof('mintmark') == 'universal'
        assert mintmark.universal.id == 40001
        assert mintmark.universal.level == 5
        assert not mintmark.universal.HasField('gem')

    def test_create_universal_mintmark_all_levels(self):
        """测试所有等级的全能刻印"""
        for level in range(1, 6):  # 1-5 级
            mintmark = create_universal_mintmark(id=40001, level=level)
            assert mintmark.universal.level == level

    def test_create_universal_mintmark_with_gem(self):
        """测试带宝石的全能刻印"""
        mintmark = create_universal_mintmark(
            id=40001, level=5, gem_id=1800011, bind_skill_id=24708
        )

        assert mintmark.universal.id == 40001
        assert mintmark.universal.level == 5
        assert mintmark.universal.HasField('gem')
        assert mintmark.universal.gem.gem_id == 1800011
        assert mintmark.universal.gem.bind_skill_id == 24708

    def test_create_universal_mintmark_with_ability(self):
        """测试带自定义能力值的全能刻印"""
        ability = PetAbilityValue(
            hp=100,
            attack=120,
            defense=80,
            special_attack=90,
            special_defense=85,
            speed=110,
        )
        mintmark = create_universal_mintmark(id=40001, level=5, ability=ability)

        assert mintmark.universal.id == 40001
        assert mintmark.universal.level == 5
        assert mintmark.universal.HasField('ability')
        assert mintmark.universal.ability.hp == 100
        assert mintmark.universal.ability.attack == 120

    def test_create_universal_mintmark_with_gem_and_ability(self):
        """测试同时带宝石和能力值的全能刻印"""
        ability = PetAbilityValue(
            hp=100,
            attack=120,
            defense=80,
            special_attack=90,
            special_defense=85,
            speed=110,
        )
        mintmark = create_universal_mintmark(
            id=40001, level=5, gem_id=1800011, bind_skill_id=24708, ability=ability
        )

        assert mintmark.universal.HasField('gem')
        assert mintmark.universal.HasField('ability')
        assert mintmark.universal.gem.gem_id == 1800011
        assert mintmark.universal.ability.hp == 100

    def test_universal_mintmark_read(self):
        """测试读取全能刻印"""
        mintmark = create_universal_mintmark(id=40001, level=5)
        data = read_mintmark(mintmark)

        assert isinstance(data, MintmarkInfo.Universal)
        assert data.id == 40001
        assert data.level == 5


class TestQuanxiaoMintmark:
    """测试全效刻印创建"""

    def test_create_quanxiao_mintmark_basic(self):
        """测试基本的全效刻印创建"""
        mintmark = create_quanxiao_mintmark(id=70001, skill_mintmark_id=50001)

        assert isinstance(mintmark, MintmarkInfo)
        assert mintmark.WhichOneof('mintmark') == 'quanxiao'
        assert mintmark.quanxiao.id == 70001
        assert mintmark.quanxiao.skill_mintmark_id == 50001

    def test_create_quanxiao_mintmark_various_ids(self):
        """测试不同 ID 的全效刻印"""
        test_cases = [
            (70001, 50001),
            (70002, 50002),
            (70100, 50100),
        ]
        for ability_id, skill_id in test_cases:
            mintmark = create_quanxiao_mintmark(
                id=ability_id, skill_mintmark_id=skill_id
            )
            assert mintmark.quanxiao.id == ability_id
            assert mintmark.quanxiao.skill_mintmark_id == skill_id

    def test_quanxiao_mintmark_read(self):
        """测试读取全效刻印"""
        mintmark = create_quanxiao_mintmark(id=70001, skill_mintmark_id=50001)
        data = read_mintmark(mintmark)

        assert isinstance(data, MintmarkInfo.Quanxiao)
        assert data.id == 70001
        assert data.skill_mintmark_id == 50001


class TestReadMintmark:
    """测试读取刻印函数"""

    def test_read_skill_mintmark(self):
        """测试读取技能刻印"""
        mintmark = create_skill_mintmark(id=50001)
        data = read_mintmark(mintmark)
        assert isinstance(data, MintmarkInfo.Skill)

    def test_read_ability_mintmark(self):
        """测试读取能力刻印"""
        mintmark = create_ability_mintmark(id=60001)
        data = read_mintmark(mintmark)
        assert isinstance(data, MintmarkInfo.Ability)

    def test_read_universal_mintmark(self):
        """测试读取全能刻印"""
        mintmark = create_universal_mintmark(id=40001, level=5)
        data = read_mintmark(mintmark)
        assert isinstance(data, MintmarkInfo.Universal)

    def test_read_quanxiao_mintmark(self):
        """测试读取全效刻印"""
        mintmark = create_quanxiao_mintmark(id=70001, skill_mintmark_id=50001)
        data = read_mintmark(mintmark)
        assert isinstance(data, MintmarkInfo.Quanxiao)

    def test_read_empty_mintmark(self):
        """测试读取空刻印"""
        mintmark = MintmarkInfo()
        with pytest.raises(ValueError, match='Unknown mintmark type'):
            read_mintmark(mintmark)


class TestStateResist:
    """测试状态抗性创建"""

    def test_create_state_resist_basic(self):
        """测试基本的状态抗性创建"""
        resist = create_state_resist((1, 55), (2, 18), (3, 10))

        assert isinstance(resist, tuple)
        assert len(resist) == 3
        assert all(isinstance(item, ResistanceInfo.StateItem) for item in resist)

    def test_create_state_resist_values(self):
        """测试状态抗性的值"""
        resist = create_state_resist((1, 55), (2, 18), (3, 10))

        assert resist[0].state_id == 1
        assert resist[0].percent == 55
        assert resist[1].state_id == 2
        assert resist[1].percent == 18
        assert resist[2].state_id == 3
        assert resist[2].percent == 10

    def test_create_state_resist_various_values(self):
        """测试不同值的状态抗性"""
        test_cases = [
            ((1, 100), (2, 50), (3, 0)),
            ((10, 75), (20, 25), (30, 15)),
            ((5, 0), (6, 0), (7, 0)),
        ]
        for args1, args2, args3 in test_cases:
            resist = create_state_resist(args1, args2, args3)
            assert resist[0].state_id == args1[0]
            assert resist[0].percent == args1[1]
            assert resist[1].state_id == args2[0]
            assert resist[1].percent == args2[1]
            assert resist[2].state_id == args3[0]
            assert resist[2].percent == args3[1]

    def test_create_state_resist_in_resistance_info(self):
        """测试在 ResistanceInfo 中使用状态抗性"""
        ctl_resist = create_state_resist((1, 55), (2, 18), (3, 10))
        resistance = ResistanceInfo(
            hurt=ResistanceInfo.Hurt(crit=35, regular=35, precent=35), ctl=ctl_resist
        )

        assert len(resistance.ctl) == 3
        assert resistance.ctl[0].state_id == 1
        assert resistance.ctl[0].percent == 55


class TestCreatePetCodeMessage:
    """测试创建 PetCode 消息"""

    def test_create_petcode_message_basic(self, sample_pet_info, sample_seer_set):
        """测试基本的 PetCode 消息创建"""
        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=sample_seer_set,
            pets=[sample_pet_info],
        )

        assert isinstance(message, PetCodeMessage)
        assert message.server == PetCodeMessage.Server.SERVER_OFFICIAL
        assert message.display_mode == PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP
        assert len(message.pets) == 1
        assert len(message.seer_set.equips) == len(sample_seer_set.equips)

    def test_create_petcode_message_all_servers(self, sample_pet_info, sample_seer_set):
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
                seer_set=sample_seer_set,
                pets=[sample_pet_info],
            )
            assert message.server == server

    def test_create_petcode_message_all_display_modes(
        self, sample_pet_info, sample_seer_set
    ):
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
                seer_set=sample_seer_set,
                pets=[sample_pet_info],
            )
            assert message.display_mode == mode

    def test_create_petcode_message_multiple_pets(
        self, sample_pet_info, sample_seer_set
    ):
        """测试多只宠物"""
        from seerbp.petcode.v1.message_pb2 import PetAbilityValue, PetInfo

        pet2 = PetInfo(
            id=3843,
            level=100,
            dv=31,
            ability_total=PetAbilityValue(
                hp=110,
                attack=130,
                defense=90,
                special_attack=100,
                special_defense=95,
                speed=120,
            ),
        )

        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=sample_seer_set,
            pets=[sample_pet_info, pet2],
        )

        assert len(message.pets) == 2
        assert message.pets[0].id == 3842
        assert message.pets[1].id == 3843

    def test_create_petcode_message_empty_pets(self, sample_seer_set):
        """测试空宠物列表"""
        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=sample_seer_set,
            pets=[],
        )

        assert len(message.pets) == 0
        assert message.server == PetCodeMessage.Server.SERVER_OFFICIAL

    def test_create_petcode_message_full_featured(self):
        """测试完整功能的消息创建"""
        from seerbp.petcode.v1.message_pb2 import PetAbilityValue, PetInfo

        # 创建一个包含所有功能的宠物
        pet = PetInfo(
            id=3842,
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
            evs=PetAbilityValue(
                hp=255,
                attack=255,
                defense=255,
                special_attack=255,
                special_defense=255,
                speed=255,
            ),
            effects=[PetInfo.Effect(id=67, status=1, args=[1, 5])],
            skills=[24708, 31567, 31568, 31569],
            mintmarks=[create_universal_mintmark(id=40001, level=5)],
            nature=1,
        )

        seer_set = PetCodeMessage.SeerSet(
            equips=[200001, 300001, 400001, 500001, 600001]
        )

        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=seer_set,
            pets=[pet],
        )

        assert message.pets[0].id == 3842
        assert len(message.pets[0].skills) == 4
        assert len(message.pets[0].mintmarks) == 1
        assert message.pets[0].mintmarks[0].WhichOneof('mintmark') == 'universal'

    def test_create_petcode_message_with_battle_fires(
        self, sample_pet_info, sample_seer_set
    ):
        """测试带战斗火焰的消息创建"""
        battle_fires = [
            PetCodeMessage.BattleFire.BATTLE_FIRE_GREEN,
            PetCodeMessage.BattleFire.BATTLE_FIRE_BLUE,
        ]
        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=sample_seer_set,
            pets=[sample_pet_info],
            battle_fires=battle_fires,
        )

        assert len(message.battle_fires) == 2
        assert message.battle_fires[0] == PetCodeMessage.BattleFire.BATTLE_FIRE_GREEN
        assert message.battle_fires[1] == PetCodeMessage.BattleFire.BATTLE_FIRE_BLUE

    def test_create_petcode_message_with_all_battle_fires(
        self, sample_pet_info, sample_seer_set
    ):
        """测试所有类型的战斗火焰"""
        battle_fires = [
            PetCodeMessage.BattleFire.BATTLE_FIRE_GREEN,
            PetCodeMessage.BattleFire.BATTLE_FIRE_BLUE,
            PetCodeMessage.BattleFire.BATTLE_FIRE_PURPLE,
            PetCodeMessage.BattleFire.BATTLE_FIRE_GOLD,
        ]
        message = create_petcode_message(
            server=PetCodeMessage.Server.SERVER_OFFICIAL,
            display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
            seer_set=sample_seer_set,
            pets=[sample_pet_info],
            battle_fires=battle_fires,
        )

        assert len(message.battle_fires) == 4
        assert PetCodeMessage.BattleFire.BATTLE_FIRE_GOLD in message.battle_fires
