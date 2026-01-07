import { base64Decode, base64Encode } from '@bufbuild/protobuf/wire';
import {
  toBinary as schemaToBinary,
  fromBinary as schemaFromBinary,
  type MessageShape, type DescMessage, toJson as schemaToJson, fromJson as schemaFromJson,
  type MessageJsonType,
} from "@bufbuild/protobuf";
import { gzip, ungzip } from "pako";

function compressWithGzip(binary: Uint8Array) {
  return gzip(binary, { level: 1 });
}

function decompressWithGzip(binary: Uint8Array) {
  return ungzip(binary);
}

/**
 * 将消息对象转换为二进制数据
 * @param schema - 消息模式
 * @param message - 消息对象
 * @returns 二进制数据
 */
export function toBinary<T extends DescMessage>(schema: T, message: MessageShape<T>): Uint8Array {
  return compressWithGzip(schemaToBinary(schema, message));
}

/**
 * 将二进制数据转换为消息对象
 * @param schema - 消息模式
 * @param binary - 二进制数据
 * @returns 消息对象
 */
export function fromBinary<T extends DescMessage>(schema: T, binary: Uint8Array): MessageShape<T> {
  return schemaFromBinary(schema, decompressWithGzip(binary));
}

/**
 * 将消息对象转换为 Base64 字符串
 * @param schema - 消息模式
 * @param message - 消息对象
 * @returns Base64 字符串
 */
export function toBase64<T extends DescMessage>(schema: T, message: MessageShape<T>): string {
  return base64Encode(toBinary(schema, message));
}

/**
 * 将 Base64 字符串转换为消息对象
 * @param schema - 消息模式
 * @param base64 - Base64 字符串
 * @returns 消息对象
 */
export function fromBase64<T extends DescMessage>(schema: T, base64: string): MessageShape<T> {
  return fromBinary(schema, base64Decode(base64));
}

/**
 * 将消息对象转换为 JSON 对象
 * @param schema - 消息模式
 * @param message - 消息对象
 * @returns JSON 对象
 */
export function toObject<T extends DescMessage>(schema: T, message: MessageShape<T>): MessageJsonType<T> {
  return schemaToJson(schema, message) as MessageJsonType<T>;
}

/**
 * 将 JSON 对象转换为消息对象
 * @param schema - 消息模式
 * @param json - JSON 对象
 * @returns 消息对象
 */
export function fromObject<T extends DescMessage>(schema: T, json: MessageJsonType<T>): MessageShape<T> {
  return schemaFromJson(schema, json) as MessageShape<T>;
}

export { createPetCodeMessage } from "./create_and_read.js";
