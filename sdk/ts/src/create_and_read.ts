import { create } from "@bufbuild/protobuf";
import type { OmitTypeName } from "./omit-type-name.js";
import { MintmarkInfo_Universal_GemItemSchema, MintmarkInfoSchema, PetAbilityValueSchema, PetCodeMessage_DisplayMode, PetCodeMessage_Server, PetCodeMessageSchema, PetInfoSchema, ResistanceInfo_StateItemSchema, type MintmarkInfo, type MintmarkInfo_Ability, type MintmarkInfo_Quanxiao, type MintmarkInfo_Skill, type MintmarkInfo_Universal, type PetAbilityValueJson, type PetCodeMessage, type PetCodeMessage_SeerSetJson, type PetInfo, type ResistanceInfo_StateItem } from "./generated/seerbp/petcode/v1/message_pb.js";

/**
 * 创建能力刻印
 * @param id - 能力刻印 ID
 * @returns `MintmarkInfo` 对象
 */
export function createAbilityMintmark(id: number): MintmarkInfo {
  return create(MintmarkInfoSchema, { mintmark: { value: { id }, case: "ability" } });
}

/**
 * 创建技能刻印
 * @param id - 技能刻印 ID
 * @returns `MintmarkInfo` 对象
 */
export function createSkillMintmark(id: number): MintmarkInfo {
  return create(MintmarkInfoSchema, { mintmark: { value: { id }, case: "skill" } });
}

/**
 * 创建全效刻印
 * @param id - 能力刻印 ID
 * @param skillMintmarkId - 技能刻印 ID
 * @returns `MintmarkInfo` 对象
 */
export function createQuanxiaoMintmark(id: number, skillMintmarkId: number): MintmarkInfo {
  return create(MintmarkInfoSchema, { mintmark: { value: { id, skillMintmarkId }, case: "quanxiao" } });
}

type GemOption = { id: number, bindSkillId: number }
/**
 * 创建全能刻印
 * @param id - 全能刻印 ID
 * @param level - 全能刻印等级
 * @param options - 额外选项
 * @returns `MintmarkInfo` 对象
 */
export function createUniversalMintmark(
  id: number,
  level: number,
  options: { ability?: PetAbilityValueJson, gem?: GemOption }
): MintmarkInfo {
  const { ability, gem } = options;
  const gemMessage = gem
    ? create(MintmarkInfo_Universal_GemItemSchema, { gemId: gem.id, bindSkillId: gem.bindSkillId })
    : {};
  const abilityMessage = ability
    ? create(PetAbilityValueSchema, ability)
    : {};
  return create(MintmarkInfoSchema,
    { mintmark: { value: { id, level, gem: gemMessage, ability: abilityMessage }, case: "universal" } });
}

type MintmarkUnion = MintmarkInfo_Skill
  | MintmarkInfo_Ability
  | MintmarkInfo_Universal
  | MintmarkInfo_Quanxiao;

/**
 * 读取刻印的具体类型
 * @param mintmark - `MintmarkInfo` 对象
 * @returns 具体的刻印对象（`MintmarkInfo_Skill` / `MintmarkInfo_Ability` / `MintmarkInfo_Universal` / `MintmarkInfo_Quanxiao`）
 */
export function readMintmark(mintmark: MintmarkInfo): MintmarkUnion {
  const value = mintmark.mintmark.value;
  if (value === undefined) {
    throw new Error("Mintmark is undefined");
  }

  return mintmark.mintmark.value;
}

type StateResistTuple = [ResistanceInfo_StateItem, ResistanceInfo_StateItem, ResistanceInfo_StateItem];
/**
 * 创建异常抗性列表，参数元组中位置1为异常状态ID，位置2为抗性百分比
 * @returns 状态抗性列表
 */
export function createStateResist(
  args1: [number, number],
  args2: [number, number],
  args3: [number, number],
): StateResistTuple {
  return [
    create(ResistanceInfo_StateItemSchema, { stateId: args1[0], percent: args1[1] }),
    create(ResistanceInfo_StateItemSchema, { stateId: args2[0], percent: args2[1] }),
    create(ResistanceInfo_StateItemSchema, { stateId: args3[0], percent: args3[1] }),
  ];
}

/**
 * 创建精灵代码消息对象
 * @param server - 服务器类型
 * @param displayMode - 显示模式
 * @param pets - 精灵列表
 * @param seerSet - 套装和称号信息
 * @returns `PetCodeMessage` 对象
 */
export function createPetCodeMessage(
  server: PetCodeMessage_Server,
  displayMode: PetCodeMessage_DisplayMode,
  pets: OmitTypeName<PetInfo>[],
  seerSet: PetCodeMessage_SeerSetJson = {},
): PetCodeMessage {
  const petMessages = pets.map(pet => create(PetInfoSchema, pet as any));
  return create(PetCodeMessageSchema, { server, displayMode, seerSet, pets: petMessages });
}
