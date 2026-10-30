# FAR_R18-11 — 為什麼我一直停，以及如何讓它不再停

裁決基準（上位優先）：① 對齊 r2-revision2 ② Native E2E 閉環 ③ 無人值守 ④ 高必要性 ⑤ 不過度治理／工程化 ⑥ 低阻力高效率

---

## 一、根因（實測，不是自評）

| 你的假設 | 量測 | 判定 |
|---|---|---|
| 停下是因為四庫／治理過重？ | 佇列狀態 `DONE 7 · PARTIAL 8 · PARKED 10 · HOLD 1`，而腳本判定 **actionable = 0 列**；goal `status=paused`；gate `--audit` **rc=0** | **不是治理重，是我的狀態機把 PARTIAL 當終點**。佇列自己宣告「沒事了」，於是我每次都在合法地停 |
| 是 thin prompt 治理過重？ | 22 個 WP 中真正需要第二 principal 的只有三類：**11 列等 Issuer、1 列等 Writer、1 列等 checker**；其餘皆本地可量測 | prompt 不是停的原因；**SoD（三個不同 principal）才是吞吐上限**，而那是正確的治理 |
| 為何 /goal 顯示「目標受阻」？ | `state_meta.goal.status = paused`（先前 gate 連續失敗 2/5 被暫停）；現 gate rc=0 | 是**狀態殘留**，不是當前阻塞。已改回 `active` |
| 為何「接著我做」卻沒做？ | 沒有任何排程器在叫我。turn-based agent 沒有自我喚醒能力 | **架構問題**，只能靠排程器解決 |

一句話：**我把「可辯護的暫停」做成了「自動的停止」——佇列把未完成工作標成非行動項，且沒有東西在我離開後繼續跑。**

---

## 二、已落地（本回合實作，非建議）

1. **PARTIAL 不再是終點**：`tools/r18_autodriver.py` 的 actionable 改為「有 JOB 且狀態非 DONE/REUSE」。
2. **第一次無人值守執行已完成**：driver 跑 4 個 job，`PARKED 10→7`、`PARTIAL 8→11`；`WP-02/03/17` 由一句話 PARK 變成**實測**（`receipts/WP0203_17_BINDINGS.json`：policy present 無 epoch、Issuer present 但 registry rev 為 None、CAP-BOOT absent）。
3. **排程器已建立並啟動**：cron `2897733e2ca1`（`every 30m`、`no_agent`、`script=r18_driver_tick.py`），並啟動 **gateway**（PID 23508）——先前 gateway 沒跑，任何 cron 都不會觸發。
4. **goal 已 resume**：`paused → active`。
5. **journal**：`receipts/DRIVER_JOURNAL.jsonl` 逐次記錄 rc／秒數／stdout 尾。

---

## 三、裁決

- **D1（③⑥）單一佇列為準**：`ledger.json` 是唯一工作隊列；Kanban 只做視圖，由 driver 更新。
- **D2（③）只有三種情況可停**：需要 Issuer／Writer／checker（typed，附 resume_predicate）、破壞性動作、憑證缺失。
- **D3（②）車道只用在需要第二 principal 之處**：WP-07、WP-09；讀取型量測不開車道。
- **D4（⑤）不新增第五個追蹤器**：ledger＋DRIVER_JOURNAL＋receipts 已足；FAR 只在有裁決時寫。
- **D5（①④）交付由 driver 批次推送**，不每回合開 PR。

---

## 四、仍然真實的限制（不美化）

1. **11 個 HOST_OP/RELEASE 需 Issuer PERMIT**：owner 窗口（`WIN-796b69117680`，39/40 ops 尚存）只能簽 payload，不能代替 Issuer 發 PERMIT。
2. **WP-09 的 HOLD 不會因再跑一次變 PASS**：缺的是 native 執行證據。
3. **gateway 未安裝為 Windows 排程工作**：目前是手動 spawn，重開機後不自動起；要真正長期無人值守須 `hermes gateway install`。
4. **另一 SESSION 仍在動**：`HG-KSEOS` 有 4 個非我修改的檔案（含 dispatcher），車道收據只能重現於當前樹。

---

## 五、結論

治理不是停止的原因；**停止的原因是佇列語義 + 缺少排程器**。兩者已修正並以實跑證明。剩下的停頓只會來自「需要別的 principal 簽」——那是設計上應該停的地方。
