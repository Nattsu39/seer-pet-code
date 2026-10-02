# PetCode SDK 开发指南

本文档面向希望为 PetCode 项目开发新语言 SDK 的开发者，介绍如何基于 Protobuf 原生 SDK 构建封装层，提供便捷的序列化、辅助创建等功能。

## 目录

1. [简介](#简介)
2. [Buf 和 BSR 介绍](#buf-和-bsr-介绍)
3. [PetCode SDK 与 Protobuf 原生 SDK 的区别](#petcode-sdk-与-protobuf-原生-sdk-的区别)
4. [通过 BSR 获取原生 SDK](#通过-bsr-获取原生-sdk)
5. [PetCode SDK 需要实现的函数](#petcode-sdk-需要实现的函数)
6. [开发流程示例](#开发流程示例)
7. [测试与发布](#测试与发布)

---

## 简介

PetCode 使用 Protocol Buffers 作为数据交换格式，并通过 [Buf](https://buf.build) 工具链来管理 `.proto` 文件和自动生成各语言的代码。

开发一个完整的 PetCode SDK 需要两个步骤：

1. **获取 Protobuf 原生 SDK**：通过 BSR 获取自动生成的数据结构代码
2. **封装 PetCode SDK**：在原生 SDK 基础上封装便捷的序列化、辅助创建等功能

> **说明**：本文档使用 **Python** 作为示例语言展示实现细节。其他语言的 SDK 开发流程和核心概念完全相同，只是具体语法有所差异。你可以参考现有的 Python 和 TypeScript SDK 源码作为参考。

---

## Buf 和 BSR 介绍

### 什么是 Buf？

**Buf** 是一个现代化的 Protobuf 工具链，用于替代传统的 `protoc` 编译器。它提供了更好的开发体验：

- **简化配置**：通过 `buf.yaml` 统一管理 proto 文件
- **自动代码生成**：通过 `buf.gen.yaml` 配置代码生成规则
- **依赖管理**：像 npm/pip 一样管理 proto 依赖
- **Linting 和格式化**：内置 proto 文件的代码检查和格式化工具
- **向后兼容性检查**：自动检测破坏性变更

### 什么是 BSR？

**BSR（Buf Schema Registry）** 是 Buf 提供的 Protobuf 模式注册中心，类似于 npm Registry 或 PyPI，用于发布和分发 Protobuf 模式。

BSR 的核心功能：

1. **集中式模式管理**：将 proto 文件发布到 BSR，供其他项目引用
2. **自动代码生成**：BSR 自动为各种语言生成代码，无需本地安装 `protoc`
3. **版本管理**：支持语义化版本控制，确保向后兼容
4. **包发布**：将生成的代码发布到各语言的包管理器（npm、PyPI 等）

### PetCode 使用 BSR 的方式

PetCode 项目将 `.proto` 文件发布到 BSR 上：

- **BSR 地址**：[`buf.build/seerbp/petcode`](https://buf.build/seerbp/petcode)
- **自动生成**：BSR 自动为多种语言生成原生 SDK
- **包发布**：生成的代码会自动发布到对应的包管理器

---

## PetCode SDK 与 Protobuf 原生 SDK 的区别

### Protobuf 原生 SDK

Protobuf 原生 SDK 是由 `protoc` 或 Buf 自动从 `.proto` 文件生成的代码，提供基础的数据结构定义和序列化功能。

**特点**：

- ✅ 包含所有 proto 定义的消息类型和枚举
- ✅ 提供基础的序列化/反序列化功能（如 `SerializeToString()`、`ParseFromString()`）
- ❌ 没有压缩功能（需手动实现 gzip）
- ❌ 没有 Base64 编码功能
- ❌ 没有便捷的辅助创建函数（如刻印、抗性等复杂结构）
- ❌ API 较为底层，使用相对繁琐

**示例**（Python 原生 SDK）：

```python
from seerbp.petcode.v1.message_pb2 import PetCodeMessage

# 基础序列化（无压缩）
binary = message.SerializeToString()

# 基础反序列化
message = PetCodeMessage()
message.ParseFromString(binary)
```

### PetCode SDK

PetCode SDK 是在原生 SDK 基础上封装的高级库，提供更便捷的 API 和额外功能。

**特点**：

- ✅ 依赖原生 SDK 作为底层数据结构
- ✅ 提供压缩功能（内置 gzip 压缩）
- ✅ 提供 Base64 编码/解码（用于生成分享码）
- ✅ 提供辅助创建函数（如 `create_universal_mintmark()`）
- ✅ 提供效果类型识别函数（如 `get_effect_type()`）
- ✅ 提供更简洁、更友好的 API

**示例**（Python PetCode SDK）：

```python
from petcode import to_base64, from_base64
from petcode.create_and_read import create_universal_mintmark

# 一行代码序列化为 Base64（内置压缩）
code = to_base64(message)

# 一行代码反序列化
message = from_base64(code)

# 便捷创建刻印
mintmark = create_universal_mintmark(id=40001, level=5, gem_id=1800011, bind_skill_id=24708)
```

### 对比总结

| 功能 | Protobuf 原生 SDK | PetCode SDK |
| ------ | ------------------ | ------------- |
| 数据结构定义 | ✅ | ✅（依赖原生 SDK） |
| 基础序列化 | ✅ | ✅ |
| Gzip 压缩 | ❌ 需手动实现 | ✅ 内置 |
| Base64 编码 | ❌ 需手动实现 | ✅ 内置 |
| JSON 转换 | ✅ 但较繁琐 | ✅ 简化 API |
| 辅助创建函数 | ❌ | ✅ |
| 效果类型识别 | ❌ | ✅ |
| 使用复杂度 | 较高 | 较低 |

---

## 通过 BSR 获取原生 SDK

BSR 支持多种方式获取原生 SDK，以下介绍最常用的两种方式。

### 方式 1：通过包管理器安装（推荐）

BSR 会自动将生成的代码发布到各语言的包管理器，你可以直接安装使用。

```bash
# 安装原生 SDK（以 Python 为例）
pip install seerbp-petcode-protocolbuffers-python --index-url https://buf.build/gen/python
```

**使用示例**：

```python
from seerbp.petcode.v1.message_pb2 import PetCodeMessage, PetInfo

# 创建消息
message = PetCodeMessage(
    server=PetCodeMessage.Server.SERVER_OFFICIAL,
    display_mode=PetCodeMessage.DisplayMode.DISPLAY_MODE_PVP,
    pets=[PetInfo(id=3022, level=100)]
)

# 基础序列化
binary = message.SerializeToString()
```

### 方式 2：通过 Buf CLI 本地生成

如果你的语言没有对应的包发布渠道，或者想要自定义生成选项，可以使用 Buf CLI 本地生成。

#### 1. 安装 Buf CLI

```bash
# macOS
brew install bufbuild/buf/buf

# Linux/Windows（使用二进制）
# 下载地址：https://github.com/bufbuild/buf/releases
```

#### 2. 创建 `buf.gen.yaml` 配置

```yaml
version: v2
plugins:
  # 以 Python 为例
  - remote: buf.build/protocolbuffers/python
    out: ./generated
```

#### 3. 生成代码

```bash
# 从 BSR 生成代码
buf generate buf.build/seerbp/petcode
```

生成的代码会输出到 `./generated` 目录。

### 包名称速查表

> **提示**：请参考 [BSR 仓库页面](https://buf.build/seerbp/petcode/sdks/main:protobuf) 获取详细信息

| 语言 | 包名称 | 安装命令 |
| ------ | -------- | ---------- |
| Python | `seerbp-petcode-protocolbuffers-python` | `pip install seerbp-petcode-protocolbuffers-python --index-url https://buf.build/gen/python` |
| TypeScript | `@buf/seerbp_petcode.bufbuild_es` | `npm install @buf/seerbp_petcode.bufbuild_es` |
| Go | `buf.build/gen/go/seerbp/petcode/protocolbuffers/go` | `go get buf.build/gen/go/seerbp/petcode/protocolbuffers/go` |
| Java | `build.buf.gen.seerbp.petcode.protobuf` | Maven/Gradle 配置（见 BSR 仓库页面） |

---

## PetCode SDK 需要实现的函数

开发 PetCode SDK 的核心目标是在原生 SDK 基础上提供便捷的封装层。以下是必须实现的功能模块和函数。

> **提示**：在开始之前，请参考对应语言的 [Protobuf 文档](https://protobuf.dev)，了解原生 SDK 的使用方法，对于部分非官方插件生成的 SDK （例如：`bufbuild/es`），请查看插件文档。

### 1. 序列化与反序列化模块

这是 SDK 的核心功能，提供压缩和编码支持。

#### 1.1 带压缩的二进制序列化/反序列化

**函数签名**：

```python
def to_binary(message: PetCodeMessage) -> bytes:
    """将消息序列化为二进制数据（内置 gzip 压缩）"""
    pass

def from_binary(data: bytes) -> PetCodeMessage:
    """将二进制数据解压缩并反序列化为消息"""
    pass
```

**实现要点**：

- 使用原生 SDK 的序列化/反序列化为二进制数据的方法
- 使用 gzip 压缩/解压缩（压缩级别建议为 1）
- 处理解压失败、解析失败等异常

**实现示例**：

```python
import gzip
from seerbp.petcode.v1.message_pb2 import PetCodeMessage

def to_binary(message: PetCodeMessage) -> bytes:
    """将消息序列化为二进制数据，并使用 gzip 压缩"""
    binary = message.SerializeToString()
    return gzip.compress(binary, compresslevel=1)

def from_binary(data: bytes) -> PetCodeMessage:
    """将二进制数据解压缩，并反序列化为消息"""
    decompressed = gzip.decompress(data)
    message = PetCodeMessage()
    message.ParseFromString(decompressed)
    return message
```

#### 1.2 Base64 编码/解码

**函数签名**：

```python
def to_base64(message: PetCodeMessage) -> str:
    """将消息序列化为 Base64 字符串（内置压缩）"""
    pass

def from_base64(data: str) -> PetCodeMessage:
    """将 Base64 字符串解码并反序列化为消息"""
    pass
```

**实现要点**：

- 基于 `to_binary()` 和 `from_binary()` 实现
- 使用标准 Base64 编码（Python: `base64.b64encode()`）

**实现示例**：

```python
import base64

def to_base64(message: PetCodeMessage) -> str:
    """将消息序列化为 Base64 字符串"""
    binary = to_binary(message)
    return base64.b64encode(binary).decode('utf-8')

def from_base64(data: str) -> PetCodeMessage:
    """将 Base64 字符串解码并反序列化为消息"""
    binary = base64.b64decode(data)
    return from_binary(binary)
```

#### 1.3 JSON 转换

**函数签名**：

```python
def to_dict(message: PetCodeMessage) -> dict:
    """将消息转换为字典（JSON 格式）"""
    pass

def from_dict(data: dict) -> PetCodeMessage:
    """将字典反序列化为消息"""
    pass
```

**实现要点**：

- 使用 Protobuf 库提供的 JSON 转换工具（Python: `json_format.MessageToDict()`）
- 枚举值应转换为字符串（如 `SERVER_OFFICIAL`）而非数字

**实现示例**：

```python
from google.protobuf import json_format

def to_dict(message: PetCodeMessage) -> dict:
    """将消息转换为字典"""
    return json_format.MessageToDict(message)

def from_dict(data: dict) -> PetCodeMessage:
    """将字典反序列化为消息"""
    return json_format.ParseDict(data, PetCodeMessage())
```

---

### 2. 辅助创建函数模块

为了简化复杂数据结构的创建（如刻印、抗性等），SDK 应提供辅助创建函数。

#### 2.1 刻印创建函数

**需要实现的函数**：

```python
def create_skill_mintmark(id: int) -> MintmarkInfo:
    """创建技能刻印"""
    pass

def create_ability_mintmark(id: int) -> MintmarkInfo:
    """创建能力刻印"""
    pass

def create_universal_mintmark(
    id: int,
    level: int,
    *,
    gem_id: int = None,
    bind_skill_id: int = None,
    ability: PetAbilityValue = None
) -> MintmarkInfo:
    """创建全能刻印"""
    pass

def create_quanxiao_mintmark(id: int, *, skill_mintmark_id: int) -> MintmarkInfo:
    """创建全效刻印"""
    pass

def read_mintmark(mintmark: MintmarkInfo) -> MintmarkInfo.Skill | MintmarkInfo.Ability | MintmarkInfo.Universal | MintmarkInfo.Quanxiao:
    """读取刻印的具体类型"""
    pass
```

**实现要点**：

- 使用 Protobuf 的 `oneof` 机制正确设置刻印类型
- `create_universal_mintmark()` 需处理宝石信息和自定义能力值
- `read_mintmark()` 需正确识别刻印类型

**实现示例**：

```python
from seerbp.petcode.v1.message_pb2 import MintmarkInfo, PetAbilityValue

def create_skill_mintmark(id: int) -> MintmarkInfo:
    """创建技能刻印"""
    return MintmarkInfo(skill=MintmarkInfo.Skill(id=id))

def create_ability_mintmark(id: int) -> MintmarkInfo:
    """创建能力刻印"""
    return MintmarkInfo(ability=MintmarkInfo.Ability(id=id))

def create_universal_mintmark(
    id: int,
    level: int,
    *,
    gem_id: int = None,
    bind_skill_id: int = None,
    ability: PetAbilityValue = None
) -> MintmarkInfo:
    """创建全能刻印"""
    universal = MintmarkInfo.Universal(id=id, level=level)
    
    # 添加宝石信息
    if gem_id is not None and bind_skill_id is not None:
        universal.gem.gem_id = gem_id
        universal.gem.bind_skill_id = bind_skill_id
    
    # 添加自定义能力值
    if ability is not None:
        universal.ability.CopyFrom(ability)
    
    return MintmarkInfo(universal=universal)

def create_quanxiao_mintmark(id: int, *, skill_mintmark_id: int) -> MintmarkInfo:
    """创建全效刻印"""
    return MintmarkInfo(
        quanxiao=MintmarkInfo.Quanxiao(
            id=id,
            skill_mintmark_id=skill_mintmark_id
        )
    )

def read_mintmark(mintmark: MintmarkInfo):
    """读取刻印的具体类型"""
    mintmark_type = mintmark.WhichOneof('mintmark')
    
    if mintmark_type == 'skill':
        return mintmark.skill
    elif mintmark_type == 'ability':
        return mintmark.ability
    elif mintmark_type == 'universal':
        return mintmark.universal
    elif mintmark_type == 'quanxiao':
        return mintmark.quanxiao
    else:
        raise ValueError(f"未知的刻印类型: {mintmark_type}")
```

#### 2.2 抗性创建函数

**函数签名**：

```python
def create_state_resist(*items: tuple[int, int]) -> list[ResistanceInfo.StateItem]:
    """
    创建状态抗性列表
    
    参数：
        items: 元组 (state_id, percent)，表示状态 ID 和抗性百分比
    
    返回：
        ResistanceInfo.StateItem 列表
    """
    pass
```

**实现要点**：

- 接受可变数量的 `(state_id, percent)` 元组
- 返回 `ResistanceInfo.StateItem` 列表

**实现示例**：

```python
from seerbp.petcode.v1.message_pb2 import ResistanceInfo

def create_state_resist(*items: tuple[int, int]) -> list[ResistanceInfo.StateItem]:
    """创建状态抗性列表"""
    return [
        ResistanceInfo.StateItem(state_id=state_id, percent=percent)
        for state_id, percent in items
    ]
```

---

### 3. 效果类型识别模块

效果（Effect）通过 `status` 字段区分类型，SDK 应提供便捷的识别函数。

#### 3.1 效果类型枚举

**枚举定义**：

```python
from enum import IntEnum

class EffectType(IntEnum):
    """效果类型枚举"""
    NONE = 0        # 无效果
    GENERAL = 1     # 特性
    ITEM = 2        # 道具效果
    VARIATION = 4   # 异能特质
    SOULMARK = 5    # 魂印
    TEAM_TECH = 7   # 战队科技
    OTHER = 99      # 其他
```

#### 3.2 效果类型识别函数

**函数签名**：

```python
def get_effect_type(status: int) -> EffectType:
    """根据 status 值获取效果类型"""
    pass
```

**实现要点**：

- 根据 `status` 值返回对应的 `EffectType` 枚举
- 未知类型返回 `EffectType.OTHER`

**实现示例**：

```python
def get_effect_type(status: int) -> EffectType:
    """根据 status 值获取效果类型"""
    try:
        return EffectType(status)
    except ValueError:
        return EffectType.OTHER
```

#### 3.3 效果参数化表示（可选）

如果你的 SDK 需要与 API 交互，可以提供效果的参数化表示。

**数据类定义**：

```python
from dataclasses import dataclass

@dataclass
class EffectParam:
    """效果的参数化表示"""
    type: EffectType
    name: str  # 格式: "id_arg1_arg2_..."
```

**转换函数**：

```python
def effect_to_param(effect: PetInfo.Effect) -> EffectParam:
    """将 Effect 对象转换为 EffectParam"""
    effect_type = get_effect_type(effect.status)
    args_str = "_".join([str(effect.id)] + [str(arg) for arg in effect.args])
    return EffectParam(type=effect_type, name=args_str)

def param_to_effect(param: EffectParam) -> PetInfo.Effect:
    """将 EffectParam 转换为 Effect 对象"""
    parts = param.name.split("_")
    effect_id = int(parts[0])
    args = [int(x) for x in parts[1:]] if len(parts) > 1 else []
    return PetInfo.Effect(id=effect_id, status=param.type.value, args=args)
```

---

### 4. 功能总结

#### 必须实现的函数

| 模块 | 函数 |
| ------ | ------ |
| 序列化 | `to_binary()` |
| 序列化 | `from_binary()` |
| 序列化 | `to_base64()` |
| 序列化 | `from_base64()` |
| 序列化 | `to_dict()` / `to_object()` |
| 序列化 | `from_dict()` / `from_object()` |
| 辅助创建 | `create_skill_mintmark()` |
| 辅助创建 | `create_ability_mintmark()` |
| 辅助创建 | `create_universal_mintmark()` |
| 辅助创建 | `create_quanxiao_mintmark()` |
| 辅助创建 | `read_mintmark()` |
| 辅助创建 | `create_state_resist()` |
| 效果处理 | `get_effect_type()` |
| 效果处理 | `effect_to_param()` |
| 效果处理 | `param_to_effect()` |
| 弃用数据转换 | `convert_deprecated_data()` / `convertDeprecatedData()` |

> **弃用数据转换**：`convert_deprecated_data(message)` 将消息中已废弃的字段转换为新字段（原地修改并返回）。例如将 `PetInfo.extra_hp` 转换为 `PetAbilityBonus` 中一个全新的 `TYPE_BASEVALUE` 类型的体力加成项，不会与已有加成项合并。

---

## 开发流程示例

以下展示完整的 SDK 开发流程，。

### 1. 创建项目结构

```bash
# 创建项目目录
mkdir petcode-sdk-python
cd petcode-sdk-python

# 创建目录结构
mkdir -p petcode tests
touch petcode/__init__.py
touch petcode/create_and_read.py
touch petcode/effect.py
touch tests/...
```

### 2. 安装原生 SDK

```bash
# 安装原生 SDK
pip install seerbp-petcode-protocolbuffers-python --index-url https://buf.build/gen/python
```

### 3. 实现序列化模块

在 `petcode/__init__.py` 中实现：

```python
import base64
import gzip
from google.protobuf import json_format
from seerbp.petcode.v1.message_pb2 import PetCodeMessage

def to_binary(message: PetCodeMessage) -> bytes:
    """将消息序列化为二进制数据（内置 gzip 压缩）"""
    return gzip.compress(message.SerializeToString(), compresslevel=1)

def from_binary(data: bytes) -> PetCodeMessage:
    """将二进制数据解压缩并反序列化为消息"""
    return PetCodeMessage.FromString(gzip.decompress(data))

def to_base64(message: PetCodeMessage) -> str:
    """将消息序列化为 Base64 字符串"""
    return base64.b64encode(to_binary(message)).decode('utf-8')

def from_base64(data: str) -> PetCodeMessage:
    """将 Base64 字符串解码并反序列化为消息"""
    return from_binary(base64.b64decode(data))

def to_dict(message: PetCodeMessage) -> dict:
    """将消息转换为字典"""
    return json_format.MessageToDict(message)

def from_dict(data: dict) -> PetCodeMessage:
    """将字典反序列化为消息"""
    return json_format.ParseDict(data, PetCodeMessage())
```

### 4. 实现辅助创建模块

在 `petcode/create_and_read.py` 中实现刻印创建函数（代码见上文）。

### 5. 实现效果处理模块

在 `petcode/effect.py` 中实现效果类型识别（代码见上文）。

### 6. 编写测试

为所有函数编写测试代码

### 7. 配置打包

创建 `pyproject.toml`：

```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "petcode"
version = "1.0.0"
description = "PetCode SDK for Python"
requires-python = ">=3.10"
dependencies = [
    "seerbp-petcode-protocolbuffers-python"
]

[tool.setuptools.packages.find]
where = ["."]
include = ["petcode*"]
```

### 8. 测试和发布

```bash
# 运行测试
pytest

# 构建包
python -m build

# 发布到 PyPI
twine upload dist/*
```

### 9. 为 seer-pet-code 仓库提交 PR

1. 在 [seer-pet-code](https://github.com/nattsu39/seer-pet-code) 仓库中创建一个新分支
2. 将你的 SDK 代码复制到 `sdk/<language>/` 目录下
3. 提交 PR，等待审核

---

## 测试与发布

### 测试清单

开发完成后，请确保测试以下功能：

- ✅ **序列化往返**：`message -> to_base64() -> from_base64() -> message` 数据应保持一致
- ✅ **刻印创建**：使用辅助函数创建的刻印应能正确序列化和反序列化
- ✅ **抗性创建**：抗性列表应能正确创建
- ✅ **效果类型识别**：`get_effect_type()` 应正确识别所有效果类型
- ✅ **异常处理**：无效的 Base64 字符串、损坏的二进制数据应抛出明确的异常

### 文档要求

请确保提供 **README.md**，包含安装方式、快速开始、API 参考等必要信息。

### 发布到包管理器

- **Python**：发布到 PyPI
- **TypeScript**：发布到 npm
- **Go**：发布到 GitHub，使用 Go Modules
- **Java**：发布到 Maven Central

---

## 参考资源

- **Buf 官方文档**：<https://buf.build/docs>
- **BSR 使用指南**：<https://buf.build/docs/bsr/introduction>
- **Protobuf 官方文档**：<https://protobuf.dev>
- **PetCode 使用手册**：[docs/manual.md](manual.md)
- **Python SDK 源码**：[sdk/py/](../sdk/py/)
- **TypeScript SDK 源码**：[sdk/ts/](../sdk/ts/)
