param(
  [string]$BaseUrl = "https://data.gf.com.cn",
  [string]$OutputPath = "",
  [switch]$ListOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function New-Endpoint {
  param(
    [int]$No,
    [string]$Path,
    [string]$Use,
    [string]$Method = "POST",
    [string]$ContentType = "form",
    [string]$Body = "",
    [bool]$WritePath = $false
  )

  [pscustomobject]@{
    no = $No
    path = $Path
    use = $Use
    method = $Method
    contentType = $ContentType
    body = $Body
    writePath = $WritePath
  }
}

function Get-BearerToken {
  if (-not [string]::IsNullOrWhiteSpace($env:SZDATA_BEARER_TOKEN)) {
    return $env:SZDATA_BEARER_TOKEN.Trim()
  }

  $secure = Read-Host -AsSecureString "Bearer token (input hidden; not saved)"
  $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
  try {
    return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
  } finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
  }
}

function Read-ErrorBody {
  param($Response)

  if ($null -eq $Response) { return "" }
  try {
    $reader = New-Object System.IO.StreamReader($Response.GetResponseStream())
    return $reader.ReadToEnd()
  } catch {
    return ""
  }
}

function Select-JsonMessage {
  param([string]$Body)

  if (-not $Body) { return @("", "") }
  try {
    $json = $Body | ConvertFrom-Json
    $code = ""
    $msg = ""
    if ($null -ne $json.PSObject.Properties["code"]) { $code = [string]$json.code }
    foreach ($name in @("msg", "message", "error")) {
      $property = $json.PSObject.Properties[$name]
      if ($property -and $property.Value) {
        $msg = [string]$property.Value
        break
      }
    }
    return @($code, $msg)
  } catch {
    $text = ($Body -replace "\s+", " ").Trim()
    if ($text.Length -gt 160) { $text = $text.Substring(0, 160) }
    return @("", $text)
  }
}

function Get-AccessClass {
  param(
    [object]$Status,
    [string]$AppCode,
    [string]$Message
  )

  if ($Status -eq "ERR") { return "ERROR" }
  if ($Status -eq 401 -or $Status -eq 403) { return "NO_AUTH" }
  if ($AppCode -match "^(401|403|100401|100403)$") { return "NO_AUTH" }
  if ($Message -match "未登录|登录|认证|鉴权|授权|权限|Unauthorized|Forbidden|token|Token") {
    return "NO_AUTH"
  }
  if ($Status -eq 200) { return "AUTH_PASSED_BUSINESS_ERROR" }
  return "UNKNOWN"
}

$endpoints = @(
  New-Endpoint 1 "/portal/prod-api/metaservice/metadataSearch/searchByEs" "metadata search" "POST" "form" "content=%E5%AE%A2%E6%88%B7&type=003000&pageNo=1&pageSize=1&status=1&tempShow=0&highLight=0&searchWayType=0&extraDatabaseId=&classifications="
  New-Endpoint 2 "/portal/prod-api/metaservice/metadataSearch/getTableByGuid" "table detail by guid" "POST" "json" '{"guid":""}'
  New-Endpoint 3 "/portal/prod-api/metaservice/metadataSearch/getTableDDL" "table DDL" "POST" "json" '{"guid":""}'
  New-Endpoint 4 "/portal/prod-api/metaservice/metadataSearch/getHoraeSqlByTaskId" "Horae task SQL" "POST" "json" '{"horaeTaskId":"238523"}'
  New-Endpoint 5 "/portal/prod-api/metaservice/metaTableSampleData/hive" "Hive table sample data" "POST" "form" "clusterId=19fc4a91c21111ecb8b21866daf1650c&guid=&qualifiedName=dm_otc_n.md_stock_daily_market"
  New-Endpoint 6 "/govern/prod-api/metaservice/lineage/getLineageInfo.json" "table lineage" "POST" "json" '{"guid":"","centerGuid":"","depth":"2"}'
  New-Endpoint 7 "/govern/prod-api/metaservice/lineage/getGuidByApiCode.json" "API code to guid" "POST" "json" '{"apiCode":""}'
  New-Endpoint 8 "/portal/prod-api/metaservice/businessSystem/queryReviewed.json" "reviewed business system candidates" "POST" "form" "keyword="

  New-Endpoint 9 "/portal/prod-api/developservice/schedule/getScheduleDetailTimeFormatted.json" "schedule task detail / DispatchTaskConfig detail" "POST" "form" "schedulingId=238523"
  New-Endpoint 10 "/portal/prod-api/developservice/schedule/getScheduleDetailTimeFormatted.json" "schedule upstream dependency from tasklink" "POST" "form" "schedulingId=238523"
  New-Endpoint 11 "/portal/prod-api/developservice/schedule/getScheduleTopicList.json" "schedule topic dictionary" "POST" "form" ""
  New-Endpoint 12 "/portal/prod-api/developservice/schedule/getScheduleTopicListByUser.json" "current user's selectable schedule topics" "POST" "form" ""
  New-Endpoint 13 "/portal/prod-api/developservice/schedule/getScheduleTopicUser.json" "schedule topic users" "POST" "json" '[{"topicName":"DM_OTC_N","topicDesc":""}]'
  New-Endpoint 14 "/portal/prod-api/external/execservice/ranger/getUserPoliciesByServiceNameAndUser" "topic user's base table policies" "POST" "json" '{"user":"gf_otc_n"}'
  New-Endpoint 15 "/portal/prod-api/developservice/schedule/getTaskLabelList.json" "task label dictionary" "POST" "form" ""
  New-Endpoint 16 "/portal/prod-api/developservice/schedule/getScheduleTypeList.json" "schedule type dictionary" "POST" "form" ""

  New-Endpoint 17 "/portal/prod-api/behaviourservice/scheduleThemeApply/page" "schedule theme permission apply list" "POST" "form" "pageNo=1&pageSize=1&current=1&size=1&applyNo=&name=DM_OTC_N&applicant=&transformPeople=&auditStatus=&authorizeStatus=&transformStatus=&recycleStatus="
  New-Endpoint 18 "/portal/prod-api/behaviourservice/scheduleThemeApply/SQD2026060801" "schedule theme permission apply detail" "GET" "" ""
  New-Endpoint 19 "/portal/prod-api/behaviourservice/scheduleThemeApplyRecord/applyRecord" "schedule theme permission apply records" "POST" "form" "applyNo=SQD2026060801"
  New-Endpoint 20 "/portal/prod-api/behaviourservice/scheduleThemeApply/isOa" "schedule theme OA check" "POST" "form" ""

  New-Endpoint 21 "/portal/prod-api/developservice/wideTable/list" "wide table list" "POST" "form" "pageNum=1&pageSize=1"
  New-Endpoint 22 "/portal/prod-api/developservice/dataSetConfig/wideTableGeneration/detail" "wide table generation detail" "POST" "form" "uuid=d1635793ca55332a3854308be6c2d0c1"
  New-Endpoint 23 "/portal/prod-api/developservice/wideTable/getLocalSchedulingConfig.json" "wide table local schedule config readback" "POST" "form" "wideTableUuid=d1635793ca55332a3854308be6c2d0c1"
  New-Endpoint 24 "/portal/prod-api/developservice/wideTable/getUpgradeSchedulingConfig.json" "wide table upgrade schedule config readback" "POST" "form" "wideTableUuid=d1635793ca55332a3854308be6c2d0c1"
  New-Endpoint 25 "/portal/prod-api/developservice/horaeUpgradeApply/getWideTableSql" "generate wide table schedule SQL" "POST" "form" "dataSetConfigId=&databaseName=dm_otc_n&tableName=md_stock_daily_market"
  New-Endpoint 26 "/portal/prod-api/developservice/wideTable/getIndicatorTaskIdList.json" "wide table upstream task link" "POST" "form" "dataSetConfigId="
  New-Endpoint 27 "/portal/prod-api/developservice/wideTable/listActionLog" "wide table action log" "POST" "form" "uuid=d1635793ca55332a3854308be6c2d0c1&pageNum=1&pageSize=1"

  New-Endpoint 28 "/portal/prod-api/developservice/projectSpace/workNode/schedule/listTaskInstance" "project-space schedule task instance list" "POST" "form" "taskId=238523&pageNum=1&pageSize=1"
  New-Endpoint 29 "/portal/prod-api/developservice/projectSpace/workNode/schedule/getTaskConfigRunResult" "schedule config run result" "POST" "form" "taskId=238523"
  New-Endpoint 30 "/portal/prod-api/developservice/projectSpace/workNode/schedule/getTask" "project-space schedule task config" "POST" "form" "taskId=238523"
  New-Endpoint 31 "/portal/prod-api/developservice/projectSpace/workNode/schedule/getTaskVersionList.json" "schedule task version list" "POST" "form" "taskId=238523"
  New-Endpoint 32 "/portal/prod-api/developservice/projectSpace/workNode/schedule/getVersionCompareInfo.json" "schedule task version diff" "POST" "form" "taskId=238523"
  New-Endpoint 33 "/portal/prod-api/developservice/schedule/waitOfflineTaskPage.json" "pending offline schedule task list" "POST" "form" "pageNo=1&pageSize=1"
  New-Endpoint 34 "/portal/prod-api/developservice/schedule/fetchWaitOfflineTaskChangeLog.json" "pending offline schedule task change log" "POST" "form" "schedulingId=238523"
  New-Endpoint 35 "/portal/prod-api/developservice/schedule/getDateAfterNBusinessDays.json" "date after N business days" "POST" "form" "n=1"
  New-Endpoint 36 "/portal/prod-api/developservice/horaeFailedTask/page.json" "Horae failed task list" "POST" "form" "pageNo=1&pageSize=1"
  New-Endpoint 37 "/portal/prod-api/graphservice/taskLoopDetection/getAllLinkByStartAndEnd.json" "task link / loop detection" "POST" "form" "startTaskId=238523&endTaskId=238523"
  New-Endpoint 38 "/portal/prod-api/quartzservice/sysTask" "Quartz task" "POST" "form" "pageNo=1&pageSize=1"
  New-Endpoint 39 "/portal/prod-api/quartzservice/sysTaskLog" "Quartz task log" "POST" "form" "pageNo=1&pageSize=1"

  New-Endpoint 40 "/portal/prod-api/developservice/wideTable/saveOrUpdateLocalSchedule.json" "save wide table schedule config" "POST" "form" "" $true
  New-Endpoint 41 "/portal/prod-api/developservice/horaeUpgradeApply/commitUpgradeApply.json" "commit wide table upgrade apply" "POST" "form" "" $true
  New-Endpoint 42 "/portal/prod-api/developservice/wideTable/applyUpgrade.json" "apply wide table upgrade" "POST" "form" "" $true
  New-Endpoint 43 "/portal/prod-api/developservice/schedule/waitOfflineTaskSubmit.json" "submit pending offline task" "POST" "form" "" $true
  New-Endpoint 44 "/portal/prod-api/developservice/projectSpace/workNode/schedule/freezeTask.json" "freeze schedule task" "POST" "form" "" $true
  New-Endpoint 45 "/portal/prod-api/developservice/projectSpace/workNode/schedule/submitOffline.json" "submit schedule offline" "POST" "form" "" $true
  New-Endpoint 46 "/portal/prod-api/developservice/projectSpace/workNode/schedule/updateConfigRunResult.json" "update schedule config run result" "POST" "form" "" $true
  New-Endpoint 47 "/portal/prod-api/behaviourservice/scheduleThemeApply/batchAdd" "add schedule theme permission apply" "POST" "form" "" $true
  New-Endpoint 48 "/portal/prod-api/behaviourservice/scheduleThemeApply/verify" "verify schedule theme permission apply" "POST" "form" "" $true
  New-Endpoint 49 "/portal/prod-api/behaviourservice/scheduleThemeApply/update" "update / audit / authorize schedule theme permission apply" "POST" "form" "" $true
  New-Endpoint 50 "/portal/prod-api/behaviourservice/scheduleThemeApply/edit" "edit schedule theme permission apply" "POST" "form" "" $true
  New-Endpoint 51 "/portal/prod-api/behaviourservice/scheduleThemeApply/updateModeling" "update linked modeling" "POST" "form" "" $true
  New-Endpoint 52 "/portal/prod-api/behaviourservice/scheduleThemeRule/create" "create schedule theme rule" "POST" "form" "" $true
  New-Endpoint 53 "/portal/prod-api/behaviourservice/scheduleThemeRule/update" "update schedule theme rule" "POST" "form" "" $true
  New-Endpoint 54 "/portal/prod-api/behaviourservice/scheduleThemeRule/delete" "delete schedule theme rule" "POST" "form" "" $true
)

if ($ListOnly) {
  $endpoints | Select-Object no, path, use, method, writePath | ConvertTo-Json -Depth 4
  exit 0
}

$token = Get-BearerToken
if ($token -match "^Bearer\s+") {
  $token = ($token -replace "^Bearer\s+", "").Trim()
}
if (-not $token) {
  throw "Bearer token is empty."
}

$headers = @{
  Authorization = "Bearer $token"
  Accept = "application/json, text/plain, */*"
}

$results = @()
foreach ($endpoint in $endpoints) {
  if ($endpoint.writePath) {
    $results += [pscustomobject]@{
      no = $endpoint.no
      path = $endpoint.path
      use = $endpoint.use
      method = $endpoint.method
      bearerAccess = "NOT_TESTED_WRITE_PATH"
      httpStatus = "-"
      appCode = "-"
      message = "state-changing path skipped by design"
    }
    continue
  }

  $status = "ERR"
  $body = ""
  $errMessage = ""
  try {
    $request = @{
      Uri = ($BaseUrl.TrimEnd("/") + $endpoint.path)
      Method = $endpoint.method
      Headers = $headers
      TimeoutSec = 15
      UseBasicParsing = $true
      ErrorAction = "Stop"
    }
    if ($endpoint.method -ne "GET") {
      $request.Body = $endpoint.body
      if ($endpoint.contentType -eq "json") {
        $request.ContentType = "application/json;charset=UTF-8"
      } else {
        $request.ContentType = "application/x-www-form-urlencoded;charset=utf-8"
      }
    }
    $response = Invoke-WebRequest @request
    $status = [int]$response.StatusCode
    $body = [string]$response.Content
  } catch {
    $errMessage = $_.Exception.Message
    if ($_.Exception.Response) {
      $status = [int]$_.Exception.Response.StatusCode.value__
      $body = Read-ErrorBody $_.Exception.Response
    }
  }

  $parts = Select-JsonMessage $body
  $appCode = $parts[0]
  $message = $parts[1]
  if (-not $message -and $errMessage) { $message = $errMessage }
  $access = Get-AccessClass $status $appCode $message

  $results += [pscustomobject]@{
    no = $endpoint.no
    path = $endpoint.path
    use = $endpoint.use
    method = $endpoint.method
    bearerAccess = $access
    httpStatus = $status
    appCode = $appCode
    message = $message
  }
}

if ($OutputPath) {
  $dir = Split-Path -Parent $OutputPath
  if ($dir -and -not (Test-Path $dir)) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
  }
  $results | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 -Path $OutputPath
}

$results | ConvertTo-Json -Depth 5

$token = $null
