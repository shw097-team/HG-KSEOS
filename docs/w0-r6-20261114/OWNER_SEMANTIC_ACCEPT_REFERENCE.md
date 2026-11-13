# OWNER_SEMANTIC_ACCEPT 回執參考（2026-11-14）

**這一頁不是第二份規範**，只是把「業主已簽」這件事接到被簽的兩個檔案上。被簽的兩個檔案**位元組未變**（見下方 digest），本頁是新增檔，不影響簽章效力。

## 1. 簽了什麼

| 欄 | 值 |
|---|---|
| act | `OWNER_SEMANTIC_ACCEPT`（Route A：業主以自身身分接受交付的語義內容） |
| window | `WIN-4d8a83d39e8f`（task `FHS-W0-W1ENTRY-20261114`，scope 僅 `owner_semantic_accept`，effect ceiling `REPOSITORY_WRITE`） |
| 口令 | 由業主於 2026-11-14T00:38:44 在遮罩 tkinter 視窗自行輸入；未落盤、未進 log、未經任何 argv |
| owner fingerprint | `412b351937be72a1` |
| 被簽 body | `SIGN_BODY_CANDIDATE.json`，4,341 B，payload `sha256 2afe1ad7b9e3a60dd2209157f56d3944d110e78e21ac9c8c4ce1a7d8229feb46` |
| 簽章 | ed25519，128 hex；獨立以 `owner_public_hex` 重驗 **OK**（見 §4） |
| 回執 | `SIGN_BODY_CANDIDATE.SIGNED.json`（同目錄） |
| ops | 1／2（視窗另 1 次額度未使用，簽後即收窗） |

## 2. 被簽的兩個檔案（digest 即 body 內所載，未變）

| 檔案 | bytes | sha256 |
|---|---:|---|
| `FHS_PIPD-LS-PKG_W0_vNEXT_2026-11-14_r1_實質正文.md` | 21791 | `c4617197f47bb2c2437b9340b4cffda740369bf7c4796f1aba3a6166a8656d7f` |
| `FHS_PIPD-LS-PKG_W0_vNEXT_2026-11-14_r1_證據型附錄.md` | 17289 | `5de9a02a2f6f500fcb40a1fc9d107b70d72511dcd868eef70adaf64373f7843a` |

**若日後任何一個檔案被修訂，本次簽章不再涵蓋新位元組**，須以新候選重簽；這是設計，不是缺陷。

## 3. 這一簽的效力邊界

**是**：業主對這兩份交付之語義內容的接受（`OWNER_SEMANTIC_ACCEPT`），可用於解除「作者端交付無人接受」這一項的懸置。

**不是**（body 內 `not_claimed` 已明列）：
- 不是 `ORIGINAL_ACK`（原域 Reader 的核簽仍缺）
- 不是 Native 准入（無 WorkID／Grant／WorldRaw）
- 不是 Independent PASS（無不同技術 Principal 的 Checker verdict）
- 不是 `RELEASE_GRANTED`、不是 Canonical promotion、不是 W1 Repo 已建立

原域 HOLD 一項未解：`H-READER`、`H-H16`、`H-ENTRY`、`H-POS02-ORIGIN`、`H-GUARD-EPOCH`、`H-MANDATE-PLAN-VERIFY`、`H-USAGE-EXECUTE`。

## 4. 任何人可重驗（不需金鑰）

```bash
PY="C:/Users/user/AppData/Local/hermes/cache/scratch/fhs_next/venv311/Scripts/python.exe"
"$PY" - <<'PY'
import json,hashlib,pathlib
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
base=pathlib.Path(r"C:/Projects/Agent_Workspace/FHS_NEXT_Workspace/W0_R6_OWNER_PREAUTH_20261114")
body=(base/"SIGN_BODY_CANDIDATE.json").read_bytes()
r=json.load(open(base/"SIGN_BODY_CANDIDATE.SIGNED.json",encoding="utf-8"))
print("payload_ok", hashlib.sha256(body).hexdigest()==r["payload_sha256"])
pk=Ed25519PublicKey.from_public_bytes(bytes.fromhex(r["owner_public_hex"]))
pk.verify(bytes.fromhex(r["signature_hex"]), body)
print("signature_ok True")
PY
```

`owner_public_hex`（`d42c654cd1afba80…`）在回執內、也在 `owner_envelope/design/OWNER_ENROLLMENT.json`；兩者一致才算通過。

## 5. 推送

同一分支 `w0-r6-20261114`（`shw097-team/HG-KSEOS`，PR #25）：本頁、`SIGN_BODY_CANDIDATE.json`、`SIGN_BODY_CANDIDATE.SIGNED.json` 與更新後的 `DELIVERY.json`。**未合併 `main`**。
