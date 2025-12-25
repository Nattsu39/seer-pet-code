# PetCode Python SDK - API 参考

本文档提供 PetCode Python SDK 的 API 参考。完整的使用手册请参考 [docs/manual.md](../../docs/manual.md)。

## 目录

- [序列化函数](#序列化函数)
- [辅助创建函数](#辅助创建函数)
- [效果处理函数](#效果处理函数)
- [枚举值速查表](#枚举值速查表)

---

## 序列化函数

所有序列化函数都位于 `petcode` 模块。

### `to_base64(message: PetCodeMessage) -> str`

将消息序列化为 URL 安全的 Base64 字符串（内部已 Gzip 压缩）。

**参数**：

- `message`: 要序列化的 `PetCodeMessage` 对象

**返回**：Base64 字符串

**用途**：生成分享码、二维码内容

**示例**：

```python
code = to_base64(message)
print(code)  # H4sIAAAAAAAC/2WOQQ6AIAxE7/IXa...
```

### `from_base64(data: str) -> PetCodeMessage`

将 Base64 字符串还原为消息（内部自动解压）。

**参数**：

- `data`: Base64 字符串

**返回**：`PetCodeMessage` 对象

**异常**：

- `DecodeError`: 数据格式错误
- `ValueError`: Base64 解码失败

**示例**：

```python
message = from_base64("H4sIAAAAAAAC/2WOQQ6AIAxE7/IXa...")
```

### `to_binary(message: PetCodeMessage) -> bytes`

将消息序列化为二进制数据（内部已 Gzip 压缩）。

**参数**：

- `message`: 要序列化的 `PetCodeMessage` 对象

**返回**：字节数据

**用途**：存入数据库、文件存储、网络传输

**示例**：

```python
binary = to_binary(message)
with open('pet_config.bin', 'wb') as f:
    f.write(binary)
```

### `from_binary(data: bytes) -> PetCodeMessage`

将二进制数据还原为消息（内部自动解压）。

**参数**：

- `data`: 字节数据

**返回**：`PetCodeMessage` 对象

**示例**：

```python
with open('pet_config.bin', 'rb') as f:
    binary = f.read()
message = from_binary(binary)
```

### `to_dict(message: PetCodeMessage) -> dict`

将消息转换为字典（JSON 格式）。

**参数**：

- `message`: 要转换的 `PetCodeMessage` 对象

**返回**：字典对象

**用途**：调试输出、JSON API 交互

**示例**：

```python
data = to_dict(message)
import json
print(json.dumps(data, indent=2, ensure_ascii=False))
```

### `from_dict(data: dict) -> PetCodeMessage`

将字典还原为消息。

**参数**：

- `data`: 字典对象

**返回**：`PetCodeMessage` 对象

**示例**：

```python
data = {'server': 'SERVER_OFFICIAL', 'displayMode': 'DISPLAY_MODE_PVP', 'pets': [...]}
message = from_dict(data)
```

---

## 辅助创建函数

辅助创建函数位于 `petcode.create_and_read` 模块。

### `create_skill_mintmark(id: int) -> MintmarkInfo`

创建技能刻印。

**参数**：

- `id`: 技能刻印 ID

**返回**：`MintmarkInfo` 对象

**示例**：

```python
mintmark = create_skill_mintmark(id=50001)
```

### `create_ability_mintmark(id: int) -> MintmarkInfo`

创建能力刻印。

**参数**：

- `id`: 能力刻印 ID

**返回**：`MintmarkInfo` 对象

**示例**：

```python
mintmark = create_ability_mintmark(id=60001)
```

### `create_universal_mintmark(id: int, level: int, *, gem_id: int = None, bind_skill_id: int = None, ability: PetAbilityValue = None) -> MintmarkInfo`

创建全能刻印。

**参数**：

- `id`: 刻印 ID
- `level`: 刻印等级（1-5）
- `gem_id`: 可选，宝石 ID（需要同时提供 `bind_skill_id`）
- `bind_skill_id`: 可选，宝石绑定的技能 ID（需要同时提供 `gem_id`）
- `ability`: 可选，自定义能力值（用于旧版随机刻印）

**返回**：`MintmarkInfo` 对象

**示例**：

```python
# 无宝石
mm1 = create_universal_mintmark(id=40001, level=5)

# 带宝石
mm2 = create_universal_mintmark(id=40001, level=5, gem_id=1800011, bind_skill_id=24708)

# 自定义能力值
mm3 = create_universal_mintmark(
    id=40001, 
    level=5, 
    ability=PetAbilityValue(hp=100, attack=120, defense=80, special_attack=90, special_defense=85, speed=110)
)
```

### `create_quanxiao_mintmark(id: int, *, skill_mintmark_id: int) -> MintmarkInfo`

创建全效刻印。

**参数**：

- `id`: 能力刻印 ID
- `skill_mintmark_id`: 技能刻印 ID

**返回**：`MintmarkInfo` 对象

**示例**：

```python
mintmark = create_quanxiao_mintmark(id=70001, skill_mintmark_id=50001)
```

### `read_mintmark(mintmark: MintmarkInfo) -> MintmarkInfo.Skill | MintmarkInfo.Ability | MintmarkInfo.Universal | MintmarkInfo.Quanxiao`

读取刻印的具体类型。

**参数**：

- `mintmark`: `MintmarkInfo` 对象

**返回**：具体的刻印对象（Skill / Ability / Universal / Quanxiao）

**异常**：

- `ValueError`: 未知的刻印类型

**示例**：

```python
data = read_mintmark(mintmark)
if isinstance(data, MintmarkInfo.Universal):
    print(f"全能刻印: {data.id}")
```

### `create_state_resist(args1: tuple[int, int], args2: tuple[int, int], args3: tuple[int, int]) -> tuple[ResistanceInfo.StateItem, ...]`

创建状态抗性列表。

**参数**：

- `args1`, `args2`, `args3`: 元组 `(state_id, percent)`，表示状态 ID 和抗性百分比

**返回**：包含 3 个 `ResistanceInfo.StateItem` 的元组

**示例**：

```python
ctl_resist = create_state_resist((1, 55), (2, 18), (3, 10))
resistance = ResistanceInfo(
    hurt=ResistanceInfo.Hurt(crit=35, regular=35, precent=35),
    ctl=ctl_resist
)
```

---

## 效果处理函数

效果处理函数位于 `petcode.effect` 模块。

### `get_effect_type(status: int) -> EffectType`

根据 status 值获取效果类型。

**参数**：

- `status`: 效果的 status 字段值

**返回**：`EffectType` 枚举值

**示例**：

```python
effect_type = get_effect_type(1)
if effect_type == EffectType.GENERAL:
    print("这是特性")
```

### `effect_to_param(effect: PetInfo.Effect) -> EffectParam`

将 PetInfo.Effect 对象转换为 EffectParam，用于生成 API 请求参数。

**参数**：

- `effect`: PetInfo.Effect 对象

**返回**：`EffectParam` 对象，包含特效类型和字符串表示

**示例**：

```python
from petcode.effect import effect_to_param

effect = PetInfo.Effect(id=67, status=1, args=[1, 5])
param = effect_to_param(effect)
print(param.type)  # EffectType.GENERAL
print(param.name)  # "67_1_5"
```

### `param_to_effect(param: EffectParam) -> PetInfo.Effect`

将 EffectParam 转换回 PetInfo.Effect 对象。

**参数**：

- `param`: EffectParam 对象

**返回**：`PetInfo.Effect` 对象

**示例**：

```python
from petcode.effect import param_to_effect, EffectParam, EffectType

param = EffectParam(type=EffectType.GENERAL, name="67_1_5")
effect = param_to_effect(param)
print(effect.id)      # 67
print(effect.status)  # 1
print(effect.args)    # [1, 5]
```

### `EffectParam` 类

特效的参数化表示，用于生成 SeerAPI 请求 URL。

**属性**：

- `type`: 特效类型（EffectType 枚举）
- `name`: 特效的字符串表示，格式为 "id_arg1_arg2_..."

### `EffectType` 枚举

| 枚举值 | 数值 | 说明 |
| -------- | ------ | ------ |
| `NONE` | 0 | 无效果 |
| `GENERAL` | 1 | 特性 |
| `ITEM` | 2 | 道具效果 |
| `VARIATION` | 4 | 异能特质 |
| `SOULMARK` | 5 | 魂印 |
| `TEAM_TECH` | 7 | 战队科技 |
| `OTHER` | 99 | 其他 |

---

## 枚举值速查表

### Server（服务器）

| 枚举名 | 数值 | 说明 |
| -------- | ------ | ------ |
| `SERVER_UNSPECIFIED` | 0 | 未指定 |
| `SERVER_OFFICIAL` | 1 | 官方服 |
| `SERVER_TEST` | 2 | 测试服 |
| `SERVER_TAIWAN` | 3 | 台服 |
| `SERVER_CLASSIC` | 4 | 经典服 |

### DisplayMode（展示模式）

| 枚举名 | 数值 | 说明 |
| ------ | ------ | ------ |
| `DISPLAY_MODE_UNSPECIFIED` | 0 | 未指定 |
| `DISPLAY_MODE_PVP` | 1 | PVP 模式 |
| `DISPLAY_MODE_PVE` | 2 | PVE 模式 |
| `DISPLAY_MODE_BOSS` | 3 | BOSS 模式 |

### PetAbilityBonus.Type（能力加成类型）

| 枚举名 | 数值 | 说明 |
| ------ | ------ | ------ |
| `TYPE_UNSPECIFIED` | 0 | 未指定 |
| `TYPE_TEAM_TECH` | 1 | 战队加成 |
| `TYPE_ANNUAL_VIP` | 2 | 年费加成 |
| `TYPE_SUPER_NONO` | 3 | 超能 NoNo 加成 |
| `TYPE_SOULMARK` | 4 | 魂印加成 |
| `TYPE_AWAKEN` | 5 | 神谕觉醒加成 |
| `TYPE_SPECIAL` | 6 | 特殊加成 |
| `TYPE_OTHER` | 99 | 其他加成 |

### EffectType（效果类型）

| 枚举名 | 数值 | 说明 |
| ------ | ------ | ------ |
| `NONE` | 0 | 无效果 |
| `GENERAL` | 1 | 特性 |
| `ITEM` | 2 | 道具效果（应使用 pet_items 字段） |
| `VARIATION` | 4 | 异能特质 |
| `SOULMARK` | 5 | 魂印 |
| `TEAM_TECH` | 7 | 战队科技（应使用 ability_bonus 字段） |
| `OTHER` | 99 | 其他 |

---

## 更多信息

完整的使用指南、数据结构详解、最佳实践等内容请参考：[PetCode 使用手册](../../docs/manual.md)
