import { describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  toBinary,
  fromBinary,
  toBase64,
  fromBase64,
  toObject,
  fromObject,
} from "../src/index.js";
import { PetInfoSchema, PetCodeMessageSchema, PetCodeMessage_Server, PetCodeMessage_DisplayMode, ResistanceInfoSchema } from "../src/generated/seerbp/petcode/v1/message_pb.js";
import { create } from "@bufbuild/protobuf";
import { createAbilityMintmark, createStateResist } from "../src/create_and_read.js";

describe("index (序列化和反序列化)", () => {
  // 创建测试用的消息对象
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

  const testMessage = create(PetCodeMessageSchema, {
    server: PetCodeMessage_Server.OFFICIAL,
    displayMode: PetCodeMessage_DisplayMode.PVP,
    pets: [testPet],
    seerSet: {},
  });

  describe("toBinary 和 fromBinary", () => {
    it("应该将消息转换为二进制并能够还原", () => {
      const binary = toBinary(PetCodeMessageSchema, testMessage);
      assert.ok(binary instanceof Uint8Array);
      assert.ok(binary.length > 0);

      const restored = fromBinary(PetCodeMessageSchema, binary);
      assert.equal(restored.server, testMessage.server);
      assert.equal(restored.displayMode, testMessage.displayMode);
      assert.equal(restored.pets.length, 1);
      assert.equal(restored.pets[0]?.id, 123);
      assert.equal(restored.pets[0]?.level, 100);
    });

    it("应该处理空消息", () => {
      const emptyMessage = create(PetCodeMessageSchema, {
        server: PetCodeMessage_Server.OFFICIAL,
        displayMode: PetCodeMessage_DisplayMode.PVP,
        pets: [],
        seerSet: {},
      });

      const binary = toBinary(PetCodeMessageSchema, emptyMessage);
      const restored = fromBinary(PetCodeMessageSchema, binary);

      assert.equal(restored.server, emptyMessage.server);
      assert.equal(restored.pets.length, 0);
    });

    it("应该保留精灵的详细信息", () => {
      const binary = toBinary(PetInfoSchema, testPet);
      const restored = fromBinary(PetInfoSchema, binary);

      assert.equal(restored.id, testPet.id);
      assert.equal(restored.level, testPet.level);
      assert.equal(restored.nature, testPet.nature);
      assert.equal(restored.abilityTotal?.hp, testPet.abilityTotal?.hp);
      assert.equal(restored.abilityTotal?.attack, testPet.abilityTotal?.attack);
    });
  });

  describe("toBase64 和 fromBase64", () => {
    it("应该将消息转换为 Base64 字符串并能够还原", () => {
      const base64 = toBase64(PetCodeMessageSchema, testMessage);
      assert.equal(typeof base64, "string");
      assert.ok(base64.length > 0);

      const restored = fromBase64(PetCodeMessageSchema, base64);
      assert.equal(restored.server, testMessage.server);
      assert.equal(restored.displayMode, testMessage.displayMode);
      assert.equal(restored.pets.length, 1);
      assert.equal(restored.pets[0]?.id, 123);
    });

    it("应该生成有效的 Base64 字符串", () => {
      const base64 = toBase64(PetInfoSchema, testPet);
      // Base64 字符串应该只包含合法字符
      assert.match(base64, /^[A-Za-z0-9+/]*=*$/);
    });

    it("应该与二进制转换保持一致", () => {
      const binary = toBinary(PetInfoSchema, testPet);
      const base64 = toBase64(PetInfoSchema, testPet);
      const fromBase64Result = fromBase64(PetInfoSchema, base64);
      const fromBinaryResult = fromBinary(PetInfoSchema, binary);

      assert.equal(fromBase64Result.id, fromBinaryResult.id);
      assert.equal(fromBase64Result.level, fromBinaryResult.level);
      assert.equal(fromBase64Result.nature, fromBinaryResult.nature);
    });
  });

  describe("toObject 和 fromObject", () => {
    it("应该将消息转换为 JSON 对象并能够还原", () => {
      const json = toObject(PetCodeMessageSchema, testMessage);
      assert.equal(typeof json, "object");
      assert.equal(json.server, "SERVER_OFFICIAL");
      assert.equal(json.displayMode, "DISPLAY_MODE_PVP");
      assert.ok(Array.isArray(json.pets));

      const restored = fromObject(PetCodeMessageSchema, json);
      assert.equal(restored.server, testMessage.server);
      assert.equal(restored.displayMode, testMessage.displayMode);
      assert.equal(restored.pets.length, 1);
    });

    it("应该正确序列化和反序列化精灵信息", () => {
      const json = toObject(PetInfoSchema, testPet);
      assert.equal(json.id, 123);
      assert.equal(json.level, 100);
      assert.equal(json.nature, 1);
      assert.ok(json.abilityTotal);

      const restored = fromObject(PetInfoSchema, json);
      assert.equal(restored.id, testPet.id);
      assert.equal(restored.level, testPet.level);
      assert.equal(restored.nature, testPet.nature);
    });

    it("应该处理嵌套对象", () => {
      const json = toObject(PetInfoSchema, testPet);
      assert.equal(typeof json.abilityTotal, "object");

      const restored = fromObject(PetInfoSchema, json);
      assert.equal(restored.abilityTotal?.hp, testPet.abilityTotal?.hp);
      assert.equal(restored.abilityTotal?.attack, testPet.abilityTotal?.attack);
    });
  });

  describe("完整的往返转换", () => {
    it("应该支持 Object -> Binary -> Object 往返", () => {
      const json1 = toObject(PetInfoSchema, testPet);
      const message = fromObject(PetInfoSchema, json1);
      const json2 = toObject(PetInfoSchema, message);

      assert.equal(json1.id, json2.id);
      assert.equal(json1.level, json2.level);
      assert.equal(json1.nature, json2.nature);
    });

    it("应该支持复杂消息的完整往返", () => {
      // Object -> Message -> Base64 -> Message -> Object
      const originalJson = toObject(PetCodeMessageSchema, testMessage);
      const message1 = fromObject(PetCodeMessageSchema, originalJson);
      const base64 = toBase64(PetCodeMessageSchema, message1);
      const message2 = fromBase64(PetCodeMessageSchema, base64);
      const finalJson = toObject(PetCodeMessageSchema, message2);

      assert.equal(originalJson.server, finalJson.server);
      assert.equal(originalJson.displayMode, finalJson.displayMode);
      assert.equal(originalJson.pets?.length, finalJson.pets?.length);
    });
  });
});

