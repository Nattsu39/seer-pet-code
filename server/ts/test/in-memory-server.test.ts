/**
 * 内存服务器测试 - 使用 createRouterTransport
 * 这是 ConnectRPC 推荐的测试方法，无需启动真实的 HTTP 服务器
 */
import { test } from "node:test";
import assert from "node:assert";
import { createRouterTransport } from "@connectrpc/connect";
import { Code, createClient } from "@connectrpc/connect";
import { PetCodeService } from "@seerbp/petcode-sdk/pb/server/v1/service_pb.js";
import routes from "../src/connect.js";
import {
  createTestPetCodeMessage,
  createTestPetCodeMessageWithMultiplePets,
  createEmptyPetCodeMessage,
} from "./helpers.js";

/**
 * 创建测试用的客户端
 */
const createTestClient = () => {
  // 创建内存传输层
  const transport = createRouterTransport(routes);

  // 创建客户端
  return createClient(PetCodeService, transport);
};

test("encodePetCodeMessageToBase64 - 应该成功编码消息", async () => {
  const client = createTestClient();
  const message = createTestPetCodeMessage();

  const response = await client.encodePetCodeMessageToBase64({
    petCodeMessage: message,
  });

  assert.ok(response, "应该返回响应");
  assert.ok(response.base64, "应该返回 base64 字符串");
  assert.ok(typeof response.base64 === "string", "base64 应该是字符串");
  assert.ok(response.base64.length > 0, "base64 不应为空");
});

test("encodePetCodeMessageToBase64 - 应该成功编码多个精灵", async () => {
  const client = createTestClient();
  const message = createTestPetCodeMessageWithMultiplePets(3);

  const response = await client.encodePetCodeMessageToBase64({
    petCodeMessage: message,
  });

  assert.ok(response.base64, "应该返回 base64 字符串");
  assert.ok(response.base64.length > 0, "base64 不应为空");
});

test("encodePetCodeMessageToBase64 - 应该成功编码空精灵列表", async () => {
  const client = createTestClient();
  const message = createEmptyPetCodeMessage();

  const response = await client.encodePetCodeMessageToBase64({
    petCodeMessage: message,
  });

  assert.ok(response.base64, "应该返回 base64 字符串");
});

test("encodePetCodeMessageToBase64 - 缺少 petCodeMessage 时应该抛出错误", async () => {
  const client = createTestClient();

  try {
    await client.encodePetCodeMessageToBase64({
      petCodeMessage: undefined,
    });
    assert.fail("应该抛出错误");
  } catch (error: any) {
    assert.strictEqual(error.code, Code.InvalidArgument, "错误码应该是 InvalidArgument");
    assert.ok(
      error.message.includes("petCodeMessage is required"),
      "错误消息应该包含 'petCodeMessage is required'"
    );
  }
});

test("decodePetCodeMessageFromBase64 - 应该成功解码有效的 base64", async () => {
  const client = createTestClient();
  const originalMessage = createTestPetCodeMessage();

  // 先编码
  const encodeResponse = await client.encodePetCodeMessageToBase64({
    petCodeMessage: originalMessage,
  });

  // 再解码
  const decodeResponse = await client.decodePetCodeMessageFromBase64({
    base64: encodeResponse.base64,
  });

  assert.ok(decodeResponse.petCodeMessage, "应该返回解码后的消息");
  assert.strictEqual(
    decodeResponse.petCodeMessage.server,
    originalMessage.server,
    "服务器类型应该匹配"
  );
  assert.strictEqual(
    decodeResponse.petCodeMessage.displayMode,
    originalMessage.displayMode,
    "显示模式应该匹配"
  );
  assert.strictEqual(
    decodeResponse.petCodeMessage.pets.length,
    originalMessage.pets.length,
    "精灵数量应该匹配"
  );
});

test("decodePetCodeMessageFromBase64 - 应该正确解码多个精灵", async () => {
  const client = createTestClient();
  const originalMessage = createTestPetCodeMessageWithMultiplePets(5);

  // 编码
  const encodeResponse = await client.encodePetCodeMessageToBase64({
    petCodeMessage: originalMessage,
  });

  // 解码
  const decodeResponse = await client.decodePetCodeMessageFromBase64({
    base64: encodeResponse.base64,
  });

  assert.ok(decodeResponse.petCodeMessage, "应该返回解码后的消息");
  assert.strictEqual(
    decodeResponse.petCodeMessage.pets.length,
    5,
    "应该解码出 5 个精灵"
  );

  // 验证每个精灵的数据
  for (let i = 0; i < 5; i++) {
    const decodedPet = decodeResponse.petCodeMessage.pets[i];
    const originalPet = originalMessage.pets[i];
    assert.ok(decodedPet, `精灵 ${i} 应该存在`);
    assert.ok(originalPet, `原始精灵 ${i} 应该存在`);
    assert.strictEqual(
      decodedPet.id,
      originalPet.id,
      `精灵 ${i} 的 ID 应该匹配`
    );
    assert.strictEqual(
      decodedPet.level,
      originalPet.level,
      `精灵 ${i} 的等级应该匹配`
    );
  }
});

test("decodePetCodeMessageFromBase64 - 缺少 base64 时应该抛出错误", async () => {
  const client = createTestClient();

  try {
    await client.decodePetCodeMessageFromBase64({
      base64: "",
    });
    assert.fail("应该抛出错误");
  } catch (error: any) {
    assert.strictEqual(error.code, Code.InvalidArgument, "错误码应该是 InvalidArgument");
    assert.ok(
      error.message.includes("base64 is required"),
      "错误消息应该包含 'base64 is required'"
    );
  }
});

test("decodePetCodeMessageFromBase64 - 无效的 base64 应该抛出错误", async () => {
  const client = createTestClient();

  try {
    await client.decodePetCodeMessageFromBase64({
      base64: "invalid-base64-string",
    });
    assert.fail("应该抛出错误");
  } catch (error: any) {
    assert.strictEqual(error.code, Code.InvalidArgument, "错误码应该是 InvalidArgument");
    assert.ok(
      error.message.includes("invalid base64"),
      "错误消息应该包含 'invalid base64'"
    );
  }
});

test("decodePetCodeMessageFromBase64 - 非 base64 字符串应该抛出错误", async () => {
  const client = createTestClient();

  try {
    await client.decodePetCodeMessageFromBase64({
      base64: "这不是有效的base64字符串!!!",
    });
    assert.fail("应该抛出错误");
  } catch (error: any) {
    assert.strictEqual(error.code, Code.InvalidArgument, "错误码应该是 InvalidArgument");
  }
});

test("完整流程 - 编码、解码、再编码应该保持一致", async () => {
  const client = createTestClient();
  const originalMessage = createTestPetCodeMessage();

  // 第一次编码
  const encode1 = await client.encodePetCodeMessageToBase64({
    petCodeMessage: originalMessage,
  });

  // 解码
  const decode = await client.decodePetCodeMessageFromBase64({
    base64: encode1.base64,
  });

  // 第二次编码
  const encode2 = await client.encodePetCodeMessageToBase64({
    petCodeMessage: decode.petCodeMessage,
  });

  // 两次编码的结果应该相同
  assert.strictEqual(
    encode1.base64,
    encode2.base64,
    "多次编码应该产生相同的结果"
  );
});

test("边界情况 - 空精灵列表的编码和解码", async () => {
  const client = createTestClient();
  const emptyMessage = createEmptyPetCodeMessage();

  // 编码
  const encodeResponse = await client.encodePetCodeMessageToBase64({
    petCodeMessage: emptyMessage,
  });

  // 解码
  const decodeResponse = await client.decodePetCodeMessageFromBase64({
    base64: encodeResponse.base64,
  });

  assert.strictEqual(
    decodeResponse.petCodeMessage?.pets.length,
    0,
    "精灵列表应该为空"
  );
  assert.strictEqual(
    decodeResponse.petCodeMessage.server,
    emptyMessage.server,
    "服务器类型应该匹配"
  );
});

