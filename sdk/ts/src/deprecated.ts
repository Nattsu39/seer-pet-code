import { create } from "@bufbuild/protobuf";
import {
  PetAbilityBonus_Type,
  PetAbilityBonusSchema,
  type PetCodeMessage,
  type PetInfo,
} from "./generated/seerbp/petcode/v1/message_pb.js";

/**
 * 将 `pet.extraHp` 转换为一个全新的 {@link PetAbilityBonus_Type.BASEVALUE} 加成项
 */
function convertExtraHp(pet: PetInfo): void {
  if (pet.extraHp === 0) {
    return;
  }

  pet.abilityBonus.push(
    create(PetAbilityBonusSchema, {
      type: PetAbilityBonus_Type.BASEVALUE,
      value: { hp: { value: pet.extraHp } },
    }),
  );

  pet.extraHp = 0;
}

/**
 * 将消息中的弃用数据转换为新数据（原地修改并返回）。
 *
 * 目前会处理以下弃用字段：
 *
 * - `PetInfo.extra_hp`：转换为 `ability_bonus` 中一个全新的
 *   {@link PetAbilityBonus_Type.BASEVALUE} 类型的 `hp` 固定加成项，不会与已有加成项合并。
 *
 * @param message - 待转换的 `PetCodeMessage` 对象
 * @returns 转换后的同一个 `PetCodeMessage` 对象（便于链式调用）
 */
export function convertDeprecatedData(message: PetCodeMessage): PetCodeMessage {
  for (const pet of message.pets) {
    convertExtraHp(pet);
  }
  return message;
}
