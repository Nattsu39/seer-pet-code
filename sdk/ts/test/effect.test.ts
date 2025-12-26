import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { EffectType, getEffectType, effectToParam, paramToEffect } from "../src/effect.js";
import { create } from "@bufbuild/protobuf";
import { PetInfo_EffectSchema } from "../src/generated/seerbp/petcode/v1/message_pb.js";

describe("effect", () => {
  describe("EffectType 枚举", () => {
    it("应该包含所有预期的特效类型", () => {
      assert.equal(EffectType.GENERAL, 1);
      assert.equal(EffectType.ITEM, 2);
      assert.equal(EffectType.VARIATION, 4);
      assert.equal(EffectType.SOULMARK, 5);
      assert.equal(EffectType.TEAM_TECH, 7);
      assert.equal(EffectType.OTHER, 99);
    });
  });

  describe("getEffectType", () => {
    it("应该返回 GENERAL 类型", () => {
      const type = getEffectType(1);
      assert.equal(type, EffectType.GENERAL);
    });

    it("应该返回 ITEM 类型", () => {
      const type = getEffectType(2);
      assert.equal(type, EffectType.ITEM);
    });

    it("应该返回 VARIATION 类型", () => {
      const type = getEffectType(4);
      assert.equal(type, EffectType.VARIATION);
    });

    it("应该返回 SOULMARK 类型", () => {
      const type = getEffectType(5);
      assert.equal(type, EffectType.SOULMARK);
    });

    it("应该返回 TEAM_TECH 类型", () => {
      const type = getEffectType(7);
      assert.equal(type, EffectType.TEAM_TECH);
    });

    it("应该对未知状态值返回 OTHER 类型", () => {
      assert.equal(getEffectType(0), EffectType.OTHER);
      assert.equal(getEffectType(3), EffectType.OTHER);
      assert.equal(getEffectType(6), EffectType.OTHER);
      assert.equal(getEffectType(100), EffectType.OTHER);
      assert.equal(getEffectType(-1), EffectType.OTHER);
    });
  });

  describe("effectToParam", () => {
    it("应该转换不带参数的特效", () => {
      const effect = create(PetInfo_EffectSchema, {
        id: 123,
        status: 1,
        args: [],
      });

      const param = effectToParam(effect);
      assert.equal(param.type, EffectType.GENERAL);
      assert.equal(param.name, "123");
    });

    it("应该转换带单个参数的特效", () => {
      const effect = create(PetInfo_EffectSchema, {
        id: 456,
        status: 2,
        args: [100],
      });

      const param = effectToParam(effect);
      assert.equal(param.type, EffectType.ITEM);
      assert.equal(param.name, "456_100");
    });

    it("应该转换带多个参数的特效", () => {
      const effect = create(PetInfo_EffectSchema, {
        id: 789,
        status: 4,
        args: [10, 20, 30],
      });

      const param = effectToParam(effect);
      assert.equal(param.type, EffectType.VARIATION);
      assert.equal(param.name, "789_10_20_30");
    });

    it("应该处理 SOULMARK 类型", () => {
      const effect = create(PetInfo_EffectSchema, {
        id: 111,
        status: 5,
        args: [50, 60],
      });

      const param = effectToParam(effect);
      assert.equal(param.type, EffectType.SOULMARK);
      assert.equal(param.name, "111_50_60");
    });

    it("应该处理 TEAM_TECH 类型", () => {
      const effect = create(PetInfo_EffectSchema, {
        id: 222,
        status: 7,
        args: [5],
      });

      const param = effectToParam(effect);
      assert.equal(param.type, EffectType.TEAM_TECH);
      assert.equal(param.name, "222_5");
    });

    it("应该处理未知类型", () => {
      const effect = create(PetInfo_EffectSchema, {
        id: 333,
        status: 99,
        args: [],
      });

      const param = effectToParam(effect);
      assert.equal(param.type, EffectType.OTHER);
      assert.equal(param.name, "333");
    });
  });

  describe("paramToEffect", () => {
    it("应该从参数创建不带 args 的特效", () => {
      const param = {
        type: EffectType.GENERAL,
        name: "123",
      };

      const effect = paramToEffect(param);
      assert.equal(effect.id, 123);
      assert.equal(effect.status, EffectType.GENERAL);
      assert.equal(effect.args.length, 0);
    });

    it("应该从参数创建带单个 arg 的特效", () => {
      const param = {
        type: EffectType.ITEM,
        name: "456_100",
      };

      const effect = paramToEffect(param);
      assert.equal(effect.id, 456);
      assert.equal(effect.status, EffectType.ITEM);
      assert.equal(effect.args.length, 1);
      assert.equal(effect.args[0], 100);
    });

    it("应该从参数创建带多个 args 的特效", () => {
      const param = {
        type: EffectType.VARIATION,
        name: "789_10_20_30",
      };

      const effect = paramToEffect(param);
      assert.equal(effect.id, 789);
      assert.equal(effect.status, EffectType.VARIATION);
      assert.equal(effect.args.length, 3);
      assert.equal(effect.args[0], 10);
      assert.equal(effect.args[1], 20);
      assert.equal(effect.args[2], 30);
    });

    it("应该处理 SOULMARK 类型", () => {
      const param = {
        type: EffectType.SOULMARK,
        name: "111_50_60",
      };

      const effect = paramToEffect(param);
      assert.equal(effect.id, 111);
      assert.equal(effect.status, EffectType.SOULMARK);
      assert.equal(effect.args.length, 2);
      assert.equal(effect.args[0], 50);
      assert.equal(effect.args[1], 60);
    });

    it("应该处理 TEAM_TECH 类型", () => {
      const param = {
        type: EffectType.TEAM_TECH,
        name: "222_5",
      };

      const effect = paramToEffect(param);
      assert.equal(effect.id, 222);
      assert.equal(effect.status, EffectType.TEAM_TECH);
      assert.equal(effect.args.length, 1);
      assert.equal(effect.args[0], 5);
    });

    it("应该在 name 格式无效时抛出错误", () => {
      const param = {
        type: EffectType.GENERAL,
        name: "",
      };

      assert.throws(() => {
        paramToEffect(param);
      }, /Invalid effect string/);
    });
  });

  describe("effectToParam 和 paramToEffect 往返转换", () => {
    it("应该支持不带参数的往返转换", () => {
      const original = create(PetInfo_EffectSchema, {
        id: 123,
        status: 1,
        args: [],
      });

      const param = effectToParam(original);
      const restored = paramToEffect(param);

      assert.equal(restored.id, original.id);
      assert.equal(restored.status, original.status);
      assert.equal(restored.args.length, original.args.length);
    });

    it("应该支持带参数的往返转换", () => {
      const original = create(PetInfo_EffectSchema, {
        id: 456,
        status: 2,
        args: [100, 200, 300],
      });

      const param = effectToParam(original);
      const restored = paramToEffect(param);

      assert.equal(restored.id, original.id);
      assert.equal(restored.status, original.status);
      assert.equal(restored.args.length, original.args.length);
      assert.equal(restored.args[0], original.args[0]);
      assert.equal(restored.args[1], original.args[1]);
      assert.equal(restored.args[2], original.args[2]);
    });

    it("应该支持所有特效类型的往返转换", () => {
      const types = [
        EffectType.GENERAL,
        EffectType.ITEM,
        EffectType.VARIATION,
        EffectType.SOULMARK,
        EffectType.TEAM_TECH,
        EffectType.OTHER,
      ];

      types.forEach((type, index) => {
        const original = create(PetInfo_EffectSchema, {
          id: 100 + index,
          status: type,
          args: [10, 20],
        });

        const param = effectToParam(original);
        const restored = paramToEffect(param);

        assert.equal(restored.id, original.id);
        assert.equal(restored.status, original.status);
        assert.equal(restored.args.length, original.args.length);
      });
    });
  });
});

