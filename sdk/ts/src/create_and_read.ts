import { create } from "@bufbuild/protobuf";
import type { OmitTypeName } from "./omit-type-name.js";
import { MintmarkInfo_Universal_GemItemSchema, MintmarkInfoSchema, PetAbilityValueSchema, PetCodeMessage_DisplayMode, PetCodeMessage_Server, PetCodeMessageSchema, PetInfoSchema, ResistanceInfo_StateItemSchema, type MintmarkInfo, type MintmarkInfo_Ability, type MintmarkInfo_Quanxiao, type MintmarkInfo_Skill, type MintmarkInfo_Universal, type PetAbilityValueJson, type PetCodeMessage, type PetCodeMessage_SeerSetJson, type PetInfo, type ResistanceInfo_StateItem } from "./generated/petcode/v1/message_pb.js";

export function createAbilityMintmark(id: number): MintmarkInfo {
  return create(MintmarkInfoSchema, { mintmark: { value: { id }, case: "ability" } });
}

export function createSkillMintmark(id: number): MintmarkInfo {
  return create(MintmarkInfoSchema, { mintmark: { value: { id }, case: "skill" } });
}

export function createQuanxiaoMintmark(id: number, skillMintmarkId: number): MintmarkInfo {
  return create(MintmarkInfoSchema, { mintmark: { value: { id, skillMintmarkId }, case: "quanxiao" } });
}

type GemOption = { id: number, bindSkillId: number }
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

export function readMintmark(mintmark: MintmarkInfo): MintmarkUnion {
  const value = mintmark.mintmark.value;
  if (value === undefined) {
    throw new Error("Mintmark is undefined");
  }

  return mintmark.mintmark.value;
}

type StateResistTuple = [ResistanceInfo_StateItem, ResistanceInfo_StateItem, ResistanceInfo_StateItem];
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

export function createPetCodeMessage(
  server: PetCodeMessage_Server,
  displayMode: PetCodeMessage_DisplayMode,
  pets: OmitTypeName<PetInfo>[],
  seerSet: PetCodeMessage_SeerSetJson = {},
): PetCodeMessage {
  const petMessages = pets.map(pet => create(PetInfoSchema, pet as any));
  return create(PetCodeMessageSchema, { server, displayMode, seerSet, pets: petMessages });
}
