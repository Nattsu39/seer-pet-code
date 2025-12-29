# PetCode 使用手册

本手册帮助开发者快速掌握 PetCode SDK，用于处理精灵配置数据的标准化交换。

> **说明**：本文档中的所有代码示例和 API 说明均基于 **Python SDK**。其他语言的 SDK 提供相同的功能和类似的 API，具体用法请参考对应 SDK 目录下的文档。

## 目录

1. [简介与核心概念](#1-简介与核心概念)
   - [什么是 PetCode？](#什么是-petcode)
   - [什么是 Protobuf？](#什么是-protobuf)
   - [为什么使用 Protobuf？](#为什么使用-protobuf)
2. [快速开始](#2-快速开始)
   - [5分钟上手示例](#5分钟上手示例)
   - [运行示例](#运行示例)
3. [安装与配置](#3-安装与配置)
   - [Python SDK](#python-sdk)
   - [其他语言 SDK](#其他语言-sdk)
4. [核心数据结构详解](#4-核心数据结构详解)
   - [PetCodeMessage](#petcodemessage)
   - [PetInfo](#petinfo)
   - [PetAbilityValue](#petabilityvalue)
   - [PetAbilityBonus](#petabilitybonus)
   - [MintmarkInfo](#mintmarkinfo)
   - [ResistanceInfo](#resistanceinfo)
   - [Effect](#effect)
   - [SeerSet](#seerset)
5. [常用操作指南](#5-常用操作指南)
   - [数据序列化与反序列化](#数据序列化与反序列化)
   - [创建精灵配置](#创建精灵配置)
   - [读取和修改配置](#读取和修改配置)
   - [多精灵配置](#多精灵配置)
6. [进阶功能](#6-进阶功能)
   - [处理刻印（OneOf 字段）](#处理刻印oneof-字段)
   - [处理效果（Effect）](#处理效果effect)
   - [处理抗性（ResistanceInfo）](#处理抗性resistanceinfo)
7. [最佳实践与注意事项](#7-最佳实践与注意事项)
   - [数据验证策略](#数据验证策略)
   - [版本兼容性](#版本兼容性)
   - [常见陷阱](#常见陷阱)
8. [API 参考](#8-api-参考)
9. [接入规范](#9-接入规范)
   - [登录器/脚本开发者（导出方）](#登录器脚本开发者导出方)
   - [其他工具开发者（导入/导出/展示方）](#其他工具开发者导入导出展示方)

---

## 1. 简介与核心概念

### 什么是 PetCode？

PetCode 是一套用于精灵配置数据交换的标准化协议。它定义了精灵属性、技能、刻印、特性等信息的统一数据格式，使不同工具（登录器、计算器、图鉴站等）之间能够无缝共享数据。

### 什么是 Protobuf？

Protocol Buffers（Protobuf）是 Google 开发的一种数据序列化格式，类似于 JSON 或 XML，但具有以下优势：

- **体积更小**：二进制格式比 JSON 减少 60-80% 的体积
- **速度更快**：序列化和反序列化性能比 JSON 快 3-10 倍
- **强类型**：每个字段都有明确的类型定义
- **跨语言**：支持 20+ 种编程语言

### 为什么使用 Protobuf？

PetCode 选择 Protobuf 的核心原因：

1. **自动代码生成**：从 `.proto` 文件自动生成各语言的 SDK，无需手动编写解析代码
2. **向后兼容**：通过字段编号机制，可以在不破坏现有工具的情况下扩展协议
3. **数据压缩**：配合 Gzip 压缩，生成的精灵码非常紧凑，适合二维码分享

> **提示**：你不需要深入学习 Protobuf，SDK 已经封装了所有复杂操作。把它当作普通的数据类使用即可。

---

## 2. 快速开始

### 5分钟上手示例

下面展示如何创建一个精灵配置并生成分享码：

```python
from seerbp.petcode.v1.message_pb2 import PetCodeMessage, PetInfo, PetAbilityValue
from petcode import to_base64

# === 场景：创建一只满配精灵用于 PVP ===

# 步骤 1：创建精灵的基础信息
my_pet = PetInfo(
    id=3022,              # 精灵 ID
    level=100,            # 等级
    dv=31,                # 个体值
    nature=1,             # 性格 ID
    evs=PetAbilityValue(  # 学习力分配
        hp=255,
        attack=255,
        defense=0,
        special_attack=0,
        special_defense=0,
        speed=0
    ),
    skills=[19248, 19229, 24707, 24717, 19230],  # 技能 ID 列表（最多5个）
    ability_total=PetAbilityValue(  # 最终能力值（面板数值）
        hp=1209,
        attack=632,
        defense=433,
        special_attack=250,
        special_defense=433,
        speed=369,
    )
)

# 步骤 2：将精灵包装在消息容器中
message = PetCodeMessage(
    server=PetCodeMessage.Server.SERVER_OFFICIAL,  # 官服数据
    display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,  # PVP 展示模式
    pets=[my_pet]  # 精灵列表
)

# 步骤 3：生成 Base64 分享码
code = to_base64(message)
print(f"生成的精灵码: {code}")
# 输出示例: H4sIAAAAAAAC/2WOQQ6AIAxE7/IXa0IwRr3FslAoP...
```

### 运行示例

```bash
# 确保已安装 SDK
pip install petcode

# 运行上面的代码
python your_script.py
```

> **提示**：生成的 Base64 字符串可以直接用于直接分享或生成二维码。

---

## 3. 安装与配置

### Python SDK

**系统要求**：Python 3.10 或更高版本

**安装**：

```bash
pip install petcode
```

**验证安装**：

```python
import petcode
from seerbp.petcode.v1.message_pb2 import PetCodeMessage
print("SDK 安装成功！")
```

### 其他语言 SDK

PetCode 还提供以下语言的 SDK：

- **TypeScript/JavaScript**：请参考 `sdk/ts/README.md`
- **其他语言**：SDK 功能大体相似，请参考各自的 README

> **注意**：虽然本文档的示例使用 Python，但所有语言的官方 SDK 都提供相同的数据结构和功能。核心概念和使用方法在各语言间是通用的

---

## 4. 核心数据结构详解

> **提示**：也可直接查看自动生成的 [数据结构文档](data-structure.md) 了解数据结构和字段含义。

### PetCodeMessage

这是整个数据交换的**根对象**，所有数据都必须包裹在这个对象中。

**主要字段**：

| 字段 | 类型 | 必填 | 说明 |
| ------ | ------ | ------ | ------ |
| `server` | `Server` 枚举 | 是 | 来源服务器（官服、测试服、台服等） |
| `display_mode` | `DisplayMode` 枚举 | 是 | 展示模式（PVP、PVE、BOSS） |
| `pets` | `PetInfo` 列表 | 是 | 精灵信息列表（1-6 只） |
| `seer_set` | `SeerSet` | 否 | 赛尔套装和称号信息 |

**枚举值**：

```python
# Server（服务器）
SERVER_OFFICIAL = 1   # 官方服
SERVER_TEST = 2       # 测试服
SERVER_TAIWAN = 3     # 台服
SERVER_CLASSIC = 4    # 经典服

# DisplayMode（展示模式）
DISPLAY_MODE_PVP = 1   # PVP 模式
DISPLAY_MODE_PVE = 2   # PVE 模式
DISPLAY_MODE_BOSS = 3  # BOSS 模式
```

### PetInfo

描述**单只精灵**的核心对象。

**基础属性字段**：

| 字段 | 类型 | 必填 | 说明 |
| ------ | ------ | ------ | ------ |
| `id` | `int` | 是 | 精灵 ID |
| `level` | `int` | 是 | 等级 |
| `dv` | `int` | 是 | 个体值 |
| `nature` | `int` | 否 | 性格 ID |
| `evs` | `PetAbilityValue` | 否 | 学习力（总和 ≤ 510） |
| `extra_hp` | `int` | 否 | 体力上限附加值 |
| `is_awaken` | `bool` | 否 | 是否神谕觉醒 |
| `skin_id` | `int` | 否 | 皮肤 ID |

**技能相关字段**：

| 字段 | 类型 | 必填 | 说明 |
| ------ | ------ | ------ | ------ |
| `skills` | `int` 列表 | 否 | 技能 ID 列表（最多 5 个，第五技能在最后） |

> **技能石说明**：
>
> 技能石 ID 由以下公式计算：
>
> ```text
> 技能石ID = 类型系数 × 100000 + 完美技能石效果ID × 1000 + 技能石ID
> ```
>
> 其中：
>
> - **类型系数**：物攻技能石为 `1`，特攻技能石为 `2`
> - **完美技能石效果ID**：完美技能石的效果 ID
> - **技能石ID**：基础技能石 ID
>
> 示例：
>
> ```python
> # 物攻技能石（类型=1，效果=5，基础ID=123）
> skill_stone_id = 1 * 100000 + 5 * 1000 + 123  # = 105123
>
> # 特攻技能石（类型=2，效果=2，基础ID=456）
> skill_stone_id = 2 * 100000 + 2 * 1000 + 45  # = 202045
> ```

**刻印与战斗道具字段**：

| 字段 | 类型 | 必填 | 说明 |
| ------ | ------ | ------ | ------ |
| `mintmarks` | `MintmarkInfo` 列表 | 否 | 刻印信息（最多 3 个） |
| `pet_items` | `int` 列表 | 否 | 战斗道具 ID 列表 |

**效果与加成字段**：

| 字段 | 类型 | 必填 | 说明 |
| ------ | ------ | ------ | ------ |
| `effects` | `Effect` 列表 | 否 | 特性、异能特质、魂印等效果 |
| `ability_bonus` | `PetAbilityBonus` 列表 | 否 | 能力加成详情（年费、战队等） |
| `resistance` | `ResistanceInfo` | 否 | 抗性信息 |

**最终属性字段**：

| 字段 | 类型 | 必填 | 说明 |
| ------ | ------ | ------ | ------ |
| `ability_total` | `PetAbilityValue` | 否 | 最终能力值总和（面板数值） |

### PetAbilityValue

精灵的**六项能力值**对象，用于表示学习力、能力总和等。

**字段**：

| 字段 | 类型 | 说明 |
| ------ | ------ | ------ |
| `hp` | `int` | 体力值 |
| `attack` | `int` | 攻击值 |
| `defense` | `int` | 防御值 |
| `special_attack` | `int` | 特攻值 |
| `special_defense` | `int` | 特防值 |
| `speed` | `int` | 速度值 |

**使用示例**：

```python
# 学习力分配
evs = PetAbilityValue(
    hp=255,
    attack=255,
    defense=0,
    special_attack=0,
    special_defense=0,
    speed=0
)

# 最终能力值
ability_total = PetAbilityValue(
    hp=1209,
    attack=632,
    defense=433,
    special_attack=250,
    special_defense=433,
    speed=369
)
```

### PetAbilityBonus

精灵的**额外能力加成**信息，如年费加成、战队加成等。

**结构说明**：

- `type`：加成类型（枚举）
- `value`：加成详情，包含六项能力的加成值
  - 每项加成可以是**固定值**（`value`）或**百分比**（`percent`），二者也可以同时设置

**加成类型枚举**：

| 枚举值 | 数值 | 说明 |
| ------ | ------ | ------ |
| `TYPE_TEAM_TECH` | 1 | 战队加成 |
| `TYPE_ANNUAL_VIP` | 2 | 年费加成 |
| `TYPE_SUPER_NONO` | 3 | 超能 NoNo 加成 （闪光/暗黑加成） |
| `TYPE_SOULMARK` | 4 | 魂印加成 |
| `TYPE_AWAKEN` | 5 | 神谕觉醒加成 |
| `TYPE_SPECIAL` | 6 | 特殊加成 |
| `TYPE_OTHER` | 99 | 其他加成 |

**完整示例**：

```python
from seerbp.petcode.v1.message_pb2 import PetAbilityBonus

# 创建年费加成（全属性 +10）
annual_vip_bonus = PetAbilityBonus(
    type=PetAbilityBonus.Type.TYPE_ANNUAL_VIP,
    value=PetAbilityBonus.Value(
        hp=PetAbilityBonus.ExtraValue(value=10),
        attack=PetAbilityBonus.ExtraValue(value=10),
        defense=PetAbilityBonus.ExtraValue(value=10),
        special_attack=PetAbilityBonus.ExtraValue(value=10),
        special_defense=PetAbilityBonus.ExtraValue(value=10),
        speed=PetAbilityBonus.ExtraValue(value=10),
    ),
)

# 创建百分比加成（攻击 +15%）
percent_bonus = PetAbilityBonus(
    type=PetAbilityBonus.Type.TYPE_SPECIAL,
    value=PetAbilityBonus.Value(
        attack=PetAbilityBonus.ExtraValue(percent=15),
        # 其他属性不加成则不设置
    ),
)

# 将加成添加到精灵
my_pet.ability_bonus.extend([annual_vip_bonus, percent_bonus])
```

### MintmarkInfo

精灵的**刻印信息**。刻印有 4 种类型，使用 Protobuf 的 `oneof` 机制表示（同一时间只能是其中一种）。

**刻印类型**：

1. **技能刻印**（`skill`）：只有 ID
2. **能力刻印**（`ability`）：只有 ID
3. **全能刻印**（`universal`）：包含 ID、等级、自定义能力值、宝石信息
4. **全效刻印**（`quanxiao`）：包含能力刻印 ID 和技能刻印 ID

**全能刻印详细字段**：

| 字段 | 类型 | 必填 | 说明 |
| ------ | ------ | ------ | ------ |
| `id` | `int` | 是 | 刻印 ID |
| `level` | `int` | 是 | 刻印等级（1-5） |
| `ability` | `PetAbilityValue` | 否 | 自定义能力值（旧版随机刻印） |
| `gem` | `GemItem` | 否 | 宝石信息 |

**宝石信息（GemItem）**：

| 字段 | 类型 | 说明 |
| ------ | ------ | ------ |
| `gem_id` | `int` | 宝石 ID |
| `bind_skill_id` | `int` | 宝石绑定的技能 ID |

**使用示例见第 6 章**。

### ResistanceInfo

精灵的**抗性信息**，包括伤害抗性和状态抗性。

**结构说明**：

```python
ResistanceInfo(
    hurt=ResistanceInfo.Hurt(
        crit=35,        # 暴击抗性（百分比）
        regular=35,     # 普通伤害抗性（百分比）
        precent=35      # 百分比伤害抗性（百分比）
    ),
    ctl=[              # 控制类状态抗性列表
        ResistanceInfo.StateItem(state_id=1, percent=55),  # 状态 ID 1，抗性 55%
        ResistanceInfo.StateItem(state_id=2, percent=18),
        ResistanceInfo.StateItem(state_id=3, percent=10),
    ],
    weak=[             # 弱化类状态抗性列表
        ResistanceInfo.StateItem(state_id=4, percent=10),
        ResistanceInfo.StateItem(state_id=5, percent=10),
        ResistanceInfo.StateItem(state_id=6, percent=10),
    ]
)
```

**字段说明**：

- `hurt`：伤害抗性（暴击、固伤、百分比）
- `ctl`：控制类状态抗性列表（如冰冻、麻痹等）
- `weak`：弱化类状态抗性列表（如烧伤、中毒等）

**使用辅助函数创建**（见第 8 章 API 参考）。

### Effect

精灵的**特殊效果**，包括特性、异能特质、魂印等。

> **重要**：在游戏内数据包中，特性、异能特质、魂印等都使用 `PetEffectInfo` 结构体描述，PetCode 采用相同设计以确保游戏数据包与工具的双重兼容性。

**字段**：

| 字段 | 类型 | 说明 |
| ------ | ------ | ------ |
| `id` | `int` | 效果 ID（特性 idx、魂印 ID 等） |
| `status` | `int` | 效果类型（区分特性、魂印等） |
| `args` | `int` 列表 | 效果参数 |

**效果类型（status 字段）**：

> **注意**：该值仅在 API 中为枚举，Protobuf 协议内定义为 `int32` 类型。

| 类型 | 数值 | 说明 |
| ------ | ------ | ------ |
| `GENERAL` | 1 | 特性 |
| `ITEM` | 2 | 道具效果 |
| `VARIATION` | 4 | 异能特质 |
| `SOULMARK` | 5 | 魂印 |
| `TEAM_TECH` | 7 | 战队科技 |
| `OTHER` | 99 | 其他 |

**使用示例**：

```python
from seerbp.petcode.v1.message_pb2 import PetInfo

# 添加特性（status=1）
effect_general = PetInfo.Effect(
    id=67,          # 特性 idx
    status=1,       # GENERAL
    args=[1, 5]     # 特性参数
)

# 添加异能特质（status=4）
effect_variation = PetInfo.Effect(
    id=407,         # 异能特质 ID
    status=4,       # VARIATION
    args=[2, 15]    # 特质参数
)

# 添加到精灵
my_pet.effects.extend([effect_general, effect_variation])
```

> **注意**：
>
> - 道具类效果请使用 `pet_items` 字段，不要在 `effects` 中重复添加
> - 战队加成请使用 `ability_bonus` 字段

### SeerSet

赛尔的**套装和称号**信息。

**字段**：

| 字段 | 类型 | 说明 |
| ------ | ------ | ------ |
| `equips` | `int` 列表 | 套装部件 ID 列表（最多 5 个） |
| `title_id` | `int` | 称号 ID |

**使用示例**：

```python
from seerbp.petcode.v1.message_pb2 import PetCodeMessage

message = PetCodeMessage(
    server=PetCodeMessage.Server.SERVER_OFFICIAL,
    display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
    seer_set=PetCodeMessage.SeerSet(
        equips=[1301035, 1301041, 1301036, 1301037, 1301038],  # 5 件套装
        title_id=100  # 称号 ID
    ),
    pets=[...]
)
```

---

## 5. 常用操作指南

### 数据序列化与反序列化

SDK 提供了便捷的函数来进行数据格式转换。

> **⚠️ 关键警告：Protobuf 序列化不是规范化的（Non-Canonical）**
>
> 根据 [Protobuf 官方文档](https://protobuf.dev/programming-guides/serialization-not-canonical/)，即使两个 `PetCodeMessage` 对象包含**完全相同的数据**，它们的二进制序列化结果也可能不同。这意味着：
>
> - **不同的二进制哈希值**（MD5、SHA256 等）
> - **不同的 Base64 编码字符串**
>
> **原因包括：**
>
> - 字段可以按任意顺序序列化
> - 未知字段的位置和处理方式不确定
> - Map 类型的字段顺序未定义
> - 不同 SDK 版本、编译选项或优化策略的差异
>
> **因此，请勿：**
>
> - ❌ 使用二进制哈希或 Base64 字符串比较两个配置是否相同
> - ❌ 将序列化后的二进制或 Base64 作为哈希表的键
>
> **正确做法：**
>
> - ✅ 先反序列化为对象，然后逐字段比较数据内容
> - ✅ 对于数据一致性检查，比较对象字段而非二进制表示

**导入**：

```python
from petcode import to_base64, from_base64, to_binary, from_binary, to_dict, from_dict
```

#### 1. Base64 编码（用于分享）

```python
# 序列化为 Base64 字符串（内部已 Gzip 压缩）
code = to_base64(message)
print(code)
# 输出: H4sIAAAAAAAC/2WOQQ6AIAxE7/IXa...

# 从 Base64 字符串还原（内部自动解压）
message = from_base64(code)
print(f"精灵 ID: {message.pets[0].id}")
```

> **用途**：生成分享码、二维码内容、URL 参数

#### 2. 二进制编码（用于存储）

```python
# 序列化为二进制（内部已 Gzip 压缩）
binary = to_binary(message)
print(f"数据大小: {len(binary)} 字节")

# 从二进制还原（内部自动解压）
message = from_binary(binary)
```

> **用途**：存入数据库、文件存储、网络传输

#### 3. 字典/JSON 转换

```python
# 转换为字典（用于调试或 JSON API）
data_dict = to_dict(message)
print(data_dict)
# 输出: {'server': 'SERVER_OFFICIAL', 'displayMode': 'DISPLAY_MODE_PVP', ...}

# 从字典还原
message = from_dict(data_dict)
```

> **用途**：调试输出、JSON API 交互、可读性展示

### 创建精灵配置

**基础精灵配置**：

```python
from seerbp.petcode.v1.message_pb2 import PetCodeMessage, PetInfo, PetAbilityValue
from petcode import to_base64

# 创建一只基础精灵
pet = PetInfo(
    id=3022,
    level=100,
    dv=31,
    nature=1,
    evs=PetAbilityValue(hp=255, attack=255, speed=0, defense=0, special_attack=0, special_defense=0),
    skills=[19248, 19229, 24707],
    ability_total=PetAbilityValue(hp=1200, attack=600, defense=400, special_attack=250, special_defense=400, speed=350)
)

# 包装并生成
message = PetCodeMessage(
    server=PetCodeMessage.Server.SERVER_OFFICIAL,
    display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
    pets=[pet]
)

code = to_base64(message)
```

**带刻印和特性的精灵**：

```python
from petcode.create_and_read import create_universal_mintmark

pet = PetInfo(
    id=3022,
    level=100,
    # ... 其他基础属性 ...
    
    # 添加刻印
    mintmarks=[
        create_universal_mintmark(40001, 5, gem_id=1800011, bind_skill_id=24708),
        create_universal_mintmark(40002, 5),
    ],
    
    # 添加特性
    effects=[
        PetInfo.Effect(id=67, status=1, args=[1, 5]),  # 特性
    ],
    
    # 添加战斗道具
    pet_items=[300001, 300002],
)
```

### 读取和修改配置

```python
from petcode import from_base64

# 读取分享码
code = "H4sIAAAAAAAC/2WOQQ6AIAxE7/IXa..."
message = from_base64(code)

# 读取精灵信息
first_pet = message.pets[0]
print(f"精灵 ID: {first_pet.id}")
print(f"等级: {first_pet.level}")
print(f"个体值: {first_pet.dv}")
print(f"学习力: 体力={first_pet.evs.hp}, 攻击={first_pet.evs.attack}")

# 修改精灵
first_pet.level = 99  # 修改等级
first_pet.skills.append(24717)  # 添加技能

# 重新生成分享码
new_code = to_base64(message)
```

**读取刻印**：

```python
from petcode.create_and_read import read_mintmark
from seerbp.petcode.v1.message_pb2 import MintmarkInfo

for mintmark in first_pet.mintmarks:
    data = read_mintmark(mintmark)
    
    if isinstance(data, MintmarkInfo.Universal):
        print(f"全能刻印: ID={data.id}, 等级={data.level}")
        if data.HasField('gem'):
            print(f"  宝石: {data.gem.gem_id}, 绑定技能: {data.gem.bind_skill_id}")
    elif isinstance(data, MintmarkInfo.Skill):
        print(f"技能刻印: ID={data.id}")
```

### 多精灵配置

```python
# 创建 6 只精灵的配置
pets = []
for i in range(6):
    pet = PetInfo(
        id=3000 + i,
        level=100,
        dv=31,
        # ... 其他属性 ...
    )
    pets.append(pet)

message = PetCodeMessage(
    server=PetCodeMessage.Server.SERVER_OFFICIAL,
    display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
    pets=pets  # 传入精灵列表
)

code = to_base64(message)
```

---

## 6. 进阶功能

### 处理刻印（OneOf 字段）

刻印使用 Protobuf 的 `oneof` 机制，同一时间只能是 4 种类型之一。

#### 方法 1：使用辅助函数（推荐）

SDK 提供了便捷的创建和读取函数：

```python
from petcode.create_and_read import (
    create_skill_mintmark,
    create_ability_mintmark,
    create_universal_mintmark,
    create_quanxiao_mintmark,
    read_mintmark
)

# 创建技能刻印
skill_mm = create_skill_mintmark(id=50001)

# 创建能力刻印
ability_mm = create_ability_mintmark(id=60001)

# 创建全能刻印（无宝石）
universal_mm = create_universal_mintmark(id=40001, level=5)

# 创建全能刻印（带宝石）
universal_mm_with_gem = create_universal_mintmark(
    id=40001,
    level=5,
    gem_id=1800011,
    bind_skill_id=24708
)

# 创建全能刻印（自定义能力值，用于旧版刻印升级系统）
universal_mm_custom = create_universal_mintmark(
    id=40001,
    level=5,
    ability=PetAbilityValue(hp=100, attack=120, defense=80, special_attack=90, special_defense=85, speed=110)
)

# 创建全效刻印
quanxiao_mm = create_quanxiao_mintmark(
    id=10001,
    skill_mintmark_id=20001
)

# 添加到精灵
my_pet.mintmarks.extend([universal_mm_with_gem, skill_mm, ability_mm])
```

**读取刻印**：

```python
from seerbp.petcode.v1.message_pb2 import MintmarkInfo

for mintmark in my_pet.mintmarks:
    data = read_mintmark(mintmark)
    
    if isinstance(data, MintmarkInfo.Universal):
        print(f"全能刻印: ID={data.id}, 等级={data.level}")
        if data.HasField('gem'):
            print(f"  宝石 ID: {data.gem.gem_id}")
            print(f"  绑定技能: {data.gem.bind_skill_id}")
        if data.HasField('ability'):
            print(f"  自定义能力: 体力={data.ability.hp}, 攻击={data.ability.attack}")
            
    elif isinstance(data, MintmarkInfo.Skill):
        print(f"技能刻印: ID={data.id}")
        
    elif isinstance(data, MintmarkInfo.Ability):
        print(f"能力刻印: ID={data.id}")
        
    elif isinstance(data, MintmarkInfo.Quanxiao):
        print(f"全效刻印: 能力刻印={data.id}, 技能刻印={data.skill_mintmark_id}")
```

#### 方法 2：使用 Protobuf 原生方法

```python
# 判断刻印类型
mintmark_type = mintmark.WhichOneof('mintmark')

if mintmark_type == 'universal':
    print(f"全能刻印: {mintmark.universal.id}")
elif mintmark_type == 'skill':
    print(f"技能刻印: {mintmark.skill.id}")
elif mintmark_type == 'ability':
    print(f"能力刻印: {mintmark.ability.id}")
elif mintmark_type == 'quanxiao':
    print(f"全效刻印: {mintmark.quanxiao.id}")
```

### 处理效果（Effect）

效果通过 `status` 字段区分类型。

```python
from petcode.effect import get_effect_type, EffectType

# 创建不同类型的效果
effect_general = PetInfo.Effect(id=67, status=1, args=[1, 5])      # 特性
effect_variation = PetInfo.Effect(id=407, status=4, args=[2, 15])  # 异能特质
effect_soulmark = PetInfo.Effect(id=5001, status=5, args=[])       # 魂印

my_pet.effects.extend([effect_general, effect_variation, effect_soulmark])

# 读取和分类效果
for effect in my_pet.effects:
    effect_type = get_effect_type(effect.status)
    
    if effect_type == EffectType.GENERAL:
        print(f"特性: idx={effect.id}, 参数={effect.args}")
        
    elif effect_type == EffectType.VARIATION:
        print(f"异能特质: ID={effect.id}, 参数={effect.args}")
        
    elif effect_type == EffectType.SOULMARK:
        print(f"魂印: ID={effect.id}, 参数={effect.args}")
        
    elif effect_type == EffectType.OTHER:
        print(f"其他效果: ID={effect.id}, status={effect.status}")
```

### 处理抗性（ResistanceInfo）

**使用辅助函数创建**：

```python
from petcode.create_and_read import create_state_resist
from seerbp.petcode.v1.message_pb2 import ResistanceInfo

# 创建完整的抗性信息
resistance = ResistanceInfo(
    # 伤害抗性
    hurt=ResistanceInfo.Hurt(
        crit=35,      # 暴击抗性 35%
        regular=35,   # 普通伤害抗性 35%
        precent=35    # 百分比伤害抗性 35%
    ),
    # 控制类状态抗性（使用辅助函数）
    ctl=create_state_resist(
        (1, 55),  # 状态 1 抗性 55%
        (2, 18),  # 状态 2 抗性 18%
        (3, 10)   # 状态 3 抗性 10%
    ),
    # 弱化类状态抗性
    weak=create_state_resist(
        (4, 10),
        (5, 10),
        (6, 10)
    )
)

my_pet.resistance.CopyFrom(resistance)
```

**手动创建**：

```python
resistance = ResistanceInfo(
    hurt=ResistanceInfo.Hurt(crit=35, regular=35, precent=35),
    ctl=[
        ResistanceInfo.StateItem(state_id=1, percent=55),
        ResistanceInfo.StateItem(state_id=2, percent=18),
        ResistanceInfo.StateItem(state_id=3, percent=10),
    ],
    weak=[
        ResistanceInfo.StateItem(state_id=4, percent=10),
        ResistanceInfo.StateItem(state_id=5, percent=10),
    ]
)
```

**读取抗性**：

```python
if my_pet.HasField('resistance'):
    res = my_pet.resistance
    print(f"暴击抗性: {res.hurt.crit}%")
    print(f"固定伤害抗性: {res.hurt.regular}%")
    print(f"百分比伤害抗性: {res.hurt.precent}%")
    
    print("控制类状态抗性:")
    for state in res.ctl:
        print(f"  状态 {state.state_id}: {state.percent}%")
    
    print("弱化类状态抗性:")
    for state in res.weak:
        print(f"  状态 {state.state_id}: {state.percent}%")
```

---

## 7. 最佳实践与注意事项

### 数据验证策略

PetCode 基于 Proto3 协议，**所有字段都是可选的**，并且没有默认值的概念（数值型默认为 0，字符串默认为空串）。

**最佳实践**：

1. **创建数据前进行业务逻辑校验**

```python
def create_validated_pet(id: int, level: int, dv: int, **kwargs):
    assert 0 < level, "等级必须大于0"
    assert 0 <= dv <= 31, "个体值必须在 0-31 之间"
    
    # 创建对象
    return PetInfo(id=id, level=level, dv=dv, **kwargs)
```

1. **读取数据时进行防御性检查**

```python
def safe_get_level(pet: PetInfo, mode: PetCodeMessage.DisplayMode) -> int:
    """安全获取等级，返回合法值"""
    level = pet.level
    if mode != PetCodeMessage.DisplayMode.DISPLAY_MODE_BOSS:
        assert 0 < level, ValueError("等级必须大于0")
    else:
        assert 1 <= level <= 100, ValueError("等级必须在 1-100 之间")
    return level
```

1. **使用 HasField 检查可选字段**

```python
# 正确
if pet.HasField('resistance'):
    print(pet.resistance.hurt.crit)

# 错误：可能访问不存在的字段
print(pet.resistance.hurt.crit)  # 如果 resistance 不存在会返回默认值 0
```

### 版本兼容性

Protobuf 强大的向后兼容性允许协议在不破坏现有客户端的情况下演进。

**保持兼容性的原则**：

1. **透传未知字段**

```python
# 如果你的工具遇到了不认识的字段，请保留它们
# Protobuf 会自动保留未知字段，你只需要：
# 1. 读取数据
message = from_base64(code)

# 2. 修改已知字段
message.pets[0].level = 99

# 3. 重新序列化（未知字段会被自动保留）
new_code = to_base64(message)
```

### 常见陷阱

#### Proto3 的零值问题

```python
# 陷阱：无法区分"未设置"和"设置为 0"
pet = PetInfo()
print(pet.level)  # 输出 0，但不知道是未设置还是真的为 0

# 解决方案：对于必填字段，总是显式设置
pet = PetInfo(id=3022, level=100, dv=31)
```

#### 刻印类型混淆

```python
# 陷阱：直接访问可能不存在的 oneof 字段
print(mintmark.universal.id)  # 如果是技能刻印，会返回默认值而不是报错！

# 解决方案：使用辅助函数或 WhichOneof
data = read_mintmark(mintmark)
if isinstance(data, MintmarkInfo.Universal):
    print(data.id)
```

#### 道具和效果混淆

```python
# 错误：将道具添加到 effects
pet.effects.append(PetInfo.Effect(id=300001, status=2))  # status=2 是 ITEM 类型特效

# 正确：道具应添加到 pet_items
pet.pet_items.append(300001)
```

---

## 8. API 参考

**[Python SDK API 参考文档](../sdk/py/README.md)**

其他语言 SDK 的 API 参考请查看对应 SDK 目录下的 README 文档。所有的官方 PetCode SDK 均拥有这些函数，行为大体一致。

---

## 9. 接入规范

如果你是工具或平台开发者，并希望接入 PetCode 标准，请参考以下条件。

### 登录器/脚本开发者（导出方）

对于用于从游戏内导出精灵配置的登录器或脚本，**必须满足**以下核心条件：

1. **完整解析能力**：能够完整解析游戏内的 `PetInfo` 数据包。
2. **刻印信息获取**：能够通过刻印唯一 ID（获取时间）准确获得刻印的详细信息（如 ID、等级、属性，宝石绑定信息等）。

此外，**至少需要满足**下列条件之一以生成标准数据：

- **集成 SDK**：直接集成任意语言版本的 PetCode SDK。
- **远程生成**：通过 HTTP 请求调用远端服务来生成 Protobuf 数据（仅适用于无法直接运行 SDK 的环境）。

### 其他工具开发者（导入/导出/展示方）

对于既需要导入又需要导出的其他工具（如计算器、图鉴站等）：

1. **集成 SDK**：必须直接集成任意语言版本的 PetCode SDK 到工具中。直接集成可以提供更好的性能和用户体验，实现离线处理能力，避免对远程服务的依赖和网络开销。
2. **效果类型识别**：工具必须能够通过 `Effect` 数据对象的 `status` 字段正确分辨效果类型（特性、特质、魂印等），并据此进行正确的展示或计算。

> **提示**：使用 `petcode.effect.get_effect_type()` 函数可以轻松识别效果类型。

---

## 结语

本手册涵盖了 PetCode SDK 的主要功能和最佳实践。如果你在使用过程中遇到问题：

1. 检查 [API 参考](#8-api-参考) 了解具体函数用法
2. 参考各语言 SDK 的 README 文档
3. 查看 [数据结构文档](data-structure.md) 了解数据结构和字段含义

祝你使用愉快！
