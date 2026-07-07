# szdata 调度主题权限 / 申请管理只读参
> 面向后续 CLI / adapter / agent 的只读参考本文件只沉淢 2026-07-04 本轮观察结论；数量页面行为和接口字段均不写成永久事实
## 页面与环境边
- 目标页面：`https://data.gf.com.cn/portal/#/dataArchitecture/schedulingPermission/applyManage`
- 路由：`/dataArchitecture/schedulingPermission/applyManage`
- 页面标题：`调度主题权限申请 - 数据综合管理平台`
- 环境：`szdata` 生产环境，只允许只读查看、被network 观察、bundle 定向搜索、help/wiki 定向搜索- 本轮未执行保存提交修改删除授权取消授权审批撤回分配导入导出等权限修改动作
## 页面 UI 结论

页面位于顶部导航的更多菜单下，当前展弢到数据架构本轮在同一模块中确认到 3 个前端路由：

| 路由 | 前端 name | 标题 | 备注 |
|---|---|---|---|
| `schedulingPermission/rulesManage` | `schedulingPermissionRulesManage` | 调度主题权限规则 | 规则管理，未进入 |
| `schedulingPermission/applyManage` | `schedulingPermissionApplyManage` | 调度主题权限申请 | 本轮目标|
| `schedulingPermission/dataSource` | `schedulingPermissionDataSource` | 数据源权限申| 相邻页面，不外推结论 |

申请管理页本轮观察到的筛选项
- 申请单编号：`applyNo`
- 申请单：`name`
- 申请人：`applicant`
- 改人：`transformPeople`
- 审核状：`auditStatus`
- 授权状：`authorizeStatus`
- 改状态：`transformStatus`
- 回收状：`recycleStatus`

页面按钮与入口：

- 只读/查询类：`搜索`、`重置`、分页每页条数申请单名称详情入口、`流转记录`- 写风险入口：`新增`、`编辑`、`审核`、`授权`、`改`、`回收`、`关联信息修改`、弹窗内`确定` / `确认`。本轮未点击这些入口- `流转记录` `el-popover`，前端调用申请流转记录接口，展示处理人动作时间下丢步骤、意见等；本轮页面首屏多条记录显示暂无记录
列表列：

- 序号
- 申请单编- 申请- 申请- 改人
- 弢始时- 结束时间
- 审核状- 授权状- 改状- 回收状- 操作

本轮首屏默认分页10 页，观察到数4027 条03 页；这只是本轮生产页面观察
状枚举来自前bundle
| 字段 | | 展示 |
|---|---:|---|
| `auditStatus` | 1 | 审核|
| `auditStatus` | 2 | 自动通过 |
| `auditStatus` | 3 | 直接通过 |
| `auditStatus` | 4 | 有限通过 |
| `auditStatus` | 5 | 自动拒绝 |
| `auditStatus` | 6 | 人工拒绝 |
| `auditStatus` | 7 | 自动有限通过 |
| `authorizeStatus` | 1 | 待授|
| `authorizeStatus` | 2 | 拒绝授权 |
| `authorizeStatus` | 3 | 已授|
| `transformStatus` | 1 | 待改|
| `transformStatus` | 2 | 已改|
| `recycleStatus` | 1 | 待回|
| `recycleStatus` | 2 | 已回|

## URL / 路由解释

主路由为
```text
/dataArchitecture/schedulingPermission/applyManage
```

前端没有发现独立`detail` / `apply` / `edit` / `approve` / `auth` 子路由申请管理页通过 query 参数切换模式
| query | 含义 |
|---|---|
| `applyNo` | 申请单号，用于拉取指定申请单详情 |
| `type=4` | 审核模式，需 `haveAudit=true` 才打弢弹窗 |
| `type=6` | 授权模式，需 `haveAuthorize=true` 才打弢弹窗 |
| `type=8` | 改模式，霢 `haveTransform=true` 才打弢弹窗 |
| `type=10` | 回收模式，需 `haveRecycle=true` 才打弢弹窗 |
| `type=12` | 详情查看模式 |

已确认：`type` 只是前端弹窗模式，不应被当成权限事实。按钮是否显示由列表/详情返回`haveAudit`、`haveAuthorize`、`haveTransform`、`haveRecycle`、`haveEdit` 控制，这些字段代表当前登录用户在当前流程上的可操作入口，不等同于目标申请单最终有效权限
## 只读接口清单

### `POST /behaviourservice/scheduleThemeApply/page`

- 用：申请管理列表数据- 来源：打弢目标页自动调用；前端 `getList` 调用- 关键请求参数：`pageNo`、`pageSize`、`applyNo`、`name`、`applicant`、`transformPeople`、`auditStatus`、`authorizeStatus`、`transformStatus`、`recycleStatus`- 关键响应字段：`records`、`total`、`size`、`current`、`pages`- 单条记录关键字段：`id`、`uuid`、`applyNo`、`themeName`、`databaseName`、`applyReason`、`name`、`applicant`、`applyTime`、`endTime`、`auditPeople`、`auditStatus`、`auditTime`、`auditComments`、`authorizeStatus`、`authorizePeople`、`authorizeTime`、`transformPeople`、`transformStatus`、`recycleStatus`、`demandId`、`demandName`、`demandNumber`、`belongUserId`、`belongUserName`、`haveEdit`、`haveAudit`、`haveAuthorize`、`haveTransform`、`haveRecycle`、`validity`、`applyType`、`isSourceAlignedConsumption`- 是否代表实际权限：代表申请单和流程状态，不单独证明调度系统最终有效权限
### `POST /developservice/schedule/getScheduleTopicList.json`

- 用：调度主题候字典- 来源：打弢目标页自动调用- 关键请求参数：本轮未观察到有效业务参数- 关键响应字段：`topicName`、`topicDesc`、`userName`- 本轮观察：返913 个主题- 是否代表实际权限：不代表当前登录用户或目标申请人拥有这些主题权限；只是主题字候
### `POST /developservice/schedule/getScheduleTopicListByUser.json`（bundle 发现，非申请管理页自动请求）

- 用：公共调度任务配置代码中用于加载当前用户可用的调度主题”下拉- 来源：`dp.6b36573d.js` 定向搜索；调用点包括调度任务表单 `loadScheduleTopicList`、标签维宽表/任务对比等任务配置页靃69- 关键请求参数：可无业务参数调用；本轮在已登录页面上下文只`POST` 实测- 关键响应字段：`topicName`、`topicDesc`、`userName`- 本轮观察：当前登录用户返3 个主题；这是本轮账号/时间点观察，不写成永久事实- 是否代表实际权限：可能代表当前登录用户在调度任务配置场景可择的主题范围，但不支持按任意用角色/任务反查；也不能证明申请单最终生效状态
### `POST /developservice/schedule/getScheduleTopicUser.json`（bundle 发现，非申请管理页自动请求）

- 用：公共项目同步/构建配置中检查所选主题是否配置了主题用户；前端提示不能添加未配置主题用户的主题- 来源：`dp.6b36573d.js` 定向搜索- 关键请求参数：主题对象数组，例如 `[{"topicName":"DM_OTC_N"}]`；如果先查过主题字典，也可传完整主题对象- 关键响应字段：使用处读取 `topicName`、`userName` 并写`checkTopicMap`- 本轮观察：`DM_OTC_N` 返回主题用户 `gf_otc_n`- 是否代表实际权限：代表主题对应的主题用户配置；该主题用户是继续查询主题自Hive/Ranger 基础策略的入口，但本接口本身不返回完整权限
### `POST /external/execservice/ranger/getUserPoliciesByServiceNameAndUser`（bundle 调用点确认）

- 用：按主题用户读Ranger/Hive 策略摘要；前端在调度任务运行配置中用它决定某主题可库范围- 调用链：先用 `getScheduleTopicUser.json` `topicName` 取主题用户，再调用本接口- 关键请求参数：`user`，例`{"user":"gf_otc_n"}`- 关键响应字段：`database`、`table`- 本轮观察：`DM_OTC_N` 的主题用户为 `gf_otc_n`；`gf_otc_n` 返回 7 个基硢库4 个表名，基础库包`dm_otc_n`、`dm_otc_test` 等，不包`odata_n_rcc`；表名清单未命中 `u_etfcomponent_p`- 参数坑：`{"serviceName":"gfhive","userName":"gf_otc_n"}` 会返回处理出错；`{"serviceName":"gfhive","user":"gf_otc_n"}` 返回成功但空对象。前端真实调用点使用的是 `{"user":"主题用户"}`- 是否代表实际权限：这是主题自基础 Hive 权限的只读证据若目标库表不在该结果中，还霢要继续查申请管理授权记录；不能只凭基硢策略结果判定“绝对没有权限
### `POST /developservice/projectSpace/getTopicUser`（bundle 发现，非申请管理页自动请求）

- 用：项目空间/工作节点相关代码读取项目空间主题用户信息- 来源：`dp.6b36573d.js` 定向搜索；同丢模块还存Ranger 用户策略查询封装，但本轮未进入该页面、未调用- 关键请求参数：本轮仅从封装发现，未确认业务参数- 是否代表实际权限：可能是项目空间维度的主题用户辅助信息；不能直接作为调度主题权限通用查询结论
### `POST /behaviourservice/scheduleThemeApply/isOa`

- 用：判断当前登录账号 OA/人员类型相关标识- 来源：打弢目标页自动调用- 关键响应字段：`data`，本轮为 `1`- 是否代表实际权限：不代表调度主题权限，仅用于页面申请/接口人等逻辑
### `GET /portalservice/login/info.json?majorModuleIds=1-2`

- 用：读取当前登录用户、顶部菜单按钮权限等门户信息- 关键响应字段：`userId`、`userName`、`btnPerms`、`menuList`- 是否代表实际权限：只代表当前登录用户的门户菜按钮可见性，不代表某个申请单、某个目标用户角色或调度主题的最终权限
### `POST /permissionservice/permFunction/list.json`

- 用：全局功能/菜单权限目录- 关键响应字段：`permUuid`、`permName`、`permCode`、`permUrl`、`parentUuid`、`permType`、`majorModuleId`- 是否代表实际权限：不代表当前用户或目标对象实际拥有这些菜按钮；只是全屢目录
### `GET /behaviourservice/scheduleThemeApply/{applyNo}`

- 用：前端详情、审核授权改造回收弹窗都会先调用详情- 来源：前bundle `Kn(e)` 调用，调用点传入 `applyNo`- 已确path 参数：`applyNo`；数`id` `uuid` 不用- 关键字段：列表字+ `tableList`、`recordList`、`modelingList`、`demandList` 等详情结构- 本轮观察：`SQD2026060801` 详情`tableList` 返回 2 条，包含 `odata_n_rcc.u_etfcomponent_p`- 是否代表实际权限：详情字段仍以申请单流程为主。若 `auditStatus`、`authorizeStatus`、`transformStatus`、`recycleStatus` 等状态满足过/已授未回收，可作为申请授权补充证据
### `POST /behaviourservice/scheduleThemeApplyRecord/applyRecord`

- 用：流转记录- 来源：点`流转记录` 时调用- 关键请求参数：`applyId`- 关键响应字段：`processName`、`processAction`、`operator`、`operateTime`、`nextStep`、`nextUser`、`comments`- 是否代表实际权限：代表流程轨迹，不代表当前有效权限
### bundle 中发现但未调用的写风险接
以下接口来自前端 bundle，仅作为风险边界记录；本轮未调用
| 接口 | 风险 |
|---|---|
| `POST /behaviourservice/scheduleThemeApply/batchAdd` | 新增/批量新增申请 |
| `POST /behaviourservice/scheduleThemeApply/verify` | 校验申请 |
| `POST /behaviourservice/scheduleThemeApply/update` | 审核、授权改造回收等更新 |
| `POST /behaviourservice/scheduleThemeApply/edit` | 编辑/关联信息类更新风|
| `POST /behaviourservice/scheduleThemeApply/updateModeling` | 更新关联建模 |
| `POST /behaviourservice/scheduleThemeRule/create`、`update`、`delete` | 规则管理写操|

## 关键字段与数据结
申请单核心字段：

| 字段 | 含义 |
|---|---|
| `applyNo` | 申请单编号，`SQD...` |
| `name` | 申请单标题，通常为主题申请库/表相关权限|
| `themeName` | 申请的调度主|
| `databaseName` | 申请访问的数据源/库名；首屏样本多Hive/数据仓库库名 |
| `applyReason` | 申请原因 |
| `applicant` / `applicantId` | 申请人展示名 / 标识 |
| `applyTime` / `endTime` | 申请弢始时/ 流程结束时间 |
| `auditStatus` / `auditPeople` / `auditTime` / `auditComments` | 审核状与审核信息 |
| `authorizeStatus` / `authorizePeople` / `authorizeTime` / `authorizeCommets` | 授权状与授权信息 |
| `transformStatus` / `transformPeople` / `transformTime` / `transformCommets` | 改状态与改信|
| `recycleStatus` / `recyclePeople` / `recycleTime` / `recycleComments` | 回收状与回收信息 |
| `demandId` / `demandName` / `demandNumber` | 关联 IT 霢|
| `belongUserId` / `belongUserName` | 接口归属人员 |
| `tableList` | 详情中的申请库表明细；已确认`applyNo` 读取详情可拿到表级记录，`databaseName`、`tableName` |
| `recordList` | 详情中预期包含流程记录或相关记录 |
| `modelingList` | 关联建模任务 |
| `haveAudit` / `haveAuthorize` / `haveTransform` / `haveRecycle` / `haveEdit` | 当前登录用户对此申请单的可操作入|
| `validity` | 权限有效期结束时间；为空表示该接口未给出明确结束时间，不等同于永久有|
| `applyType` | 申请类型字段，首屏列表中为空；详情待复核 |
| `isSourceAlignedConsumption` | 是否贴源消费，前端详情展示为“是/-|

字段边界
- `themeName` 是调度主题，不是用户/角色- `databaseName` 是被申请访问的库/数据源范围，不是调度主题本身- `have*` 字段是当前登录用户能否操作当前流程节点，不是目标申请人或主题的权限- `auditStatus`、`authorizeStatus`、`transformStatus`、`recycleStatus` 是申请流程状态是否能推导为有效权限需要额外结合授权改造回收有效期和调度系统实际授权关系
## 调度主题权限模型总结

已确认事实：

- 前端申请管理围绕“申请单”展开，申请单把 `themeName`（调度主题）、`databaseName` / `tableList`（申请访问范围）、申请人、接口人、IT 需求建模任务和流程状态关联起来。
- wiki 中对调度权限的描述是“用户角色-主题”的关联关系，角色作为中介串联主题和用户。
- wiki 同时说明主题会关联主题用户与数据源：通过主题用户管控不同主题下任务能读写 Hive 库，通过主题关联数据源控制主题能读写不同 DB。
- 前端调度任务配置代码把“主题 -> 主题用户 -> Ranger/Hive 策略摘要”作为可选库判断链路：`getScheduleTopicUser.json` 返回主题用户，`getUserPoliciesByServiceNameAndUser` 返回该主题用户的基础 `database` / `table` 权限摘要。

基于证据的推断：

- 本页面更像调度主题消费权限申请单管理，不是最终的调度系统用户-角色-主题授权真相表。
- `authorizeStatus=3`（已授权）加上通过 `auditStatus`，只能说明申请流程中已进入授权完成口径；若还存在 `transformStatus=1`、`recycleStatus=2`、过期 `validity` / `applyEnd` 等情况，不能直接判定为可用权限。
- 申请管理页本身只发现“调度主题权限申请 / 申请管理”的页面、接口和前端代码；没有发现独立的“调度主题权限查询页面”或按任意用户、角色、任务反查的通用查询代码。
- 公共调度任务 bundle 另发 `getScheduleTopicListByUser.json`，可作为“当前登录用户可用调度主题下拉”的候选证据；它不是申请管理页接口，也不是通用权限判定接口。

未知/待确认：

- 详情接口已确认使用 `applyNo` 作为 path 参数。
- `tableList` 详情结构已按 `applyNo` 读取；表级 `applyBegin/applyEnd` 若返回则作为表级有效期，申请单顶层 `validity` 作为权限有效期结束时间。
- 当前已验证的调度申请详情样本没有返回独立的表级开始时间，默认用授权时间 `authorizeTime` 作为有效期开始证据。
- 申请单状态与 Horae/调度系统实际生效权限之间是否有异步延迟或人工改造环节，需要进一步核实。
- 若后续需要判断某主题是否能访问某库表，应优先查主题用户基础策略，再查申请管理授权记录补充；`getScheduleTopicListByUser.json` 只适合限定为“当前登录用户可选主题”证据，不能外推到任意对象。

## 库表权限判定链路

目标：输入 `topicName` + `db.table`，默认直接输出“该调度主题访问该库表是否有明确权限证据”的结论。本链路只做只读查询。

1. 解析主题
   - `getScheduleTopicList.json` 确认主题存在，拿 `topicName`、`topicDesc`。
   - 未找到主题：输出 `UNKNOWN`。
2. 查主题用户
   - 调用 `getScheduleTopicUser.json`，请求体为主题对象数组。
   - 读取返回 `userName`，例：`DM_OTC_N -> gf_otc_n`。
   - 没有主题用户：输出 `UNKNOWN` / `MAYBE`，并提示基础策略无法确认。
3. 查主题自带基础策略
   - 调用 `getUserPoliciesByServiceNameAndUser`，请求体 `{"user":"<themeUser>"}`。
   - 检查 `data.database` 是否包含目标库，或包含匹配 `*`。
   - 检查 `data.table` 是否包含目标表名；本轮观察该数组为表名列表，未带库名前缀，因此如果只命中表名但库未命中，应输出 `MAYBE`。
   - 库命中或明确表命中：输出 `BASE_PASS`。
4. 查申请授权补充
   - `scheduleThemeApply/page` 按申请单主题名进行有限搜索；当前接口 `themeName`、`databaseName` 参数可能不生效，实践中 `name=<topicName>`、`name=<databaseName>` 更可靠。
   - 对记录按 `themeName`、`databaseName` 在客户端二次过滤。
   - 对 `applyNo` 调 `scheduleThemeApply/{applyNo}`，读取 `tableList`。
   - `tableList` 命中目标 `db.table`，且记录满足 `authorizeStatus=3`、`recycleStatus!=2`、无待改造或 `transformStatus=0`，输出 `APPLY_PASS`。
5. 无命中
   - 基础策略和申请详情都未命中：输出 `NO`。
   - 任一接口失败、改造/回收状态无法判断：输出 `UNKNOWN` / `MAYBE`，不要硬判。
   - 若授权状态明确但有效期字段为空，可输出 `PASS`，但 `validity.endTime` 必须保留 `-`，不得冒充有结束时间。

建议状：

| 状| 含义 |
|---|---|
| `BASE_PASS` | 主题用户基础 Hive/Ranger 策略命中目标库或|
| `APPLY_PASS` | 申请管理详情 `tableList` 命中目标库表，且状显示已授权、未回收 |
| `MAYBE` | 有部分证据但无法确认继承、有效期、改造状态或表名归属 |
| `NO` | 主题、主题用户基硢策略和申请详情均可读，且均未命中 |
| `UNKNOWN` | 主题/主题用户/表元数据无法解析，或关键接口失败 |

### 示例：`DM_OTC_N` + `odata_n_rcc.u_etfcomponent_p`

本轮只读实测链路
- 主题字典：`DM_OTC_N` 存在，说明为“柜台交易市场部数据集市”- 主题用户：`getScheduleTopicUser.json` 返回 `gf_otc_n`- 基础策略：`getUserPoliciesByServiceNameAndUser {"user":"gf_otc_n"}` 返回基础7 个：`odata_n_ois`、`pdata_hk`、`spdata_nds`、`pdata_news_n`、`odata_n_tit`、`dm_otc_n`、`dm_otc_test`；不包含 `odata_n_rcc`。基硢34 个，未命`u_etfcomponent_p`- 申请授权：`scheduleThemeApply/page` 找到 `SQD2026060801`，主`DM_OTC_N`，库 `odata_n_rcc`，`auditStatus=3`、`authorizeStatus=3`、`transformStatus=0`、`recycleStatus=0`- 申请详情：`scheduleThemeApply/SQD2026060801` `tableList` 包含 `odata_n_rcc.u_etfcomponent_p`
结论：该例应输出 `APPLY_PASS`，不`BASE_PASS`。也就是说它不是 `DM_OTC_N` 自带基础权限，是申请授权补充命中
## Help / Wiki 有效信息摘要

平台 help 定向搜索结果
- 关键词：`调度主题权限`、`调度主题`、`主题权限`、`申请管理`、`调度权限`、`任务权限`、`主题授权`、`调度申请`、`数据架构`、`schedulingPermission`
- 本轮结果：均未找到有效说明
本地 wiki 定向搜索结果
- `大数据平台指引文.../_02_权限申请指引和流程模86667671.md`
  - 提到初次使用霢要过 IT 霢求进行主题权限和数据源权限申请  - “开通主题权限模板要求说明申请开通哪些主题的查看权限、项目任务管实例管理的增删改查权限- `大数据平台指引文.../_01_Horae FAQ/01环境信息及账号权限申204332884.md`
  - 生产环境账号及权限申请走 IT 霢求，霢要列出所霢主题权限  - 若需要新增主题，霢要在霢求单里提出并经治理组评估，确定新主题命名、所用用户和 Hive 库权限  - 正式员工/合作方员工需要先登录丢次系统同步账号信息，之后才能进行主题授权- `大数据平台指引文.../_01_Horae FAQ/调度的权限控制是怎样的？-205105659.md`
  - 明确“用角色-主题”的关联关系，角色作为中介串联主题和用户  - 不同角色有不同功能菜单权限和主题权限  - 主题关联主题用户以及数据源，用来控制主题下任务能读写Hive 库和 DB- `大数据平台指引文.../调度KyuubiPyspark任务使用指引-303379365.md`
  - 提到脚本配置任务中的“可使用的调度主题需要提前授权主题对脚本的使用和执行权限- `自研投资管理系统/.../大数据数据主题及权限说明-104137315.md`
  - 只找到主题与“数据主题权限归属示例，不能外推到当前数综申请管理页靃69
## CLI/adaptor 只读实现

只设计申请管理读命令，不设计保存、提交、授权、审批、改造、回收、编辑、导入、导出命令。不要设计“按任意用户/角色/任务做调度主题权限判定”的命令，除非后续另有明确的只读权限关系接口证据。可以单独保留“当前登录用户可选调度主题”的只读命令，但必须命名清楚，不能叫泛化的 check。

已实现核心命令：

| 命令 | 用途 | 证据来源 |
|---|---|---|
| `szdata_detail scheduling-topic-list-by-current-user` | 查看当前登录用户在调度任务配置中可选的主题 | `getScheduleTopicListByUser.json` |
| `scheduling-topic-base-policy` | 查看指定主题的主题用户和基础 Hive/Ranger 库表策略摘要 | `getScheduleTopicUser.json` + `getUserPoliciesByServiceNameAndUser` |
| `szdata table-permission-topic` | 判断指定主题访问指定库表的结论 | 先查基础策略，再查申请详情 `tableList` |

仍属于后续可选命令：

| 命令 | 用途 | 证据来源 |
|---|---|---|
| `scheduling-permission-apply-list` | 查询调度主题权限申请列表 | `scheduleThemeApply/page` |
| `scheduling-permission-apply-detail` | 查看申请详情 | `scheduleThemeApply/{applyNo}` |
| `scheduling-permission-apply-record` | 查看流转记录 | `scheduleThemeApplyRecord/applyRecord` |
| `scheduling-permission-topic-list` | 查看调度主题字典 | `getScheduleTopicList.json` |

建议参数
| 命令 | 参数 |
|---|---|
| `scheduling-topic-list-by-current-user` | 可`--keyword`、`--size` |
| `scheduling-permission-apply-list` | `--topic`、`--db`、`--applicant`、`--status`、`--page`、`--size` |
| `scheduling-permission-apply-detail` | `--apply-no` |
| `scheduling-topic-base-policy` | `--topic`，可`--show-tables`、`--limit` |
| `table-permission-topic` | `--topic DM_OTC_N --table odata_n_rcc.u_etfcomponent_p`；也支持 `--tables "db1.t1,db2.t2"`；加 `--detail` 展开完整证据 |

当前实际 CLI 参数
```powershell
opencli szdata_detail scheduling-topic-list-by-current-user -f json
opencli szdata_detail scheduling-topic-list-by-current-user --keyword "OTC" -f json

opencli szdata_detail scheduling-topic-base-policy --topic DM_OTC_N -f json
opencli szdata_detail scheduling-topic-base-policy --topic DM_OTC_N --show-tables true --limit 10 -f json

opencli szdata table-permission-topic --topic DM_OTC_N --table dm_otc_n.any_table -f json
opencli szdata table-permission-topic --topic DM_OTC_N --tables "dm_otc_n.any_table,odata_n_rcc.u_etfcomponent_p" -f json

opencli szdatatest_detail scheduling-topic-list-by-current-user --help
opencli szdatatest_detail scheduling-topic-base-policy --help
opencli szdatatest table-permission-topic --help
```

默认输出
- 主题列表：主题名、主题说明；默认分页/关键词过滤，不输出全量 913 条主题。
- 基础策略：主题、主题说明、主题用户、基础库数量和列表、基础表数量和分页摘要。
- 库表判定：单表默认输出拍平为 `topicName`、`themeUser`、`table`、`conclusion`、`matchedBy`、`matched`、轻量 `source`、`validity`。
- `conclusion` 只取 `PASS`、`EXPIRED`、`NO`、`UNKNOWN`，是 agent 首先读取的字段；`BASE_PASS`、`APPLY_PASS`、`EXPIRED`、`MAYBE` 等证据状态只在 `--detail` 中展开。
- 多表默认才保留紧凑 `results`。
- 有效期开始优先取表级 `applyBegin`，否则取授权时间 `authorizeTime`；有效期结束优先取表级 `applyEnd`，否则取申请单顶层 `validity`。
- 如果平台未返回明确结束时间，`validity.endTime` 输出 `-`，不冒充有效期。
- raw 输出必须分页、限字段，并默认脱敏用户标识，不输出 cookie、token、内部 IP、端口、网关细节。

实现边界
- `login/info`、`permFunction/list` 不能用于判断目标对象是否拥有调度主题权限。
- `getScheduleTopicList` 只能做主题字典，不代表权限。
- `getScheduleTopicListByUser` 可能代表当前登录用户可选主题，不能代表任意用户/角色/任务的权限关系。
- `getUserPoliciesByServiceNameAndUser` 可作为主题用户基础 Hive/Ranger 策略摘要证据。
- `scheduleThemeApply/page` 只能作为申请流程证据，不应默认提升为实际权限查询。
- 对库表判定建议默认输出 `conclusion`：`PASS`（基础策略或未过期的已授权申请命中）、`EXPIRED`（申请详情命中库表但权限有效期结束时间已过）、`NO`（基础策略和可读申请记录均未命中）、`UNKNOWN`（主题用户元数据无法解析）。
- `--detail` 再展开证据状态：`BASE_PASS`（基础策略命中）、`APPLY_PASS`（申请授权命中）、`EXPIRED`、`MAYBE`（存在库表级继承或字段不足）、`NO`、`UNKNOWN`。
- `NO` / `UNKNOWN` / `MAYBE` 不能自动等于业务不能开发或调度不能执行，只表示当前 CLI 证据没有确认覆盖，需要用户确认补充申请单证据或走权限申请流程。
- `scheduleThemeApply/page` 的 `themeName`、`databaseName` 入参本轮观察可能不生效；实现时要做客户端二次过滤，优先用 `name=<topicName>`、`name=<databaseName>` 缩小候选。
- `scheduleThemeApply/{applyNo}` 只能用申请单号，不能用 `id` 或 `uuid`。
## Evidence

- 日期026-07-04
- 来源  - 页面只读打开：`/dataArchitecture/schedulingPermission/applyManage`
  - network 被动观察：打弢页面自动请求列表、主题字典OA 标识、登录信息全屢功能目录
  - bundle 定向搜索：`tmp/scheduling-permission-readonly/7713.ccc9c060.js`、`tmp/scheduling-permission-readonly/dp.6b36573d.js`
  - help 定向搜索：`opencli szdata_detail portal-help --keyword ... --size 5 -f json`
  - wiki 定向搜索：`E:\03_resource\wiki-down` 下用户指定关键词
  - 追查“是否有查询接口”补充搜索：平台 help 查询类关键词、本wiki 查询类关键词、`szdata/szdatatest` adapter 源码、公共调度任bundle
  - 只读实测：在已登录页面上下文调用 `getScheduleTopicListByUser.json`，只记录响应形状、字段名和数量，不输出明细- 本轮观察数量  - 申请列表：默10 页，总数 4027 条03 页  - 调度主题字典13 个主题  - 当前登录用户可调度主题：`getScheduleTopicListByUser.json` 返回 3 个主题  - 全局功能目录52 个节点  - 登录信息按钮权限：当前登录用`btnPerms` 122 项  - 安全边界  - 未输cookie、token、内IP、端口网关细节  - 文档只保留业务字段和接口路径摘要  - 本次没有做任何权限修改
## 2026-07-06 audit addendum

Production `szdata` smoke sample:

```powershell
opencli szdata table-permission-topic --topic DM_OTC_N --table dm_otc_n.md_stock_daily_market -f json
```

Observed compact verdict fields: `topicName`, `topicDesc`, `themeUser`,
`table`, `conclusion`, `matchedBy`, `matched`, `source`, `validity`. The sample
returned `conclusion=PASS`, `matchedBy=baseDatabase`, and `matched=dm_otc_n`.
An earlier run in the same audit failed while probing the theme-user policy
endpoint and then succeeded on retry; treat that as transient interface/session
evidence, not as a permission verdict.
