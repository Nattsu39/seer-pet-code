import { create } from "@bufbuild/protobuf";
import { PetInfo_EffectSchema, type PetInfo_Effect } from "./generated/seerbp/petcode/v1/message_pb.js";

/**
 * 特效类型枚举
 */
export const EffectType = {
  GENERAL: 1,
  ITEM: 2,
  VARIATION: 4,
  SOULMARK: 5,
  TEAM_TECH: 7,
  OTHER: 99,
} as const;

export type EffectType = typeof EffectType[keyof typeof EffectType];

/**
 * 根据 {@link PetInfo_Effect.status} 值获取特效类型，如果状态值不在枚举中，则返回 {@link EffectType.OTHER}
 *
 * @param status - {@link PetInfo_Effect.status} 值
 * @returns 特效类型
 */
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

/**
 * 特效参数化表示，用于方便后端数据源查询。
 */
export type EffectParam = {
  /**
   * 特效类型
   */
  type: EffectType;
  /**
   * 特效的字符串表示，格式为 `id_arg1_arg2_...`
   */
  name: string;
}

/**
 * 将 {@link PetInfo_Effect} 对象转换为 {@link EffectParam} 对象，
 *
 * 将 {@link PetInfo_Effect} 对象转换为 URL 友好的格式，方便在后端数据源中查询对应的特效。
 *
 * @param effect - {@link PetInfo_Effect} 对象
 * @return `EffectParam` 对象
 */
export function effectToParam(effect: PetInfo_Effect): EffectParam {
  return {
    type: getEffectType(effect.status),
    name: [effect.id, ...effect.args].join('_'),
  };
}

/**
 * 将 {@link EffectParam} 对象转换为 {@link PetInfo_Effect} 对象，
 *
 * @param param - {@link EffectParam} 对象
 * @return `PetInfo_Effect` 对象
 */
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
