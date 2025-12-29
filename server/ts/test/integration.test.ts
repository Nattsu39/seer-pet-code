/**
 * 集成测试 - 测试完整的 HTTP 服务器
 * 这种方式最接近生产环境，但启动更慢
 */
import { test } from "node:test";
import assert from "node:assert";
import { fastify, type FastifyInstance } from "fastify";
import { fastifyConnectPlugin } from "@connectrpc/connect-fastify";
import { createConnectTransport } from "@connectrpc/connect-node";
import { Code, createClient } from "@connectrpc/connect";
import { PetCodeService } from "@seerbp/petcode-sdk/pb/server/v1/service_pb.js";
import routes from "../src/connect.js";
import {
  createTestPetCodeMessage,
  createTestPetCodeMessageWithMultiplePets,
  createEmptyPetCodeMessage,
} from "./helpers.js";

/**
 * 创建并启动测试服务器
 */
const createTestServer = async (): Promise<{
  server: FastifyInstance;
  baseUrl: string;
  close: () => Promise<void>;
}> => {
  const server = fastify();

  await server.register(fastifyConnectPlugin, {
    routes,
  });

  server.get("/", (_, reply) => {
    reply.type("text/plain");
    reply.send("Test Server");
  });

  // 使用随机端口避免冲突
  await server.listen({ host: "127.0.0.1", port: 0 });

  const address = server.addresses()[0];
  if (!address || typeof address === "string") {
    throw new Error("无法获取服务器地址");
  }

  const baseUrl = `http://${address.address}:${address.port}`;

  return {
    server,
    baseUrl,
    close: async () => {
      await server.close();
    },
  };
};

/**
 * 创建测试用的客户端
 */
const createTestClient = (baseUrl: string) => {
  const transport = createConnectTransport({
    baseUrl,
    httpVersion: "1.1",
  });

  return createClient(PetCodeService, transport);
};

test("集成测试 - 服务器应该正常启动", async () => {
  const { baseUrl, close } = await createTestServer();

  try {
    assert.ok(baseUrl, "应该返回服务器地址");
    assert.ok(baseUrl.startsWith("http://"), "地址应该是 HTTP URL");

    // 测试根路径
    const response = await fetch(baseUrl);
    const text = await response.text();
    assert.strictEqual(text, "Test Server", "根路径应该返回正确的文本");
  } finally {
    await close();
  }
});

test("集成测试 - encodePetCodeMessageToBase64 应该成功", async () => {
  const { baseUrl, close } = await createTestServer();

  try {
    const client = createTestClient(baseUrl);
    const message = createTestPetCodeMessage();

    const response = await client.encodePetCodeMessageToBase64({
      petCodeMessage: message,
    });

    assert.ok(response.base64, "应该返回 base64 字符串");
    assert.ok(typeof response.base64 === "string", "base64 应该是字符串");
    assert.ok(response.base64.length > 0, "base64 不应为空");
  } finally {
    await close();
  }
});

test("集成测试 - decodePetCodeMessageFromBase64 应该成功", async () => {
  const { baseUrl, close } = await createTestServer();

  try {
    const client = createTestClient(baseUrl);
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
  } finally {
    await close();
  }
});

test("集成测试 - 应该正确处理多个精灵", async () => {
  const { baseUrl, close } = await createTestServer();

  try {
    const client = createTestClient(baseUrl);
    const originalMessage = createTestPetCodeMessageWithMultiplePets(10);

    // 编码
    const encodeResponse = await client.encodePetCodeMessageToBase64({
      petCodeMessage: originalMessage,
    });

    // 解码
    const decodeResponse = await client.decodePetCodeMessageFromBase64({
      base64: encodeResponse.base64,
    });

    assert.strictEqual(
      decodeResponse.petCodeMessage?.pets.length,
      10,
      "应该解码出 10 个精灵"
    );

    // 验证精灵数据
    for (let i = 0; i < 10; i++) {
      const decodedPet = decodeResponse.petCodeMessage.pets[i];
      const originalPet = originalMessage.pets[i];
      assert.ok(decodedPet, `精灵 ${i} 应该存在`);
      assert.ok(originalPet, `原始精灵 ${i} 应该存在`);
      assert.strictEqual(
        decodedPet.id,
        originalPet.id,
        `精灵 ${i} 的 ID 应该匹配`
      );
    }
  } finally {
    await close();
  }
});

test("集成测试 - 应该正确处理空精灵列表", async () => {
  const { baseUrl, close } = await createTestServer();

  try {
    const client = createTestClient(baseUrl);
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
  } finally {
    await close();
  }
});

test("集成测试 - 缺少参数应该返回错误", async () => {
  const { baseUrl, close } = await createTestServer();

  try {
    const client = createTestClient(baseUrl);

    try {
      await client.encodePetCodeMessageToBase64({
        petCodeMessage: undefined,
      });
      assert.fail("应该抛出错误");
    } catch (error: any) {
      assert.strictEqual(error.code, Code.InvalidArgument, "错误码应该是 InvalidArgument");
    }
  } finally {
    await close();
  }
});

test("集成测试 - 无效的 base64 应该返回错误", async () => {
  const { baseUrl, close } = await createTestServer();

  try {
    const client = createTestClient(baseUrl);

    try {
      await client.decodePetCodeMessageFromBase64({
        base64: "invalid-base64",
      });
      assert.fail("应该抛出错误");
    } catch (error: any) {
      assert.strictEqual(error.code, Code.InvalidArgument, "错误码应该是 InvalidArgument");
    }
  } finally {
    await close();
  }
});

test("集成测试 - 并发请求应该正常工作", async () => {
  const { baseUrl, close } = await createTestServer();

  try {
    const client = createTestClient(baseUrl);

    // 创建多个不同的消息
    const messages = Array.from({ length: 5 }, (_, i) =>
      createTestPetCodeMessageWithMultiplePets(i + 1)
    );

    // 并发发送所有请求
    const promises = messages.map((message) =>
      client.encodePetCodeMessageToBase64({ petCodeMessage: message })
    );

    const responses = await Promise.all(promises);

    // 验证所有响应
    assert.strictEqual(responses.length, 5, "应该返回 5 个响应");

    for (const response of responses) {
      assert.ok(response.base64, "每个响应都应该有 base64");
      assert.ok(response.base64.length > 0, "base64 不应为空");
    }

    // 验证解码
    for (let i = 0; i < responses.length; i++) {
      const decodeResponse = await client.decodePetCodeMessageFromBase64({
        base64: responses[i]!.base64,
      });

      assert.strictEqual(
        decodeResponse.petCodeMessage?.pets.length,
        i + 1,
        `消息 ${i} 应该有 ${i + 1} 个精灵`
      );
    }
  } finally {
    await close();
  }
});

test("集成测试 - 完整的编码解码循环", async () => {
  const { baseUrl, close } = await createTestServer();

  try {
    const client = createTestClient(baseUrl);
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
  } finally {
    await close();
  }
});

