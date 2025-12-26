import { describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  createAbilityMintmark,
  createSkillMintmark,
  createQuanxiaoMintmark,
  createUniversalMintmark,
  readMintmark,
  createStateResist,
  createPetCodeMessage,
} from "../src/create_and_read.js";
import { PetCodeMessage_DisplayMode, PetCodeMessage_Server, PetInfoSchema, ResistanceInfoSchema } from "../src/generated/seerbp/petcode/v1/message_pb.js";
import { create } from "@bufbuild/protobuf";

describe("create_and_read", () => {
  describe("createAbilityMintmark", () => {
    it("应该创建能力刻印", () => {
      const mintmark = createAbilityMintmark(123);
      assert.equal(mintmark.mintmark.case, "ability");
      assert.equal(mintmark.mintmark.value.id, 123);
    });

    it("应该处理不同的ID值", () => {
      const mintmark1 = createAbilityMintmark(1);
      const mintmark2 = createAbilityMintmark(999999);
      assert.equal(mintmark1.mintmark.value?.id, 1);
      assert.equal(mintmark2.mintmark.value?.id, 999999);
    });
  });

  describe("createSkillMintmark", () => {
    it("应该创建技能刻印", () => {
      const mintmark = createSkillMintmark(456);
      assert.equal(mintmark.mintmark.case, "skill");
      assert.equal(mintmark.mintmark.value.id, 456);
    });
  });

  describe("createQuanxiaoMintmark", () => {
    it("应该创建全效刻印", () => {
      const mintmark = createQuanxiaoMintmark(100, 200);
      assert.equal(mintmark.mintmark.case, "quanxiao");
      assert.equal(mintmark.mintmark.value.id, 100);
      assert.equal(mintmark.mintmark.value.skillMintmarkId, 200);
    });

    it("应该处理不同的ID值组合", () => {
      const mintmark = createQuanxiaoMintmark(1, 2);
      assert.equal(mintmark.mintmark.value?.id, 1);
      assert.equal(mintmark.mintmark.value?.skillMintmarkId, 2);
    });
  });

  describe("createUniversalMintmark", () => {
    it("应该创建全能刻印（不带可选参数）", () => {
      const mintmark = createUniversalMintmark(300, 5, {});
      assert.equal(mintmark.mintmark.case, "universal");
      assert.equal(mintmark.mintmark.value?.id, 300);
      assert.equal(mintmark.mintmark.value?.level, 5);
    });

    it("应该创建全能刻印（带能力值）", () => {
      const mintmark = createUniversalMintmark(300, 5, {
        ability: {
          hp: 100,
          attack: 50,
          defense: 30,
          specialAttack: 60,
          specialDefense: 40,
          speed: 20,
        },
      });
      assert.equal(mintmark.mintmark.case, "universal");
      assert.equal(mintmark.mintmark.value.id, 300);
      assert.equal(mintmark.mintmark.value.level, 5);
      assert.equal(mintmark.mintmark.value?.ability?.hp, 100);
      assert.equal(mintmark.mintmark.value?.ability?.attack, 50);
    });

    it("应该创建全能刻印（带宝石）", () => {
      const mintmark = createUniversalMintmark(300, 5, {
        gem: { id: 10, bindSkillId: 20 },
      });
      assert.equal(mintmark.mintmark.case, "universal");
      assert.equal(mintmark.mintmark.value?.gem?.gemId, 10);
      assert.equal(mintmark.mintmark.value?.gem.bindSkillId, 20);
    });

    it("应该创建全能刻印（带能力值和宝石）", () => {
      const mintmark = createUniversalMintmark(300, 5, {
        ability: { hp: 100, attack: 50, defense: 30, specialAttack: 60, specialDefense: 40, speed: 20 },
        gem: { id: 10, bindSkillId: 20 },
      });
      assert.equal(mintmark.mintmark.value?.ability?.hp, 100);
      assert.equal(mintmark.mintmark.value?.gem?.gemId, 10);
    });
  });

  describe("readMintmark", () => {
    it("应该读取能力刻印", () => {
      const mintmark = createAbilityMintmark(123);
      const value = readMintmark(mintmark);
      assert.equal(value.id, 123);
    });

    it("应该读取技能刻印", () => {
      const mintmark = createSkillMintmark(456);
      const value = readMintmark(mintmark);
      assert.equal(value.id, 456);
    });

    it("应该读取全效刻印", () => {
      const mintmark = createQuanxiaoMintmark(100, 200);
      const value = readMintmark(mintmark);
      assert.equal(value.id, 100);
      assert.equal(value.skillMintmarkId, 200);
    });

    it("应该读取全能刻印", () => {
      const mintmark = createUniversalMintmark(300, 5, {});
      const value = readMintmark(mintmark);
      assert.equal(value.id, 300);
      assert.equal(value.level, 5);
    });
  });

  describe("createStateResist", () => {
    it("应该创建异常抗性列表", () => {
      const resists = createStateResist([1, 50], [2, 75], [3, 100]);
      assert.equal(resists.length, 3);
      assert.equal(resists[0].stateId, 1);
      assert.equal(resists[0].percent, 50);
      assert.equal(resists[1].stateId, 2);
      assert.equal(resists[1].percent, 75);
      assert.equal(resists[2].stateId, 3);
      assert.equal(resists[2].percent, 100);
    });

    it("应该处理零值", () => {
      const resists = createStateResist([0, 0], [1, 0], [2, 100]);
      assert.equal(resists[0].stateId, 0);
      assert.equal(resists[0].percent, 0);
      assert.equal(resists[2].percent, 100);
    });
  });

  describe("createPetCodeMessage", () => {
    it("应该创建精灵代码消息（不带套装信息）", () => {
      const testPet = create(PetInfoSchema, {
        id: 123,
        level: 100,
        abilityTotal: { hp: 100, attack: 50, defense: 30, specialAttack: 60, specialDefense: 40, speed: 20 },
        nature: 1,
        mintmarks: [createAbilityMintmark(1)],
        skills: [],
        effects: [],
        resistance: create(ResistanceInfoSchema, {
          hurt: { crit: 35, regular: 35, precent: 35 },
          ctl: createStateResist([1, 55], [2, 18], [3, 10]),
          weak: createStateResist([4, 10], [5, 10], [6, 10]),
        }),
      });

      const message = createPetCodeMessage(
        PetCodeMessage_Server.OFFICIAL,
        PetCodeMessage_DisplayMode.PVP,
        [testPet],
      );

      assert.equal(message.server, PetCodeMessage_Server.OFFICIAL);
      assert.equal(message.displayMode, PetCodeMessage_DisplayMode.PVP);
      assert.equal(message.pets.length, 1);
      assert.equal(message.pets[0]?.id, 123);
      assert.equal(message.pets[0]?.level, 100);
    });

    it("应该创建精灵代码消息（带套装信息）", () => {
      const testPet = create(PetInfoSchema, {
        id: 123,
        level: 100,
        abilityTotal: { hp: 100, attack: 50, defense: 30, specialAttack: 60, specialDefense: 40, speed: 20 },
        nature: 1,
        mintmarks: [createAbilityMintmark(1)],
        skills: [],
        effects: [],
        resistance: create(ResistanceInfoSchema, {
          hurt: { crit: 35, regular: 35, precent: 35 },
          ctl: createStateResist([1, 55], [2, 18], [3, 10]),
          weak: createStateResist([4, 10], [5, 10], [6, 10]),
        }),
      });

      const message = createPetCodeMessage(
        PetCodeMessage_Server.TAIWAN,
        PetCodeMessage_DisplayMode.PVE,
        [testPet],
        { equips: [100, 200, 300], titleId: 400 }
      );

      assert.equal(message.server, PetCodeMessage_Server.TAIWAN);
      assert.equal(message.displayMode, PetCodeMessage_DisplayMode.PVE);
      assert.equal(message.pets.length, 1);
      assert.equal(message.pets[0]?.id, 123);
      assert.equal(message.seerSet?.equips.length, 3);
      assert.equal(message.seerSet?.titleId, 400);
    });

    it("应该处理多个精灵", () => {
      const testPet1 = create(PetInfoSchema, {
        id: 123,
        level: 100,
        abilityTotal: { hp: 100, attack: 50, defense: 30, specialAttack: 60, specialDefense: 40, speed: 20 },
        nature: 1,
        mintmarks: [createAbilityMintmark(1)],
        skills: [],
        effects: [],
      });

      const testPet2 = create(PetInfoSchema, {
        id: 456,
        level: 100,
        abilityTotal: { hp: 100, attack: 50, defense: 30, specialAttack: 60, specialDefense: 40, speed: 20 },
        nature: 1,
        mintmarks: [createAbilityMintmark(1)],
        skills: [],
        effects: [],
      });
      const message = createPetCodeMessage(
        PetCodeMessage_Server.CLASSIC,
        PetCodeMessage_DisplayMode.PVP,
        [testPet1, testPet2],
        { equips: [100, 200, 300], titleId: 400 }
      );

      assert.equal(message.pets.length, 2);
      assert.equal(message.pets[0]?.id, 123);
      assert.equal(message.pets[1]?.id, 456);
    });
  });
});

