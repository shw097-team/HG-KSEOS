# 憑證輪替與 GitHub App 設定 — 操作指引與教學

> 對象：owner（唯一能執行其中四步的人）。
> 目的：把「PAT 橋接」整合進「GitHub App 自動輪替」的單一路徑，並讓長時間無人值守的大型任務**零人工介入**。
> 前提事實：**GitHub 沒有 API** 可以註冊 App、下載私鑰、完成安裝同意，或讀取／更新 PAT 的到期日。這四件事**只能**在瀏覽器做。本指引其餘部分全部自動化。

---

## 0. 先講清楚：為什麼不是「把 PAT 換掉」就好

PAT 有兩個結構性問題，都不是設定問題：

1. **它會自己到期，而且沒有 API 可以問它什麼時候到期。** 所以任何「到期前自動輪替」的排程**做不到**——你無法在不看 UI 的情況下知道剩幾天。
2. **它是長期憑證。** 一個能寫 repo 的 PAT 一旦洩漏，在到期前一直是活的。

GitHub App installation token 則相反：**TTL 1 小時、用完即棄、由本機私鑰現簽現換**。私鑰在磁碟上，token 從不落盤。所以真正的答案是：**App 是終點，PAT 只是橋接**。

```
現在：  PAT（長期，人工輪替，無到期 API）────────┐
                                                  ├─→ cred_broker.py ─→ git push
目標：  App private key ─→ RS256 JWT ─→ installation token（1h，自動）┘
```

`cred_broker.py` **兩條路都實作了**：有 `HGK_APP_KEY` 就走 App（`mint_app_installation_token()`，`POST /app/installations/{id}/access_tokens`）；沒有才回退 PAT。所以**你可以先只做 App，PAT 原封不動當備援**——不必先刪掉任何東西。

---

## 1. 安全契約（不可協商，違反其一即整條線失效）

1. 憑證值**永不**寫入任何輸出、檔案、log、證據、prompt、remote URL、`.git/config`；一律 `[REDACTED]`。
2. 憑證只存在於 **broker 行程記憶體** 與 **git 子行程的環境變數**。
3. 憑證以 **URL-scoped** 的 `http.https://github.com/.extraheader` 傳遞，透過 `GIT_CONFIG_KEY_0`／`GIT_CONFIG_VALUE_0`（**環境**，非 argv）。
4. **絕不**用命令列 `-c <那個 extraheader key>`——CLI 的值會**覆蓋並清空**該 header，造成「靜默的未認證推送」（前幾輪踩過的真實 bug）。
5. `GIT_TERMINAL_PROMPT=0`、`GIT_CONFIG_NOSYSTEM=1`、`credential.helper=` 重設。
6. repo 內**不含任何憑證**；broker 一律從**外部**檔案或外部私鑰讀取。
7. 私鑰檔**必須在 `.git` 之外**，且不得位於任何 repo 內。
8. `cred_preflight.py` **fail-closed**：任何無法確認的檢查都算 FAIL，`exit 2`，該次執行必須中止。
9. 推送用畢即清除 shim／暫存；`.git/config` 檢查憑證殘留為 0。
10. 憑證檔若是**筆記型檔案**（見 §6 第 1 條），**必須先做形狀比對再取用**，不可 `$(cat)`。

---

## 2. 盤點：先確認你手上的是什麼（不需要讀憑證值）

```bash
# 工具是否就位、是否仍未啟用
cd C:/Projects/Agent_Workspace/HG-KSEOS
python -c "import json,hashlib,pathlib as p;m=json.load(open('scripts/cred/INSTALL_MANIFEST.json'));[print(f['target'], hashlib.sha256((p.Path('.')/f['target']).read_bytes()).hexdigest()==f['sha256']) for f in m['files']]"
python scripts/cred/verify_offline.py     # 期望 PASS_OFFLINE_T5_UNPROVEN (exit 0)
python scripts/cred/cred_preflight.py --metadata-only   # 期望狀態、不讀內容
```

**期望**：7/7 pin `True`；`PASS_OFFLINE_T5_UNPROVEN`（T5 需網路，**永遠不會**被離線驗證報成 PASS）。

> **實測更正（重要）**：本機跑 `--metadata-only` 實際回 **`OK` / `abort=false` / exit 0**，**不是** fail-closed。
> 原因是 `cred_preflight.py:34-35` **硬編了一個預設路徑**指向 owner 的筆記檔：
> `C:\Projects\Agent_Workspace\API KEY\Fine-grained personal access tokens.txt`。
> 所以**在任何環境變數都没設的情況下，工具仍會去讀那個檔**。見 §10「已知耦合」。
> 要驗證 fail-closed 行為，必須明確指向不存在路徑：
> `HGK_CRED_FILE=/nonexistent python scripts/cred/cred_preflight.py --metadata-only` → 期望 `FAIL_CLOSED` (exit 2)。

---

## 3. 階段一：建立 GitHub App（**四步，全在瀏覽器，無法自動化**）

### 步驟 1 — 註冊 App

`https://github.com/settings/apps/new`（個人）或 `https://github.com/organizations/shw097-team/settings/apps/new`（組織）。

| 欄位 | 填什麼 | 理由 |
|---|---|---|
| GitHub App name | 例：`HGK-SWOF-ACCEPTANCE-BRIDGE-APP` | 名稱全域唯一；沿用舊 PAT 的名字便於對照 |
| Homepage URL | 你的 repo URL 即可 | 必填，不影響功能 |
| **Webhook** | **取消勾選 Active** | 我們是被動推送方，不需要回呼；開了只會多出失敗投遞告警 |
| Repository permissions → **Contents** | **Read and write** | 這是推送唯一需要的權限 |
| Repository permissions → 其餘 | **No access** | 最小權限。**不要**給 Administration／Workflows／Actions |
| Organization permissions | 全部 **No access** | 同上 |
| 安裝範圍 | **Only select repositories** → `PIPD-LS-SP` | 比 All repositories 安全得多 |

建立後記下 **App ID**（頁面上可見）。**這不是機密**。

> **教學點**：App ID 是公開標識，私鑰才是機密。兩者常被新手搞混，導致把 ID 也當秘密藏起來——沒有必要。

### 步驟 2 — 產生並下載私鑰

App 設定頁 → **Private keys** → **Generate a private key**。

瀏覽器會下載一個 `.pem`（例：`hgk-swf-acceptance-bridge-app.2026-10-11.private-key.pem`）。

**三個必守事項**：
- `.pem` **只下載一次**，關掉頁面就沒了；遺失只能重新產生。
- 存放在**任何 repo 之外**，例：`C:/Users/user/.hgk-creds/hgk-app.private-key.pem`。
- 立刻確認它**不在** `.git` 內、不在工作區內（見 §5 的檢查）。

### 步驟 3 — 安裝 App 到 repo

App 頁面 → **Install App** → 選 `shw097-team` → **Only select repositories** → 勾 `PIPD-LS-SP` → **Install**。

安裝後看 URL：`https://github.com/settings/installations/<數字>`。**那個數字就是 Installation ID**。也不是機密。

> **若你漏了這步**，稍後 mint 會回 `404`——因為 App 還沒被安裝到任何 repo，就沒有 installation 可以換 token。這是**最常見**的失敗。

### 步驟 4 — 放到主機並設環境變數

```bash
# 1) 把私鑰放到 repo 之外（路徑自訂，以下為例）
mkdir -p /c/Users/user/.hgk-creds
#    把下載的 .pem 移進去，並改名為固定名稱
#    mv "C:/Users/user/Downloads/<下載的>.pem" "C:/Users/user/.hgk-creds/hgk-app.private-key.pem"

# 2) 收緊權限（非 Windows 必要，但養成習慣）
chmod 600 /c/Users/user/.hgk-creds/hgk-app.private-key.pem

# 3) 設為「使用者層級」環境變數（Windows，透過 setx 永久生效）
#    注意：setx 只影響「之後新開」的行程，本 shell 需重開
setx HGK_APP_ID "<你的 App ID>"
setx HGK_APP_KEY "C:/Users/user/.hgk-creds/hgk-app.private-key.pem"
setx HGK_APP_INSTALLATION_ID "<你的 Installation ID>"
setx HGK_REPO_SLUG "shw097-team/PIPD-LS-SP"
```

**這三個值都不是機密**（App ID、路徑、Installation ID）。**私鑰檔案本身才是機密**，而它從不進入任何環境變數的字面上——只有**路徑**進去。

> **為什麼用環境變數而不是寫進設定檔？** `INSTALL.md` 的契約第 6 條：repo 內不得含憑證，且設定一律走環境，不走 argv。argv 會出現在**行程清單**裡，任何同機使用者都看得到。

---

## 4. 階段二：驗證（不讀憑證值、不真的推送）

```bash
cd C:/Projects/Agent_Workspace/HG-KSEOS

# (a) 完整 preflight：會做「網路有效性探測」，但只讀 token，不印
python scripts/cred/cred_broker.py preflight
#     期望：abort=false；app_config_present=PASS；credential_kind=app

# (b) dry-run：真的去 acquire 一個憑證，但只印 kind 與長度
python scripts/cred/cred_broker.py dry-run
#     目標狀態（App 已設）：credential_kind="app"、credential_length≈40
#     ── 本機【今天實測】──：credential_kind="pat"、credential_length=93、
#           header_would_be_supplied=true、secret_printed=false、verdict=OK
#     credential_kind 仍是 pat 是【預期】的：App 三個變數尚未設定。
```

`dry-run` 是**這套工具最重要的設計**：它證明「mint 得出來、header 放得進去」，而**不**把 secret 印出來，也**不**真的推送。

**兩個關鍵讀數**：
- `credential_kind` 若仍是 `"pat"` → 表示 `HGK_APP_KEY` 沒生效（多半是 setx 後沒重開 shell），你還在走橋接。
- `credential_length` 約 40 是 GitHub App installation token 的正常長度；PAT 是 `github_pat_` 開頭、長得多。**這是區分你在走哪條路的唯一可靠方式。**

---

## 5. 階段三：真正推送（附安全檢查）

```bash
cd C:/Projects/Agent_Workspace/PIPD-r7-release
python "C:/Projects/Agent_Workspace/HG-KSEOS/scripts/cred/cred_broker.py" run -- push origin main
```

`run` 會：先 preflight（fail-closed）→ mint → 以子行程環境跑 `git push` → 檢查 stdout/stderr **有無憑證洩漏**（`secret_leaked`）→ 回報。

**推送後必做的三項核對**（這三步抓過真實問題，不可省）：

```bash
# 1) 遠端真的前進了嗎？（不要只看本機 HEAD）
git ls-remote --heads https://github.com/shw097-team/PIPD-LS-SP.git main

# 2) tag 有沒有被動到？（App token 不會動 tag，但驗一下成本為零）
git ls-remote https://github.com/shw097-team/PIPD-LS-SP.git "refs/tags/*"

# 3) .git/config 有沒有憑證殘留？工作樹乾淨嗎？
grep -i "extraheader\|x-access-token" .git/config || echo "CONFIG_CLEAN"
git status --porcelain | wc -l     # 期望 0
```

> **教學點**：`git push` 回 `exit 0` **不等於**遠端前進。前幾輪就發生過「推送看似成功、實際送出空認證」的靜默失敗。**一律用 `ls-remote` 對遠端讀回來確認**——這是「外部狀態要讀回驗證」的具體例子。

---

## 6. PAT 輪替（過渡橋接，仍建議做）

**GitHub 沒有 API 可以讀或改 PAT 到期日**，所以無法自動輪替。可行做法如下。

### 第 1 條 — 認清你的憑證檔是「筆記」，不是裸 token（**這引起過一次真實誤判**）

本工作區的 `API KEY/Fine-grained personal access tokens.txt` **不是**一個裸 token，而是 **4 行 CRLF 筆記，token 在第 4 行（93 字元）**。

因此 `$(cat 檔案)` 會把四行串成一個密碼送出 → 認證失敗 → **看起來像「PAT 已失效」**。
前幾輪就是這樣把「PAT 失效」的錯誤結論送給 owner 的。

**正確做法**：先做**形狀比對**，取唯一命中的那一行：

```python
import re
cand = [l.strip() for l in open(PATH, encoding='utf-8', errors='replace').split('\n')
        if re.fullmatch(r'github_pat_[A-Za-z0-9_]{20,}', l.strip())]
assert len(cand) == 1        # 命中數不是 1 就停手，不要猜
```

### 第 2 條 — 輪替的實際步驟（全瀏覽器）

1. `https://github.com/settings/personal-access-tokens` → 找到 `HGK-SWOF-ACCEPTANCE-BRIDGE`。
2. 記下它的 **Expiration**（這是**唯一**能看到的地方，沒有 API）。
3. 建立新 token：`Generate new token`，**Repository access** = Only select repositories → `PIPD-LS-SP`；**Permissions → Contents = Read and write**（其餘全部 No access）；**Expiration 建議 90 天**。
4. 更新本機檔案第 4 行（**不要**把值貼進對話、log 或 commit）。
5. 依 §4 跑 `dry-run` 驗證。
6. 確認新 token 可用**之後**，才在 GitHub 上**撤銷舊 token**。順序反了就會斷線。

### 第 3 條 — 到期前自動「提醒」（無 API，用檔案記錄取代查詢）

因為讀不到到期日，就把**已知的到期日**寫進檔案，讓 preflight／自動化可以判斷：

```bash
setx HGK_CRED_EXPIRY_FILE "C:/Users/user/.hgk-creds/pat-expiry.txt"
# 檔案內容只要一行 ISO 日期，例：2027-01-09
```

時間軸建議：**到期前 14 天**排一個提醒；**7 天前**完成輪替。

> **教學點**：無法查詢的屬性，就用「記錄下來的已知值」代替。這是整條線的通用模式——`HGK_CRED_EXPIRY_FILE` 不是繞過 GitHub，而是把「你已知的事實」交給自動化，讓它能在到期前**自己**喊停。

### 第 4 條 — 長期方向：App 到位後 PAT 就退休

`cred_broker.py` 的 `acquire()` **優先 App、回退 PAT**。所以：

- App 驗證通過後，**不必刪 PAT**——它自然不會被用到。
- 想徹底關掉橋接，把 `HGK_CRED_FILE` 指向不存在路徑即可，並確認 `dry-run` 仍回 `credential_kind="app"`。
- 最後再在 GitHub 撤銷 PAT。

---

## 7. 日常維運：如何做到無人值守長任務零人工

| 需求 | 做法 |
|---|---|
| token 永不加班 | App installation token TTL 1 小時，`cred_broker.py` **每次執行現 mint**。長任務不需續期邏輯。 |
| 憑證漂移偵測 | 每次推送前 `cred_broker.py preflight`（fail-closed）＋推送後 `secret_leaked` 檢查。 |
| 到期風險 | App 私鑰**不會過期**（除非你撤銷它）。PAT 橋接則靠 §6 第 3 條的到期檔提醒。 |
| 私鑰遺失 | 重新產生並覆蓋；App ID／Installation ID 不變。 |
| 洩漏應變 | 撤銷 App 私鑰（Private keys → 刪除）或撤銷 installation（Uninstall）。**App 私鑰洩漏的爆炸半徑遠小於 PAT**——這是 App 的核心優勢。 |

---

## 8. 故障排除（症狀 → 根因 → 修法）

| 症狀 | 根因 | 修法 |
|---|---|---|
| `Invalid username or token` | 用 `$(cat)` 讀了 **4 行筆記檔** | 改用形狀比對取單行（§6 第 1 條） |
| `ERR` 但 `exit 0`、遠端沒動 | 推送送出**空認證**（靜默未認證） | 檢查是否用 CLI `-c extraheader` 覆蓋了環境值（契約第 4 條）；改用 `cred_broker.py run` |
| mint 回 `404` | **App 未安裝到該 repo**（跳過步驟 3） | 完成 Install App |
| mint 回 `401` | App ID 或私鑰不符 | 核對 `HGK_APP_ID` 與 `.pem` 是否同一組 |
| `dry-run` 顯示 `credential_kind="pat"` | `HGK_APP_KEY` 未生效 | **setx 後要重開 shell**；或路徑用了 MSYS `/c/...`（原生程式不轉譯） |
| `header_would_be_supplied=false` 但推送其實正常 | **已修的缺陷**：舊版把自我檢查比對一個寫死的遮蔽佔位字串，該欄位**永遠報 false** | 已修為語意檢查（比對 key 尾綴與 value 前綴）。若你看到 false，先確認工具版本 |
| preflight `exit 2` | fail-closed 正確觸發 | 讀它印出的逐項 `checks`，找出是哪一項 FAIL |
| 私鑰在 repo 內被看到 | 放錯位置 | 移到 `.git` 之外；`git status` 應看不到它 |

> **環境陷阱（本機實測）**：`taskkill //F //PID` 在 git-bash/MSYS 下**會被改寫成無效參數並靜默失敗**（錯誤容易被 `| head` 吞掉）。要停長時程序，**確認 pid 真的消失**再回報——「未經驗證的終止」也是一個未經驗證的主張。

---

## 9. 驗收清單（逐條可勾）

- [ ] 步驟 1：App 已建立，**Webhook 未啟用**，Contents 僅 `Read and write`，範圍限 `PIPD-LS-SP`
- [ ] 步驟 2：`.pem` 已下載，存放於**任何 repo 之外**
- [ ] 步驟 3：App 已安裝到 `PIPD-LS-SP`，`Installation ID` 已記下
- [ ] 步驟 4：`HGK_APP_ID`／`HGK_APP_KEY`／`HGK_APP_INSTALLATION_ID` 已設為**使用者環境變數**
- [ ] §2 盤點：7/7 pin `True`、`PASS_OFFLINE_T5_UNPROVEN`
- [ ] §4 驗證：`preflight` → `abort=false`；`dry-run` → `verdict=OK`、`credential_kind="app"`、`secret_printed=false`
- [ ] §5 推送：遠端 `main` 以 `ls-remote` 讀回確認前進；tag 未動；`.git/config` 乾淨；`git status --porcelain` = 0
- [ ] §6：PAT 到期日已記入 `HGK_CRED_EXPIRY_FILE`，並設了 14 天／7 天提醒
- [ ] 全程未把任何憑證值寫入檔案、輸出、log、commit 或對話

---

## 10. 誠實界線（做不到的事）

- **四步只能人工**：App 註冊、私鑰下載、安裝同意、PAT 輪替／到期讀取——**GitHub 沒有對應 API**。
- **`verify_offline.py` 的 T5 永遠不是 PASS**：它是 `PASS_OFFLINE_T5_UNPROVEN`，因為離線無法證明線上行為。
- **broker 仍未「啟用」**：它躺在 `HG-KSEOS/scripts/cred/`，`config/` 對它的引用數為 **0**。把它接進 push 流程是**另一個獨立的控制平面輪次**，需自己的 admission。
- **App installation token 也不是萬能**：1 小時 TTL 意味著長任務中**每次**推送前都要重新 mint（這正是設計，不是缺點）。
- **本指引不證明**推送流程已被端到端啟用；它只描述**可執行且已驗證到 dry-run 層級**的操作。

### 已知耦合（照實揭露，本輪**未**改動）

`cred_preflight.py` 內建一個**指向本機絕對路徑**的預設憑證來源（見 §2 更正）。後果與處置：

- **好處**：本機免設定即可運作（`dry-run` 實測已能取得 93 字元的 PAT）。
- **風險**：這個默認值**默默把控制平面工具綁在一台主機的檔案佈局**上；換主機就會 fail-closed（安全，但看起來像壞掉）。
- **本輪裁決**：**揭露而不改動**。改動預設解析屬控制平面行為變更，需自己的 admission；且 `HGK_CRED_FILE` 仍是唯一正式機制（§6 第 3 條）。
  **因此：請一律顯式設定 `HGK_CRED_FILE`，不要依賴內建預設值。**
