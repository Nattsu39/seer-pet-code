import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { create } from "@bufbuild/protobuf";
import { convertDeprecatedData } from "../src/deprecated.js";
import {
  PetAbilityBonusSchema,
  PetAbilityBonus_Type,
  PetCodeMessage_DisplayMode,
  PetCodeMessage_Server,
  PetCodeMessageSchema,
  PetInfoSchema,
  type PetInfo,
} from "../src/generated/seerbp/petcode/v1/message_pb.js";

const createMessage = (...pets: PetInfo[]) =>
  create(PetCodeMessageSchema, {
    server: PetCodeMessage_Server.OFFICIAL,
    displayMode: PetCodeMessage_DisplayMode.PVP,
    pets,
  });

const findBaseValueBonus = (pet: PetInfo) =>
  pet.abilityBonus.find((bonus) => bonus.type === PetAbilityBonus_Type.BASEVALUE);

describe("convertDeprecatedData", () => {
  it("应该将 extraHp 转换为新的 TYPE_BASEVALUE 加成", () => {
    const pet = create(PetInfoSchema, { id: 1, extraHp: 20 });

    convertDeprecatedData(createMessage(pet));

    assert.equal(pet.extraHp, 0);
    assert.equal(pet.abilityBonus.length, 1);
    const bonus = pet.abilityBonus[0]!;
    assert.equal(bonus.type, PetAbilityBonus_Type.BASEVALUE);
    assert.equal(bonus.value?.hp?.value, 20);
    assert.equal(bonus.value?.hp?.percent, undefined);
  });

  it("即使已存在 TYPE_BASEVALUE 加成，也应新增一个全新加成项", () => {
    const pet = create(PetInfoSchema, {
      id: 1,
      extraHp: 20,
      abilityBonus: [
        create(PetAbilityBonusSchema, {
          type: PetAbilityBonus_Type.BASEVALUE,
          value: { hp: { value: 5, percent: 10 } },
        }),
      ],
    });

    convertDeprecatedData(createMessage(pet));

    assert.equal(pet.extraHp, 0);
    assert.equal(pet.abilityBonus.length, 2);
    assert.equal(pet.abilityBonus[0]!.value?.hp?.value, 5);
    assert.equal(pet.abilityBonus[0]!.value?.hp?.percent, 10);
    const created = pet.abilityBonus[1]!;
    assert.equal(created.type, PetAbilityBonus_Type.BASEVALUE);
    assert.equal(created.value?.hp?.value, 20);
    assert.equal(created.value?.hp?.percent, undefined);
  });

  it("extraHp 为 0 时不应产生任何改动", () => {
    const pet = create(PetInfoSchema, { id: 1 });

    convertDeprecatedData(createMessage(pet));

    assert.equal(pet.extraHp, 0);
    assert.equal(pet.abilityBonus.length, 0);
  });

  it("不应该影响其他类型的加成项", () => {
    const pet = create(PetInfoSchema, {
      id: 1,
      extraHp: 20,
      abilityBonus: [
        create(PetAbilityBonusSchema, { type: PetAbilityBonus_Type.TEAM_TECH }),
      ],
    });

    convertDeprecatedData(createMessage(pet));

    assert.equal(pet.abilityBonus.length, 2);
    assert.equal(pet.abilityBonus[0]!.type, PetAbilityBonus_Type.TEAM_TECH);
    const created = pet.abilityBonus[1]!;
    assert.equal(created.type, PetAbilityBonus_Type.BASEVALUE);
    assert.equal(created.value?.hp?.value, 20);
  });

  it("应该转换消息中的所有精灵", () => {
    const pets = [1, 2, 3].map((i) =>
      create(PetInfoSchema, { id: i, extraHp: 10 * i }),
    );

    convertDeprecatedData(createMessage(...pets));

    pets.forEach((pet, index) => {
      assert.equal(pet.extraHp, 0);
      assert.equal(findBaseValueBonus(pet)?.value?.hp?.value, 10 * (index + 1));
    });
  });

  it("应该原地修改并返回同一个消息对象", () => {
    const message = createMessage(create(PetInfoSchema, { id: 1, extraHp: 1 }));

    assert.equal(convertDeprecatedData(message), message);
  });
});
