# Protocol 文档

> 该文档使用 [protoc-gen-doc](https://github.com/pseudomuto/protoc-gen-doc/) 生成

<a name="top"></a>

## 目录

- [seerbp/petcode/v1/message.proto](#seerbp_petcode_v1_message-proto)
    - [MintmarkInfo](#seerbp-petcode-v1-MintmarkInfo)
    - [MintmarkInfo.Ability](#seerbp-petcode-v1-MintmarkInfo-Ability)
    - [MintmarkInfo.Quanxiao](#seerbp-petcode-v1-MintmarkInfo-Quanxiao)
    - [MintmarkInfo.Skill](#seerbp-petcode-v1-MintmarkInfo-Skill)
    - [MintmarkInfo.Universal](#seerbp-petcode-v1-MintmarkInfo-Universal)
    - [MintmarkInfo.Universal.GemItem](#seerbp-petcode-v1-MintmarkInfo-Universal-GemItem)
    - [PetAbilityBonus](#seerbp-petcode-v1-PetAbilityBonus)
    - [PetAbilityBonus.ExtraValue](#seerbp-petcode-v1-PetAbilityBonus-ExtraValue)
    - [PetAbilityBonus.Value](#seerbp-petcode-v1-PetAbilityBonus-Value)
    - [PetAbilityValue](#seerbp-petcode-v1-PetAbilityValue)
    - [PetCodeMessage](#seerbp-petcode-v1-PetCodeMessage)
    - [PetCodeMessage.SeerSet](#seerbp-petcode-v1-PetCodeMessage-SeerSet)
    - [PetInfo](#seerbp-petcode-v1-PetInfo)
    - [PetInfo.Effect](#seerbp-petcode-v1-PetInfo-Effect)
    - [ResistanceInfo](#seerbp-petcode-v1-ResistanceInfo)
    - [ResistanceInfo.Hurt](#seerbp-petcode-v1-ResistanceInfo-Hurt)
    - [ResistanceInfo.StateItem](#seerbp-petcode-v1-ResistanceInfo-StateItem)
  
    - [PetAbilityBonus.Type](#seerbp-petcode-v1-PetAbilityBonus-Type)
    - [PetCodeMessage.DisplayMode](#seerbp-petcode-v1-PetCodeMessage-DisplayMode)
    - [PetCodeMessage.Server](#seerbp-petcode-v1-PetCodeMessage-Server)
  
- [seerbp/petcode/server/v1/service.proto](#seerbp_petcode_server_v1_service-proto)
    - [DecodePetCodeMessageFromBase64Request](#seerbp-petcode-server-v1-DecodePetCodeMessageFromBase64Request)
    - [DecodePetCodeMessageFromBase64Response](#seerbp-petcode-server-v1-DecodePetCodeMessageFromBase64Response)
    - [EncodePetCodeMessageToBase64Request](#seerbp-petcode-server-v1-EncodePetCodeMessageToBase64Request)
    - [EncodePetCodeMessageToBase64Response](#seerbp-petcode-server-v1-EncodePetCodeMessageToBase64Response)
  
    - [PetCodeService](#seerbp-petcode-server-v1-PetCodeService)
  
- [标量值类型](#scalar-value-types)



<a name="seerbp_petcode_v1_message-proto"></a>
<p align="right"><a href="#top">回到顶部</a></p>

## seerbp/petcode/v1/message.proto



<a name="seerbp-petcode-v1-MintmarkInfo"></a>

### MintmarkInfo
精灵刻印信息


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| mintmark.skill | [MintmarkInfo.Skill](#seerbp-petcode-v1-MintmarkInfo-Skill) | [oneof](https://developers.google.com/protocol-buffers/docs/proto3#oneof) |  |
| mintmark.ability | [MintmarkInfo.Ability](#seerbp-petcode-v1-MintmarkInfo-Ability) | [oneof](https://developers.google.com/protocol-buffers/docs/proto3#oneof) |  |
| mintmark.universal | [MintmarkInfo.Universal](#seerbp-petcode-v1-MintmarkInfo-Universal) | [oneof](https://developers.google.com/protocol-buffers/docs/proto3#oneof) |  |
| mintmark.quanxiao | [MintmarkInfo.Quanxiao](#seerbp-petcode-v1-MintmarkInfo-Quanxiao) | [oneof](https://developers.google.com/protocol-buffers/docs/proto3#oneof) |  |






<a name="seerbp-petcode-v1-MintmarkInfo-Ability"></a>

### MintmarkInfo.Ability
能力刻印信息


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [int32](#int32) |  | 能力刻印ID |






<a name="seerbp-petcode-v1-MintmarkInfo-Quanxiao"></a>

### MintmarkInfo.Quanxiao
全效刻印信息


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [int32](#int32) |  | 能力刻印ID |
| skill_mintmark_id | [int32](#int32) |  | 技能刻印ID |






<a name="seerbp-petcode-v1-MintmarkInfo-Skill"></a>

### MintmarkInfo.Skill
技能刻印信息


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [int32](#int32) |  | 技能刻印ID |






<a name="seerbp-petcode-v1-MintmarkInfo-Universal"></a>

### MintmarkInfo.Universal
全能刻印信息


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [int32](#int32) |  | 刻印ID |
| level | [int32](#int32) |  | 刻印等级 |
| ability | [PetAbilityValue](#seerbp-petcode-v1-PetAbilityValue) | optional | 自定义刻印能力值，当该刻印数值与当前等级对应的数据不一致时需要设置该字段 （例如使用旧版刻印升级系统升级过的刻印具有随机数值） |
| gem | [MintmarkInfo.Universal.GemItem](#seerbp-petcode-v1-MintmarkInfo-Universal-GemItem) | optional | 宝石信息 |






<a name="seerbp-petcode-v1-MintmarkInfo-Universal-GemItem"></a>

### MintmarkInfo.Universal.GemItem
刻印宝石信息


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| gem_id | [int32](#int32) |  | 刻印宝石ID |
| bind_skill_id | [int32](#int32) |  | 宝石绑定的技能ID |






<a name="seerbp-petcode-v1-PetAbilityBonus"></a>

### PetAbilityBonus
精灵额外加成项，例如战队加成，年费加成等


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [PetAbilityBonus.Type](#seerbp-petcode-v1-PetAbilityBonus-Type) |  | 能力加成类型 |
| value | [PetAbilityBonus.Value](#seerbp-petcode-v1-PetAbilityBonus-Value) |  | 能力加成详情 |






<a name="seerbp-petcode-v1-PetAbilityBonus-ExtraValue"></a>

### PetAbilityBonus.ExtraValue



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [int32](#int32) | optional | 固定加成数值 |
| percent | [int32](#int32) | optional | 百分比加成数值 |






<a name="seerbp-petcode-v1-PetAbilityBonus-Value"></a>

### PetAbilityBonus.Value



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| hp | [PetAbilityBonus.ExtraValue](#seerbp-petcode-v1-PetAbilityBonus-ExtraValue) |  | 体力值加成 |
| attack | [PetAbilityBonus.ExtraValue](#seerbp-petcode-v1-PetAbilityBonus-ExtraValue) |  | 攻击值加成 |
| defense | [PetAbilityBonus.ExtraValue](#seerbp-petcode-v1-PetAbilityBonus-ExtraValue) |  | 防御值加成 |
| special_attack | [PetAbilityBonus.ExtraValue](#seerbp-petcode-v1-PetAbilityBonus-ExtraValue) |  | 特攻值加成 |
| special_defense | [PetAbilityBonus.ExtraValue](#seerbp-petcode-v1-PetAbilityBonus-ExtraValue) |  | 特防值加成 |
| speed | [PetAbilityBonus.ExtraValue](#seerbp-petcode-v1-PetAbilityBonus-ExtraValue) |  | 速度值加成 |






<a name="seerbp-petcode-v1-PetAbilityValue"></a>

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






<a name="seerbp-petcode-v1-PetCodeMessage"></a>

### PetCodeMessage



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| server | [PetCodeMessage.Server](#seerbp-petcode-v1-PetCodeMessage-Server) |  | 服务器标记，用于指示接收方需要使用的数据源 |
| display_mode | [PetCodeMessage.DisplayMode](#seerbp-petcode-v1-PetCodeMessage-DisplayMode) |  | 信息展示模式，用于指示接收方应该如何展示精灵信息 |
| seer_set | [PetCodeMessage.SeerSet](#seerbp-petcode-v1-PetCodeMessage-SeerSet) |  | 套装和称号信息 |
| pets | [PetInfo](#seerbp-petcode-v1-PetInfo) | repeated | 精灵信息列表 |






<a name="seerbp-petcode-v1-PetCodeMessage-SeerSet"></a>

### PetCodeMessage.SeerSet



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| equips | [int32](#int32) | repeated | 装备部件ID列表 |
| title_id | [int32](#int32) |  | 称号ID，对应游戏配置文件`achievements`中的`spe_name_bonus`字段 |






<a name="seerbp-petcode-v1-PetInfo"></a>

### PetInfo



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [int32](#int32) |  | 精灵ID |
| level | [int32](#int32) |  | 精灵等级 |
| dv | [int32](#int32) |  | 精灵个体值 |
| nature | [int32](#int32) |  | 精灵性格 |
| evs | [PetAbilityValue](#seerbp-petcode-v1-PetAbilityValue) |  | 精灵学习力 |
| skills | [int32](#int32) | repeated | 精灵携带的技能 |
| extra_hp | [int32](#int32) |  | 精灵额外体力上限 |
| effects | [PetInfo.Effect](#seerbp-petcode-v1-PetInfo-Effect) | repeated | 精灵特效列表，根据effectInfo.status字段区分不同类型（特性/异能特质/魂印）的特效。<br> （在游戏内，这些特效都存放在同一个effectInfo数组中，这里采用相同的设计以确保游戏数据包和工具的双重兼容性） |
| mintmarks | [MintmarkInfo](#seerbp-petcode-v1-MintmarkInfo) | repeated | 精灵装备的刻印 |
| resistance | [ResistanceInfo](#seerbp-petcode-v1-ResistanceInfo) | optional | 精灵的抗性信息 |
| is_awaken | [bool](#bool) |  | 精灵是否神谕觉醒 |
| pet_items | [int32](#int32) | repeated | 精灵携带的战斗道具id列表 |
| ability_bonus | [PetAbilityBonus](#seerbp-petcode-v1-PetAbilityBonus) | repeated | 精灵的额外能力值加成详情 |
| ability_total | [PetAbilityValue](#seerbp-petcode-v1-PetAbilityValue) |  | 精灵的能力值总和 |
| skin_id | [int32](#int32) | optional | 精灵携带的皮肤ID |






<a name="seerbp-petcode-v1-PetInfo-Effect"></a>

### PetInfo.Effect
精灵特效通用模型


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [int32](#int32) |  | 特效ID，对应游戏内配置的 eid/effect_id 字段（该字段不能为soulmark id或effect idx） |
| status | [int32](#int32) |  | 特效类型 |
| args | [int32](#int32) | repeated | 特效参数 |






<a name="seerbp-petcode-v1-ResistanceInfo"></a>

### ResistanceInfo



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| hurt | [ResistanceInfo.Hurt](#seerbp-petcode-v1-ResistanceInfo-Hurt) |  | 伤害抗性信息 |
| ctl | [ResistanceInfo.StateItem](#seerbp-petcode-v1-ResistanceInfo-StateItem) | repeated | 控制类状态抗性列表 |
| weak | [ResistanceInfo.StateItem](#seerbp-petcode-v1-ResistanceInfo-StateItem) | repeated | 弱化类状态抗性列表 |






<a name="seerbp-petcode-v1-ResistanceInfo-Hurt"></a>

### ResistanceInfo.Hurt
伤害抗性


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| crit | [int32](#int32) |  | 暴击抗性的百分比加成值，例如点满抗性后，抗性值为35%，则该字段值为35 |
| regular | [int32](#int32) |  | 固定伤害的百分比加成值，例如点满抗性后，抗性值为35%，则该字段值为35 |
| precent | [int32](#int32) |  | 百分比伤害的百分比加成值，例如点满抗性后，抗性值为35%，则该字段值为35 |






<a name="seerbp-petcode-v1-ResistanceInfo-StateItem"></a>

### ResistanceInfo.StateItem
状态抗性


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| state_id | [int32](#int32) |  | 状态ID |
| percent | [int32](#int32) |  | 状态抗性的百分比加成值（包含全免的5%）， 例如点满抗性+拥有全免抗性后，抗性值为55%，则该字段值为55 |





 <!-- end messages -->


<a name="seerbp-petcode-v1-PetAbilityBonus-Type"></a>

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



<a name="seerbp-petcode-v1-PetCodeMessage-DisplayMode"></a>

### PetCodeMessage.DisplayMode
信息展示模式，用于指示接收方应该如何展示精灵信息

| Name | Number | Description |
| ---- | ------ | ----------- |
| DISPLAY_MODE_UNSPECIFIED | 0 |  |
| DISPLAY_MODE_PVP | 1 | PVP模式 |
| DISPLAY_MODE_PVE | 2 | PVE模式 |
| DISPLAY_MODE_BOSS | 3 | BOSS模式 |



<a name="seerbp-petcode-v1-PetCodeMessage-Server"></a>

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



<a name="seerbp_petcode_server_v1_service-proto"></a>
<p align="right"><a href="#top">回到顶部</a></p>

## seerbp/petcode/server/v1/service.proto



<a name="seerbp-petcode-server-v1-DecodePetCodeMessageFromBase64Request"></a>

### DecodePetCodeMessageFromBase64Request



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| base64 | [string](#string) |  |  |






<a name="seerbp-petcode-server-v1-DecodePetCodeMessageFromBase64Response"></a>

### DecodePetCodeMessageFromBase64Response



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| pet_code_message | [seerbp.petcode.v1.PetCodeMessage](#seerbp-petcode-v1-PetCodeMessage) |  |  |






<a name="seerbp-petcode-server-v1-EncodePetCodeMessageToBase64Request"></a>

### EncodePetCodeMessageToBase64Request



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| pet_code_message | [seerbp.petcode.v1.PetCodeMessage](#seerbp-petcode-v1-PetCodeMessage) |  |  |






<a name="seerbp-petcode-server-v1-EncodePetCodeMessageToBase64Response"></a>

### EncodePetCodeMessageToBase64Response



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| base64 | [string](#string) |  |  |





 <!-- end messages -->

 <!-- end enums -->

 <!-- end HasExtensions -->


<a name="seerbp-petcode-server-v1-PetCodeService"></a>

### PetCodeService


| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| EncodePetCodeMessageToBase64 | [EncodePetCodeMessageToBase64Request](#seerbp-petcode-server-v1-EncodePetCodeMessageToBase64Request) | [EncodePetCodeMessageToBase64Response](#seerbp-petcode-server-v1-EncodePetCodeMessageToBase64Response) |  |
| DecodePetCodeMessageFromBase64 | [DecodePetCodeMessageFromBase64Request](#seerbp-petcode-server-v1-DecodePetCodeMessageFromBase64Request) | [DecodePetCodeMessageFromBase64Response](#seerbp-petcode-server-v1-DecodePetCodeMessageFromBase64Response) |  |

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

