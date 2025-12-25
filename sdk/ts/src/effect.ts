import { create } from "@bufbuild/protobuf";
import { PetInfo_EffectSchema, type PetInfo_Effect } from "./generated/petcode/v1/message_pb.js";

export const EffectType = {
  GENERAL: 1,
  ITEM: 2,
  VARIATION: 4,
  SOULMARK: 5,
  TEAM_TECH: 7,
  OTHER: 99,
} as const;

export type EffectType = typeof EffectType[keyof typeof EffectType];

export function getEffectType(status: number): EffectType {
  switch (status) {
    case 1: return EffectType.GENERAL;
    case 2: return EffectType.ITEM;
    case 4: return EffectType.VARIATION;
    case 5: return EffectType.SOULMARK;
    case 7: return EffectType.TEAM_TECH;
    default: return EffectType.OTHER;
  }
}

type EffectParam = {
  type: EffectType;
  name: string;
}


export function effectToParam(effect: PetInfo_Effect): EffectParam {
  return {
    type: getEffectType(effect.status),
    name: [effect.id, ...effect.args].join('_'),
  };
}


export function paramToEffect(param: EffectParam): PetInfo_Effect {
  const [id, ...args] = param.name.split('_');
  if (!id || !param.type || !args) {
    throw new Error('Invalid effect string');
  }

  return create(PetInfo_EffectSchema, {
    id: parseInt(id),
    status: param.type,
    args: args.map(arg => parseInt(arg)),
  });
}
