# Protocol 文档

> 该文档使用 [protoc-gen-doc](https://github.com/pseudomuto/protoc-gen-doc/) 生成

<a name="top"></a>

## 目录

- [petcode/v1/message.proto](#petcode_v1_message-proto)
    - [MintmarkInfo](#petcode-v1-MintmarkInfo)
    - [MintmarkInfo.Ability](#petcode-v1-MintmarkInfo-Ability)
    - [MintmarkInfo.Quanxiao](#petcode-v1-MintmarkInfo-Quanxiao)
    - [MintmarkInfo.Skill](#petcode-v1-MintmarkInfo-Skill)
    - [MintmarkInfo.Universal](#petcode-v1-MintmarkInfo-Universal)
    - [MintmarkInfo.Universal.GemItem](#petcode-v1-MintmarkInfo-Universal-GemItem)
    - [PetAbilityBonus](#petcode-v1-PetAbilityBonus)
    - [PetAbilityBonus.ExtraValue](#petcode-v1-PetAbilityBonus-ExtraValue)
    - [PetAbilityBonus.Value](#petcode-v1-PetAbilityBonus-Value)
    - [PetAbilityValue](#petcode-v1-PetAbilityValue)
    - [PetCodeMessage](#petcode-v1-PetCodeMessage)
    - [PetCodeMessage.SeerSet](#petcode-v1-PetCodeMessage-SeerSet)
    - [PetInfo](#petcode-v1-PetInfo)
    - [PetInfo.Effect](#petcode-v1-PetInfo-Effect)
    - [ResistanceInfo](#petcode-v1-ResistanceInfo)
    - [ResistanceInfo.Hurt](#petcode-v1-ResistanceInfo-Hurt)
    - [ResistanceInfo.StateItem](#petcode-v1-ResistanceInfo-StateItem)
  
    - [PetAbilityBonus.Type](#petcode-v1-PetAbilityBonus-Type)
    - [PetCodeMessage.DisplayMode](#petcode-v1-PetCodeMessage-DisplayMode)
    - [PetCodeMessage.Server](#petcode-v1-PetCodeMessage-Server)
  
- [标量值类型](#scalar-value-types)



<a name="petcode_v1_message-proto"></a>
<p align="right"><a href="#top">回到顶部</a></p>

## petcode/v1/message.proto



<a name="petcode-v1-MintmarkInfo"></a>

### MintmarkInfo
精灵刻印信息


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| mintmark.skill | [MintmarkInfo.Skill](#petcode-v1-MintmarkInfo-Skill) | [oneof](https://developers.google.com/protocol-buffers/docs/proto3#oneof) |  |
| mintmark.ability | [MintmarkInfo.Ability](#petcode-v1-MintmarkInfo-Ability) | [oneof](https://developers.google.com/protocol-buffers/docs/proto3#oneof) |  |
| mintmark.universal | [MintmarkInfo.Universal](#petcode-v1-MintmarkInfo-Universal) | [oneof](https://developers.google.com/protocol-buffers/docs/proto3#oneof) |  |
| mintmark.quanxiao | [MintmarkInfo.Quanxiao](#petcode-v1-MintmarkInfo-Quanxiao) | [oneof](https://developers.google.com/protocol-buffers/docs/proto3#oneof) |  |






<a name="petcode-v1-MintmarkInfo-Ability"></a>

### MintmarkInfo.Ability
能力刻印信息


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [int32](#int32) |  | 能力刻印ID |






<a name="petcode-v1-MintmarkInfo-Quanxiao"></a>

### MintmarkInfo.Quanxiao
全效刻印信息


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [int32](#int32) |  | 能力刻印ID |
| skill_mintmark_id | [int32](#int32) |  | 技能刻印ID |






<a name="petcode-v1-MintmarkInfo-Skill"></a>

### MintmarkInfo.Skill
技能刻印信息


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [int32](#int32) |  | 技能刻印ID |






<a name="petcode-v1-MintmarkInfo-Universal"></a>

### MintmarkInfo.Universal
全能刻印信息


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [int32](#int32) |  | 刻印ID |
| level | [int32](#int32) |  | 刻印等级 |
| ability | [PetAbilityValue](#petcode-v1-PetAbilityValue) | optional | 自定义刻印能力值，当该刻印数值与当前等级对应的数据不一致时需要设置该字段 （例如使用旧版刻印升级系统升级过的刻印具有随机数值） |
| gem | [MintmarkInfo.Universal.GemItem](#petcode-v1-MintmarkInfo-Universal-GemItem) | optional | 宝石信息 |






<a name="petcode-v1-MintmarkInfo-Universal-GemItem"></a>

### MintmarkInfo.Universal.GemItem
刻印宝石信息


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| gem_id | [int32](#int32) |  | 刻印宝石ID |
| bind_skill_id | [int32](#int32) |  | 宝石绑定的技能ID |






<a name="petcode-v1-PetAbilityBonus"></a>

### PetAbilityBonus
精灵额外加成项，例如战队加成，年费加成等


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [PetAbilityBonus.Type](#petcode-v1-PetAbilityBonus-Type) |  | 能力加成类型 |
| value | [PetAbilityBonus.Value](#petcode-v1-PetAbilityBonus-Value) |  | 能力加成详情 |






<a name="petcode-v1-PetAbilityBonus-ExtraValue"></a>

### PetAbilityBonus.ExtraValue



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [int32](#int32) | optional | 固定加成数值 |
| percent | [int32](#int32) | optional | 百分比加成数值 |






<a name="petcode-v1-PetAbilityBonus-Value"></a>

### PetAbilityBonus.Value



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| hp | [PetAbilityBonus.ExtraValue](#petcode-v1-PetAbilityBonus-ExtraValue) |  | 体力值加成 |
| attack | [PetAbilityBonus.ExtraValue](#petcode-v1-PetAbilityBonus-ExtraValue) |  | 攻击值加成 |
| defense | [PetAbilityBonus.ExtraValue](#petcode-v1-PetAbilityBonus-ExtraValue) |  | 防御值加成 |
| special_attack | [PetAbilityBonus.ExtraValue](#petcode-v1-PetAbilityBonus-ExtraValue) |  | 特攻值加成 |
| special_defense | [PetAbilityBonus.ExtraValue](#petcode-v1-PetAbilityBonus-ExtraValue) |  | 特防值加成 |
| speed | [PetAbilityBonus.ExtraValue](#petcode-v1-PetAbilityBonus-ExtraValue) |  | 速度值加成 |






<a name="petcode-v1-PetAbilityValue"></a>

### PetAbilityValue
精灵六项数值对象


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| hp | [int32](#int32) |  | 体力值 |
| attack | [int32](#int32) |  | 攻击值 |
| defense | [int32](#int32) |  | 防御值 |
| special_attack | [int32](#int32) |  | 特攻值 |
| special_defense | [int32](#int32) |  | 特防值 |
| speed | [int32](#int32) |  | 速度值 |






<a name="petcode-v1-PetCodeMessage"></a>

### PetCodeMessage



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| server | [PetCodeMessage.Server](#petcode-v1-PetCodeMessage-Server) |  | 服务器标记，用于指示接收方需要使用的数据源 |
| display_mode | [PetCodeMessage.DisplayMode](#petcode-v1-PetCodeMessage-DisplayMode) |  | 信息展示模式，用于指示接收方应该如何展示精灵信息 |
| seer_set | [PetCodeMessage.SeerSet](#petcode-v1-PetCodeMessage-SeerSet) |  | 套装和称号信息 |
| pets | [PetInfo](#petcode-v1-PetInfo) | repeated | 精灵信息列表 |






<a name="petcode-v1-PetCodeMessage-SeerSet"></a>

### PetCodeMessage.SeerSet



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| equips | [int32](#int32) | repeated |  |
| title_id | [int32](#int32) |  |  |






<a name="petcode-v1-PetInfo"></a>

### PetInfo



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [int32](#int32) |  | 精灵ID |
| level | [int32](#int32) |  | 精灵等级 |
| dv | [int32](#int32) |  | 精灵个体值 |
| nature | [int32](#int32) |  | 精灵性格 |
| evs | [PetAbilityValue](#petcode-v1-PetAbilityValue) |  | 精灵学习力 |
| skills | [int32](#int32) | repeated | 精灵携带的技能 |
| extra_hp | [int32](#int32) |  | 精灵额外体力 |
| effects | [PetInfo.Effect](#petcode-v1-PetInfo-Effect) | repeated | 精灵特效列表，根据effectInfo.status字段区分不同类型（特性/异能特质/魂印）的特效。<br> （在游戏内，这些特效都存放在同一个effectInfo数组中，这里采用相同的设计以确保游戏数据包和工具的双重兼容性） |
| mintmarks | [MintmarkInfo](#petcode-v1-MintmarkInfo) | repeated | 精灵装备的刻印 |
| resistance | [ResistanceInfo](#petcode-v1-ResistanceInfo) | optional | 精灵的抗性信息 |
| is_awaken | [bool](#bool) |  | 精灵是否神谕觉醒 |
| pet_items | [int32](#int32) | repeated | 精灵携带的战斗道具id列表 |
| ability_bonus | [PetAbilityBonus](#petcode-v1-PetAbilityBonus) | repeated | 精灵的额外能力值加成详情 |
| ability_total | [PetAbilityValue](#petcode-v1-PetAbilityValue) |  | 精灵的能力值总和 |
| skin_id | [int32](#int32) | optional | 精灵携带的皮肤ID |






<a name="petcode-v1-PetInfo-Effect"></a>

### PetInfo.Effect
精灵特效通用模型


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [int32](#int32) |  |  |
| status | [int32](#int32) |  |  |
| args | [int32](#int32) | repeated |  |






<a name="petcode-v1-ResistanceInfo"></a>

### ResistanceInfo



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| hurt | [ResistanceInfo.Hurt](#petcode-v1-ResistanceInfo-Hurt) |  |  |
| ctl | [ResistanceInfo.StateItem](#petcode-v1-ResistanceInfo-StateItem) | repeated |  |
| weak | [ResistanceInfo.StateItem](#petcode-v1-ResistanceInfo-StateItem) | repeated |  |






<a name="petcode-v1-ResistanceInfo-Hurt"></a>

### ResistanceInfo.Hurt



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| crit | [int32](#int32) |  |  |
| regular | [int32](#int32) |  |  |
| precent | [int32](#int32) |  |  |






<a name="petcode-v1-ResistanceInfo-StateItem"></a>

### ResistanceInfo.StateItem



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| state_id | [int32](#int32) |  |  |
| percent | [int32](#int32) |  |  |





 <!-- end messages -->


<a name="petcode-v1-PetAbilityBonus-Type"></a>

### PetAbilityBonus.Type
精灵额外能力值类型

| Name | Number | Description |
| ---- | ------ | ----------- |
| TYPE_UNSPECIFIED | 0 |  |
| TYPE_TEAM_TECH | 1 | 战队加成 |
| TYPE_ANNUAL_VIP | 2 | 年费加成 |
| TYPE_SUPER_NONO | 3 | 超能加成 |
| TYPE_SOULMARK | 4 | 魂印加成 |
| TYPE_AWAKEN | 5 | 神谕觉醒 |
| TYPE_SPECIAL | 6 | 特殊加成 |
| TYPE_OTHER | 99 | 其他 |



<a name="petcode-v1-PetCodeMessage-DisplayMode"></a>

### PetCodeMessage.DisplayMode
信息展示模式，用于指示接收方应该如何展示精灵信息

| Name | Number | Description |
| ---- | ------ | ----------- |
| DISPLAY_MODE_UNSPECIFIED | 0 |  |
| DISPLAY_MODE_PVP | 1 | PVP模式 |
| DISPLAY_MODE_PVE | 2 | PVE模式 |
| DISPLAY_MODE_BOSS | 3 | BOSS模式 |



<a name="petcode-v1-PetCodeMessage-Server"></a>

### PetCodeMessage.Server
服务器标记，用于指示接收方需要使用的数据源

| Name | Number | Description |
| ---- | ------ | ----------- |
| SERVER_UNSPECIFIED | 0 |  |
| SERVER_OFFICIAL | 1 | 官方服 |
| SERVER_TEST | 2 | 测试服 |
| SERVER_TAIWAN | 3 | 台服 |
| SERVER_CLASSIC | 4 | 经典服 |


 <!-- end enums -->

 <!-- end HasExtensions -->

 <!-- end services -->



## 标量值类型

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |

