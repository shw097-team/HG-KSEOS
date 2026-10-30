# FHS-MSC｜PIPD → Hermes 最小施工交接

**本輪目標：PIPD_CONSTRUCTION_HANDOFF_READY。** 僅表示下列無效果首工作與接收契約已具備作者端靜態接收證據；最後封包讀回記錄另列。Native=NATIVE_NOT_RUN；Independent Checker=NOT_RUN；Release=NOT_RUN。

普通 Goal：「依 WP-FHS-15 讀既有來源和已知答案，於允許的隔離草稿區產生三 SPEC；ProviderOff=true；只作 SOURCE_READ/LOCAL_DRAFT。」

先讀 [首工作接收契約](FIRST_WORK_RECEIVER_CONTRACT.md)，再讀 [TaskSpecSeed](02_FIRST_WORK/TaskSpecSeed.json)、[原 PIPD 功能 PI](02_FIRST_WORK/PI-PKG.json)、[PD 晚綁接收](02_FIRST_WORK/PD_LATE_BIND_RECEIVER_CONTRACT.json)、[原 Reader ACK](03_HANDOFF_EVIDENCE/PIPD_FUNCTIONAL_PI_READER_ACK.json)。三 SPEC真產物在 [Product](02_FIRST_WORK/RUN/ProductSPEC.json)、[Architecture](02_FIRST_WORK/RUN/ArchitectureSPEC.json)、[Program](02_FIRST_WORK/RUN/ProgramSPEC.json)。

首工作：原 WP-FHS-15；24真功能源句→24Atom，不是上輪44條ID/FirstFail投影。原 WP00/01資料讀入與Profile author決定現在可做；原 WP05 Compiler服務無須等待未來WP15 Native receipt。35項最小檢查通過，含5個原受影測試。

Hermes沿原普通Goal/PLAN入口讀取此契約與KnownAnswer；對source/draft不再問已授權文稿問題。真正Canonical WorkOrder或效果前，接原Fabric/HGK受權Receiver；使用原WorkID與Hermes task_id關聯、原Lease/Journal，UNKNOWN先世界Reconcile，不新建Queue或Issuer。需Owner/Native證據者只隔離受影live子圖：[具名差額與恢復條件](03_HANDOFF_EVIDENCE/GAPS_CLASSIFICATION_AND_RESUME.json)。

17冊完整正文與14 SBL升級內容均保留；[有效Reader](03_HANDOFF_EVIDENCE/CURRENT_READER_MAP.json) 原ID不改。7649筆全產品語義修補、485技術資格與282Runner/W18等未宣稱完成，留在原WP：[餘項分派](02_FIRST_WORK/REMAINING_REQUIREMENTS_ORIGINAL_WP_ASSIGNMENT.json)。前版FIRST_AUTHOR_FAILURE仍是全產品差額，不能反向阻斷本輪已接收的必要閉包。

正文與證據ZIP解壓至同一目錄；版本與SHA Manifest位於交付根。全部修補後各封裝一次。
