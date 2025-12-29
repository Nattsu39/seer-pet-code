/**
 * 测试辅助工具和数据生成器
 */
import { create } from "@bufbuild/protobuf";
import {
  PetCodeMessageSchema,
  PetCodeMessage_Server,
  PetCodeMessage_DisplayMode,
  type PetCodeMessage,
} from "@seerbp/petcode-sdk/pb/v1/message_pb.js";
import { PetInfoSchema, MintmarkInfoSchema, type PetInfo } from "@seerbp/petcode-sdk/pb/v1/message_pb.js";

/**
 * 创建测试用的精灵信息
 */
export const createTestPet = (overrides?: Partial<PetInfo>): PetInfo => {
  return create(PetInfoSchema, {
    id: 1,
    level: 100,
    skills: [1, 2, 3, 4],
    ...overrides,
  });
};

/**
 * 创建测试用的刻印信息
 */
export const createTestMintmark = (abilityId: number) => {
  return create(MintmarkInfoSchema, {
    mintmark: {
      case: "ability",
      value: { id: abilityId },
    },
  });
};

/**
 * 创建测试用的 PetCodeMessage
 */
export const createTestPetCodeMessage = (
  overrides?: Partial<PetCodeMessage>
): PetCodeMessage => {
  const defaultPet = createTestPet();

  return create(PetCodeMessageSchema, {
    server: PetCodeMessage_Server.OFFICIAL,
    displayMode: PetCodeMessage_DisplayMode.PVP,
    pets: [defaultPet],
    seerSet: {},
    ...overrides,
  });
};

/**
 * 创建包含多个精灵的测试消息
 */
export const createTestPetCodeMessageWithMultiplePets = (
  petCount: number
): PetCodeMessage => {
  const pets = Array.from({ length: petCount }, (_, i) =>
    createTestPet({ id: i + 1, level: 50 + i * 10 })
  );

  return create(PetCodeMessageSchema, {
    server: PetCodeMessage_Server.OFFICIAL,
    displayMode: PetCodeMessage_DisplayMode.PVP,
    pets,
    seerSet: {},
  });
};

/**
 * 创建空的 PetCodeMessage（用于测试边界情况）
 */
export const createEmptyPetCodeMessage = (): PetCodeMessage => {
  return create(PetCodeMessageSchema, {
    server: PetCodeMessage_Server.OFFICIAL,
    displayMode: PetCodeMessage_DisplayMode.PVP,
    pets: [],
    seerSet: {},
  });
};

