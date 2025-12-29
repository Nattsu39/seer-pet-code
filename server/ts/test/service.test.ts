/**
 * 服务单元测试 - 直接测试服务方法
 */
import { test } from "node:test";
import assert from "node:assert";
import { Code, ConnectError } from "@connectrpc/connect";
import { toBase64, fromBase64 } from "@seerbp/petcode-sdk";
import { PetCodeMessageSchema } from "@seerbp/petcode-sdk/pb/v1/message_pb.js";
import {
  createTestPetCodeMessage,
  createTestPetCodeMessageWithMultiplePets,
  createEmptyPetCodeMessage,
} from "./helpers.js";

/**
 * 模拟 encodePetCodeMessageToBase64 服务方法
 */
const encodePetCodeMessageToBase64 = async (
  petCodeMessage: any
): Promise<string> => {
  if (!petCodeMessage) {
    throw new ConnectError("petCodeMessage is required", Code.InvalidArgument);
  }
  try {
    return toBase64(PetCodeMessageSchema, petCodeMessage);
  } catch (error) {
    throw new ConnectError("invalid petCodeMessage", Code.InvalidArgument);
  }
};

/**
 * 模拟 decodePetCodeMessageFromBase64 服务方法
 */
const decodePetCodeMessageFromBase64 = async (base64: string) => {
  if (!base64) {
    throw new ConnectError("base64 is required", Code.InvalidArgument);
  }
  try {
    return fromBase64(PetCodeMessageSchema, base64);
  } catch (error) {
    throw new ConnectError("invalid base64", Code.InvalidArgument);
  }
};

test("encodePetCodeMessageToBase64 - 应该成功编码单个精灵消息", async () => {
  const message = createTestPetCodeMessage();
  const base64 = await encodePetCodeMessageToBase64(message);

  assert.ok(base64, "应该返回 base64 字符串");
  assert.ok(typeof base64 === "string", "返回值应该是字符串");
  assert.ok(base64.length > 0, "base64 字符串不应为空");
});

test("encodePetCodeMessageToBase64 - 应该成功编码多个精灵消息", async () => {
  const message = createTestPetCodeMessageWithMultiplePets(3);
  const base64 = await encodePetCodeMessageToBase64(message);

  assert.ok(base64, "应该返回 base64 字符串");
  assert.ok(typeof base64 === "string", "返回值应该是字符串");
});

test("encodePetCodeMessageToBase64 - 应该成功编码空精灵列表", async () => {
  const message = createEmptyPetCodeMessage();
  const base64 = await encodePetCodeMessageToBase64(message);

  assert.ok(base64, "应该返回 base64 字符串");
  assert.ok(typeof base64 === "string", "返回值应该是字符串");
});

test("encodePetCodeMessageToBase64 - 消息为空时应该抛出错误", async () => {
  await assert.rejects(
    async () => {
      await encodePetCodeMessageToBase64(null);
    },
    (error: any) => {
      assert.strictEqual(error.rawMessage, "petCodeMessage is required");
      assert.strictEqual(error.code, Code.InvalidArgument);
      return true;
    },
    "应该抛出 InvalidArgument 错误"
  );
});

test("encodePetCodeMessageToBase64 - 消息为 undefined 时应该抛出错误", async () => {
  await assert.rejects(
    async () => {
      await encodePetCodeMessageToBase64(undefined);
    },
    (error: any) => {
      assert.strictEqual(error.rawMessage, "petCodeMessage is required");
      assert.strictEqual(error.code, Code.InvalidArgument);
      return true;
    },
    "应该抛出 InvalidArgument 错误"
  );
});

test("decodePetCodeMessageFromBase64 - 应该成功解码有效的 base64", async () => {
  const originalMessage = createTestPetCodeMessage();
  const base64 = toBase64(PetCodeMessageSchema, originalMessage);

  const decoded = await decodePetCodeMessageFromBase64(base64);

  assert.ok(decoded, "应该返回解码后的消息");
  assert.strictEqual(
    decoded.server,
    originalMessage.server,
    "服务器类型应该匹配"
  );
  assert.strictEqual(
    decoded.displayMode,
    originalMessage.displayMode,
    "显示模式应该匹配"
  );
  assert.strictEqual(
    decoded.pets.length,
    originalMessage.pets.length,
    "精灵数量应该匹配"
  );
});

test("decodePetCodeMessageFromBase64 - 应该成功解码多个精灵", async () => {
  const originalMessage = createTestPetCodeMessageWithMultiplePets(5);
  const base64 = toBase64(PetCodeMessageSchema, originalMessage);

  const decoded = await decodePetCodeMessageFromBase64(base64);

  assert.strictEqual(decoded.pets.length, 5, "应该解码出 5 个精灵");

  // 验证每个精灵的数据
  for (let i = 0; i < decoded.pets.length; i++) {
    const decodedPet = decoded.pets[i];
    const originalPet = originalMessage.pets[i];
    assert.ok(decodedPet, `精灵 ${i} 应该存在`);
    assert.ok(originalPet, `原始精灵 ${i} 应该存在`);
    assert.strictEqual(
      decodedPet.id,
      originalPet.id,
      `精灵 ${i} 的 ID 应该匹配`
    );
  }
});

test("decodePetCodeMessageFromBase64 - base64 为空时应该抛出错误", async () => {
  await assert.rejects(
    async () => {
      await decodePetCodeMessageFromBase64("");
    },
    (error: any) => {
      assert.strictEqual(error.rawMessage, "base64 is required");
      assert.strictEqual(error.code, Code.InvalidArgument);
      return true;
    },
    "应该抛出 InvalidArgument 错误"
  );
});

test("decodePetCodeMessageFromBase64 - base64 无效时应该抛出错误", async () => {
  await assert.rejects(
    async () => {
      await decodePetCodeMessageFromBase64("invalid-base64");
    },
    (error: any) => {
      assert.strictEqual(error.rawMessage, "invalid base64");
      assert.strictEqual(error.code, Code.InvalidArgument);
      return true;
    },
    "应该抛出 InvalidArgument 错误"
  );
});

test("decodePetCodeMessageFromBase64 - 非 base64 字符串应该抛出错误", async () => {
  await assert.rejects(
    async () => {
      await decodePetCodeMessageFromBase64("这不是base64!!!");
    },
    (error: any) => {
      assert.strictEqual(error.rawMessage, "invalid base64");
      assert.strictEqual(error.code, Code.InvalidArgument);
      return true;
    },
    "应该抛出 InvalidArgument 错误"
  );
});

test("编码和解码循环 - 数据应该保持一致", async () => {
  const originalMessage = createTestPetCodeMessage();

  // 编码
  const base64 = await encodePetCodeMessageToBase64(originalMessage);

  // 解码
  const decoded = await decodePetCodeMessageFromBase64(base64);

  // 再次编码
  const base64Again = await encodePetCodeMessageToBase64(decoded);

  // 两次编码的结果应该相同
  assert.strictEqual(
    base64,
    base64Again,
    "多次编码应该产生相同的结果"
  );
});

