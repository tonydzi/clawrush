> Public mirror; local skill remains the deployment source. Built for Anton's fleet — adapt paths/names to your setup.
> Source SHA256: `08cd79f12de1ce42c07bd141785085f859f20d1205927911dfdef918ac5c02f3`.
> Export transformations: normalized line endings; machine hostname replaced with “original Windows host”.
> Maintainer: https://github.com/tonydzi

# Windows: старый Claude AppX Job держит запуск

Читать при `0x80070020` и свежем событии AppModel-Runtime 215/208 с `converting the job`. Это условная ветка `claude-repair`, не автоматический очиститель процессов. Портируемость: только Windows MSIX. Рельса: локальный PowerShell/WinAPI, без LLM и сети.

## 1. Установить конкретный контейнер

В `Microsoft-Windows-AppModel-Runtime/Admin` сопоставить события для **той же версии и GUID**: 210 — создан контейнер, 211 — добавлен процесс, 217 — уничтожен. Отсутствие 217 в ограниченном окне журнала — только кандидат, пока само существование Job не подтверждено.

Имена пользовательского Job имеют вид `\Container_<PackageFullName>-<UserSID>`, служебного — `\Container_<PackageFullName>-PackagedService`. Использовать фактические `ContainerName` из XML событий, данные пакета и SID целевого пользователя. Старой версии может уже не быть в `Get-AppxPackage`: взять её из событий. При необходимости перечислить корень NT Object Manager через `NtOpenDirectoryObject`/`NtQueryDirectoryObject`, отфильтровать тип `Job` и имена `Container_Claude_`.

Нужен **пользовательский старый Job**, а не текущий `PackagedService`. Не подставлять PID, SID или версию из прецедента. `IsProcessInJob=True` без handle именно этого Job не доказывает связь. Отсутствие package identity у процесса её не опровергает.

## 2. Прочитать PID-list, не меняя Job

Ниже проверенная форма read-only запроса: `JOB_OBJECT_QUERY=4`, `JobObjectBasicProcessIdList=3`. Выполнять на Windows в PowerShell; функция не завершает процессы, не меняет службы и не пишет файлы. `JobName` передать из шага 1.

```powershell
if (-not ('ClaudeReadOnlyJob' -as [type])) {
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class ClaudeReadOnlyJob {
 [StructLayout(LayoutKind.Sequential)] struct US { public ushort Length; public ushort MaximumLength; public IntPtr Buffer; }
 [StructLayout(LayoutKind.Sequential)] struct OA { public int Length; public IntPtr RootDirectory; public IntPtr ObjectName; public uint Attributes; public IntPtr SecurityDescriptor; public IntPtr SecurityQualityOfService; }
 [DllImport("ntdll.dll")] static extern uint NtOpenJobObject(out IntPtr h, uint access, ref OA oa);
 [DllImport("kernel32.dll", SetLastError=true)] static extern bool QueryInformationJobObject(IntPtr job, int cls, IntPtr info, uint size, out uint returned);
 [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr h);
 public static long[] Query(string name) {
  if (String.IsNullOrWhiteSpace(name)) throw new ArgumentException("Job name is required");
  IntPtr buf=Marshal.StringToHGlobalUni(name);
  US us=new US { Length=(ushort)(name.Length*2), MaximumLength=(ushort)((name.Length+1)*2), Buffer=buf };
  IntPtr usp=Marshal.AllocHGlobal(Marshal.SizeOf(typeof(US)));
  Marshal.StructureToPtr(us,usp,false);
  OA oa=new OA { Length=Marshal.SizeOf(typeof(OA)), ObjectName=usp, Attributes=0x40 };
  IntPtr h;
  uint status;
  try { status=NtOpenJobObject(out h,4,ref oa); }
  finally { Marshal.FreeHGlobal(usp); Marshal.FreeHGlobal(buf); }
  if(status!=0) throw new Exception("NtOpenJobObject status 0x"+status.ToString("X8"));
  IntPtr b=IntPtr.Zero;
  try {
   b=Marshal.AllocHGlobal(1048576);
   uint ret;
   if(!QueryInformationJobObject(h,3,b,1048576,out ret)) throw new Exception("QueryInformationJobObject error "+Marshal.GetLastWin32Error());
   int assigned=Marshal.ReadInt32(b,0), count=Marshal.ReadInt32(b,4);
   if(count!=assigned || count<0 || count>(1048576-8)/IntPtr.Size) throw new Exception("Incomplete or invalid PID list: assigned="+assigned+", count="+count);
   long[] pids=new long[count];
   for(int i=0;i<count;i++) pids[i]=Marshal.ReadIntPtr(b,8+i*IntPtr.Size).ToInt64();
   return pids;
  } finally { if(b!=IntPtr.Zero) Marshal.FreeHGlobal(b); CloseHandle(h); }
 }
}
'@
}
function Read-ClaudeContainer {
 param([Parameter(Mandatory=$true)][string]$JobName)
 $taskPids=@([ClaudeReadOnlyJob]::Query($JobName))
 foreach ($taskPid in $taskPids) {
  $p=Get-CimInstance Win32_Process -Filter ('ProcessId='+$taskPid)
  [pscustomobject]@{
   ProcessId=$taskPid
   ParentProcessId=$(if ($p) { $p.ParentProcessId } else { $null })
   Name=$(if ($p) { $p.Name } else { $null })
   CreationDate=$(if ($p) { $p.CreationDate } else { $null })
   ExecutablePath=$(if ($p) { $p.ExecutablePath } else { $null })
   State=$(if ($p) { 'Present' } else { 'Exited before lookup' })
  }
 }
}
```

`0xC0000022` = доступ запрещён, **не пустой Job**. Повысить права только у этого запроса; проверить минимальный скрипт до запуска. Если для UAC действительно нужны руки пользователя, назвать именно этот блок. `0xC0000034` = такого имени нет на момент проверки; сверить имя и namespace, не делать вывод «все контейнеры чисты». Пустой PID-list тоже не доказывает отсутствия Job: повторно проверить его существование и удерживающие handles.

## 3. Оценить последствия до остановки

Для каждого участника сохранить локально имя, PID, время создания, родителя, команду и рабочую папку, если доступна. Команды могут содержать секреты, не прикладывать их к публичному отчёту. Отдельно установить, что делает процесс: поиск, авторизация, сервер, WSL-приложение или действующая задача.

Функция выше намеренно не печатает командные строки. Получить их отдельно через `Get-CimInstance Win32_Process -Filter ('ProcessId='+$taskPid)` и свойство `CommandLine`, сохранив только в приватную улику. CIM не предоставляет рабочую папку процесса: искать её в исходном launcher/task/config; если источник не найден, отметить UNKNOWN и не выдумывать команду восстановления.

Членство в Job не делает процесс ненужным. Для действующего сервера/WSL сохранить способ его восстановления и потребителя. Разрешение перезапустить Claude не является разрешением уничтожить чужие данные, остановить всю WSL или произвольную инфраструктуру. Если необходимая остановка выходит за подтверждённый объём, подготовить точный список и спросить только про этот риск.

Старый список устаревает: перед остановкой повторно прочитать тот же Job и сверить **PID + время создания + имя**. Исчезнувший процесс пропустить; переиспользованный PID не трогать. Завершать только подтверждённых участников в согласованном объёме. Не использовать массовые `Stop-Process -Name python`, `taskkill /IM claude.exe /T` или `wsl --shutdown`.

## 4. Доказать результат и восстановить потребителей

1. Проверить исчезновение именно старого Job или событие 217 с его GUID после остановки. Если он остался, заново перечислить участников; не повторять убийство старых PID.
2. Активировать зарегистрированное приложение. Нужны новое событие 201, окно в пользовательской сессии и `Responding`, затем свежий UI/renderer/boot в актуальном логе. Повторная активация — отдельная проверка, не ещё одно принудительное закрытие.
3. Восстановить необходимые вспомогательные процессы **вне старого контейнера** и проверить их потребителей. Для HTTP мало открытого порта: проверить процесс/рабочую папку и ожидаемый ответ; для WSL — нужный дистрибутив и приложение. Недоступная проверка остаётся UNKNOWN.
4. В отчёте разделить: восстановлен запуск / прерваны такие задачи / такие потребители восстановлены / это не проверено. Не обещать устранение дефекта обновлятора: этот runbook освобождает конкретный старый контейнер.

## Улики и границы прецедента

05.10.2026 запрос старого Job вернул 11 процессов. Завершение подтверждённых участников сопровождалось 217 в 17:34:47 +01 и успешным 201 в 17:34:56; затем окно Responding и повторная активация. Два отдельно живших Claude Code процесса в этом Job отсутствовали и не затронуты. Причинный механизм доказан для группы, один виновник не выделен.

В числе участников были WSL-приложение, три HTTP-сервера, ожидание авторизации и поисковая цепочка. Их нельзя всех называть зависшими; восстановление этих потребителей в том ремонте не было доказано. Отсутствие `CodeIntegrity.cat` и необходимость обновления пакета не доказаны как причина/обязательное лечение первоначального отказа.

Возможно связанные внешние сообщения: [issue 91763](https://github.com/anthropics/claude-code/issues/91763), [issue 93220](https://github.com/anthropics/claude-code/issues/93220). Они не заменяют локальную проверку Job; чужие PID и команды не применять к своей машине.
