import { base64Decode, base64Encode } from '@bufbuild/protobuf/wire';
import {
  toBinary as schemaToBinary,
  fromBinary as schemaFromBinary,
  type MessageShape, type DescMessage, toJson as schemaToJson, fromJson as schemaFromJson,
  type MessageJsonType,
} from "@bufbuild/protobuf";
import { gzipSync, unzipSync } from 'node:zlib';

export function toBinary<T extends DescMessage>(schema: T, message: MessageShape<T>): Uint8Array {
  return gzipSync(schemaToBinary(schema, message), { level: 1 });
}

export function fromBinary<T extends DescMessage>(schema: T, binary: Uint8Array): MessageShape<T> {
  return schemaFromBinary(schema, unzipSync(binary));
}

export function toBase64<T extends DescMessage>(schema: T, message: MessageShape<T>): string {
  return base64Encode(toBinary(schema, message));
}

export function fromBase64<T extends DescMessage>(schema: T, base64: string): MessageShape<T> {
  return fromBinary(schema, base64Decode(base64));
}

export function toObject<T extends DescMessage>(schema: T, message: MessageShape<T>): MessageJsonType<T> {
  return schemaToJson(schema, message) as MessageJsonType<T>;
}

export function fromObject<T extends DescMessage>(schema: T, json: MessageJsonType<T>): MessageShape<T> {
  return schemaFromJson(schema, json) as MessageShape<T>;
}

export { createPetCodeMessage } from "./create_and_read.js";
