# Mô hình một session code đáng tin cậy

Tài liệu này mô tả một session code đi từ brainstorm đến khi ship, và chỉ ra bảy vấn đề của coding agent được xử lý ở bước nào. Phần cuối là nghiên cứu các skill trong `reference/` và bảng so sánh chúng.

**Trạng thái: bản nháp.** Mô hình chưa chốt. Các phase và cổng bên dưới là điểm xuất phát để chỉnh, chưa phải kết luận. Mục 12 ghi các chỗ còn nghi ngờ.

**Cách đọc tài liệu.** Các skill trong `reference/` tồn tại sẵn. Mô hình session (các phase, các cổng, ngân sách context) là đề xuất ghép của tài liệu này, chưa có bộ skill nào cung cấp sẵn nguyên chuỗi. Chỗ nào là đề xuất thì được đánh dấu **[Đề xuất]**.

---

## 1. Bảy vấn đề

| # | Vấn đề | Gốc rễ |
|---|---|---|
| P1 | Agent tự giả định, không quan tâm user journey | Khoảng cách giao tiếp: agent bắt đầu làm khi chưa hiểu người dùng cần gì |
| P2 | Kiến trúc cần được mô hình hóa, duyệt và ghi lại | Agent nhảy vào code, hình dạng hệ thống phát sinh ngẫu nhiên |
| P3 | Test case không được kiểm chứng | Test pass theo cấu trúc (tautological), hoặc dính vào implementation |
| P4 | Code quá nhiều trước khi review, review thành bất khả thi | Không có đơn vị công việc nhỏ và không có điểm dừng |
| P5 | AI slop: tạo lại, trùng lặp, code rác, viết thừa hoặc làm phức tạp quá mức | Agent không thấy toàn repo, copy ví dụ gần nhất, thêm phòng thủ và abstraction thừa; việc nhỏ bị làm to, việc giản dị bị làm phức tạp (xem mục 7) |
| P6 | Output chưa được chạy thử e2e như người dùng thật (browser, CLI) | "Compile được" và "unit test xanh" bị coi là xong |
| P7 | Chạy quá dài, từ smart zone rơi sang dump zone | Context đầy dần, chất lượng suy luận giảm |

Smart zone là khoảng context mà model còn suy luận sắc nét. `ask-matt` ước lượng khoảng 150k token trên các model tiên tiến. Qua ngưỡng đó là dump zone.

---

## 2. Nguyên tắc thiết kế

1. **Một session là một chuỗi phase, mỗi phase có artifact đầu ra và một cổng duyệt.** Không có artifact thì không qua phase. Artifact nằm trên đĩa hoặc tracker, không nằm trong trí nhớ của hội thoại.
2. **Con người duyệt ở chỗ rẻ nhất để sửa.** Hiểu sai user journey thì sửa ở phase 1 gần như miễn phí. Ở phase 6 thì tốn cả tuần.
3. **Mỗi đơn vị code nhỏ tới mức review được và kiểm chứng được trước khi sang đơn vị sau.**
4. **Bằng chứng thay cho lời nói.** "Xong" nghĩa là có artifact chạy thật (transcript, screenshot, output), không phải agent tự nói "xong".
5. **Context là tài nguyên có ngân sách.** Phase lập kế hoạch chia sẻ một context. Mỗi ticket triển khai bắt đầu một context mới.
6. **Lỗi lặp lại phải biến thành cơ chế**, không phải thêm một dòng dặn dò nữa.
7. **Phạm vi là hợp đồng được cưỡng chế.** Mỗi ticket khai báo cái được đổi và cái không làm. Công cụ (hook, lint) chặn hoặc hỏi khi vượt ra ngoài, thay vì chỉ dặn agent "đừng làm thừa" (mục 7).
8. **Giữ chỉ dẫn chung ngắn.** Quy tắc theo ticket đặt trong ticket; quy tắc lặp lại chuyển thành lint. Đừng nhồi vào CLAUDE.md (mục 7, tầng 6).

---

## 3. Tổng quan mô hình

```
 Phase 0   Setup (một lần cho mỗi repo)
              │
 ┌────────────┴─ Context A: lập kế hoạch (giữ liền mạch, ≤ smart zone) ─────────────┐
 │ Phase 1  Brainstorm & Align    ──► [G1] user xác nhận mục tiêu + user journey    │
 │ Phase 2  Spec                  ──► [G2] user duyệt spec                          │
 │ Phase 3  Architecture          ──► [G3] user duyệt sketch + ADR                  │
 │ Phase 4  Slice                 ──► [G4] user duyệt danh sách ticket              │
 └──────────────────────────────────────────────────────────────────────────────────┘
              │  handoff / clear
 ┌────────────┴─ Context B(n): mỗi ticket một context mới ──────────────────────────┐
 │ Phase 5  Implement (tdd, nhỏ)  ──► [G5] seams đã duyệt, mỗi slice red→green      │
 │ Phase 6  Review                ──► [G6] standards + spec + slop + test sạch      │
 │ Phase 7  Verify e2e            ──► [G7] VERIFIED kèm bằng chứng                  │
 └──────────────────────────────────────────────────────────────────────────────────┘
              │
 Phase 8   Ship & Learn            ──► PR có evidence, retro, mã hóa bài học
```

Các cổng G1 đến G4 là chỗ con người ngồi lại. G5 đến G7 do agent tự thực thi, người chỉ duyệt kết quả cuối.

---

## 4. Các phase

Mỗi phase có: mục tiêu, skill dùng, artifact đầu ra, cổng, và vấn đề được xử lý.

### Phase 0. Setup (một lần cho mỗi repo)

- **Mục tiêu:** để mọi session sau đó khởi động trên một nền đã có từ vựng, chuẩn code và cách chạy thử app.
- **Skill:**
  - `setup-matt-pocock-skills`: chọn issue tracker, nhãn triage, nơi lưu tài liệu.
  - `create-verification-skill` (pstack): sinh skill `verify-<app>` riêng cho repo (Launch, Doctor, Drive, Evidence, Cleanup) cùng feature map. Skill sinh ra phải được chạy thử một lần trước khi bàn giao.
  - `maintain-verification-skill` (pstack): chạy định kỳ để giữ feature map đúng với app (mục 6).
  - `GLOSSARY.md`, ADR, tài liệu coding standards (tạo dần qua `domain-modeling`).
  - **[Đề xuất]** `karpathy-guidelines` làm nền cho file chỉ dẫn ngắn của repo, sau khi chỉnh hai chỗ xung đột với các skill khác (mục 9.5).
  - **[Đề xuất]** Hook và lint chặn code thừa (mục 7, tầng 1 đến 3) được cài một lần ở đây.
- **Artifact:** `GLOSSARY.md`, thư mục ADR, coding standards, `verify-<app>/` (gồm `features/`), cấu hình hook phạm vi.
- **Xử lý:** nền cho P1, P5, P6. Đây là chỗ biến "cách chạy thử như user thật" thành tài sản của repo thay vì phát minh lại mỗi session.

### Phase 1. Brainstorm & Align

- **Mục tiêu:** hiểu đúng người dùng cần gì và hành trình của họ, trước khi nói tới giải pháp.
- **Skill:**
  - `grill-with-docs` (Matt): phỏng vấn dai dẳng tới khi mọi nhánh quyết định được giải quyết, đồng thời cập nhật `GLOSSARY.md` và ADR ngay trong lúc hỏi.
  - `in-your-own-words` (pstack): agent diễn đạt lại mục tiêu và vấn đề của bạn bằng lời của nó để bạn bắt chỗ hiểu sai.
  - `prototyping-designs` (Matt), khi câu hỏi cần trả lời bằng thứ chạy được: một file HTML để thử state model, hoặc vài biến thể UI chuyển được trên một route. Prototype là code vứt đi.
  - `research` (Matt), khi cần sự thật từ tài liệu chính thống: chạy nền, ghi kết quả có trích dẫn vào file Markdown.
- **[Đề xuất]** Ghi rõ user journey thành một artifact riêng (các bước, điểm đau, điểm thành công) ngay trong phase này. Các skill hiện có không tạo artifact đó. Journey chỉ nằm ngầm trong buổi grill và trong user stories của spec.
- **Cổng G1:** bạn xác nhận lại bản diễn đạt mục tiêu và user journey.
- **Xử lý:** P1 là chính. Một phần P2 (từ vựng chung).

### Phase 2. Spec

- **Mục tiêu:** biến cuộc hội thoại đã thống nhất thành tài liệu có thể giao cho agent khác thực thi.
- **Skill:**
  - `to-spec` (Matt): không phỏng vấn lại, chỉ tổng hợp. Spec có Problem Statement, Solution, danh sách User Stories dài, và các seam sẽ test. Mặc định mỗi spec nên có ít seam nhất có thể, lý tưởng là một. Seam phải được bạn xác nhận.
  - Thay thế: `spec-it` (gstack) gồm 5 phase (Why, Scope, Technical Interrogation sau khi đọc code, Draft Review, Quality Gate rồi file lên tracker). Có Acceptance Criteria, Testing Plan, Out of Scope, "Do Not Touch" và Rollback Plan.
- **[Đề xuất]** Nếu repo có feature map (mục 6), spec dùng ID sub-feature để chỉ rõ hành vi nào được thêm hoặc đổi.
- **Artifact:** spec trên tracker.
- **Cổng G2:** bạn duyệt spec, trong đó có danh sách seam sẽ test.
- **Xử lý:** P1, và phần "seam được duyệt" của P3.

### Phase 3. Architecture

- **Mục tiêu:** quyết định hình dạng hệ thống trước khi viết code, ghi lại và được duyệt.
- **Skill:**
  - `domain-modeling` (Matt): thử các thuật ngữ với glossary, thử tình huống biên, ghi ADR.
  - `codebase-design` (Matt): từ vựng deep module, seam, adapter. Có "deletion test" và nguyên tắc "một adapter là seam giả định, hai adapter mới là seam thật".
  - `designing-architecture` (pstack): phác kiểu, signature, cấu trúc module với body `not implemented`. Chạy nhiều ứng viên khác cấu trúc ("design it twice") rồi tổng hợp. Sketch là hợp đồng: sai lệch phải báo lại, và nếu ma sát lặp đi lặp lại thì bỏ sketch và làm lại.
  - `plan-eng-review` (gstack): review kiến trúc kèm sơ đồ ASCII, yêu cầu cập nhật sơ đồ cùng commit với code.
  - `improve-codebase-architecture` (Matt), khi thay đổi chạm vào vùng code đã rối.
- **Artifact:** sketch (kiểu, signature, ranh giới module), ADR cho quyết định khó đảo ngược, sơ đồ.
- **[Đề xuất] Cổng G3 là cứng.** Ở `designing-architecture`, bước duyệt mặc định tắt ("proceed directly to implementation"), chỉ bật khi bạn yêu cầu. Quy trình này luôn bật checkpoint để đáp ứng P2: không có sketch được duyệt và ADR thì không qua phase 4.
- **Xử lý:** P2 là chính. Một phần P5 (chặn trùng lặp từ gốc nhờ hiểu chỗ đặt code).

### Phase 4. Slice

- **Mục tiêu:** cắt công việc thành các lát nhỏ đủ để review từng lát và đủ nhỏ để vừa một context mới.
- **Skill:**
  - `to-tickets` (Matt): tracer-bullet ticket. Mỗi ticket cắt một đường hẹp nhưng trọn vẹn xuyên mọi tầng, demo được riêng, vừa một context window. Mỗi ticket khai báo ticket nào chặn nó, nên tạo thành một đồ thị tác vụ. Thay đổi rộng cơ học (rename trên toàn repo) dùng expand–contract. Bạn duyệt độ mịn và các cạnh chặn trước khi publish.
  - `wayfinder` (Matt), nếu công việc quá lớn cho một agent session: lập bản đồ các ticket quyết định, giải quyết từng cái cho tới khi đường đi rõ.
  - `principle-sequence-verifiable-units` (pstack): mỗi đơn vị kết thúc ở trạng thái kiểm tra được; thứ tự commit/PR kể một lập luận (test fail trước, fix sau).
  - `blast-radius` (pstack): tìm những gì thay đổi có thể làm vỡ ở nơi khác trước khi ship.
- **[Đề xuất] Mở rộng template ticket.** Template ticket của Matt có acceptance criteria nhưng thiếu các mục sau:
  - **Kịch bản e2e:** cách người dùng thật chứng minh ticket chạy được, làm đầu vào cho Phase 7.
  - **Phạm vi:** danh sách file dự kiến sửa, danh sách file cấm đụng (manifest, lock file, config), và mục "Không làm". Lưu thành `scope.json` để hook ở Phase 5 đọc (mục 7).
  - **Thay đổi feature map dự kiến:** sub-feature nào thêm hoặc đổi. Phase 7 dùng mục này để phát hiện bề mặt thừa.
  - Lưu ý: tracer-bullet cắt xuyên mọi tầng, nên một thay đổi nhỏ ở tầng giữa có thể bị hiểu là phải dựng đủ các tầng. Mục "Phạm vi" ở trên giảm rủi ro này.
- **Artifact:** các ticket kèm cạnh chặn.
- **Cổng G4:** bạn duyệt danh sách ticket.
- **Xử lý:** P4 là chính. P7 nhờ ticket vừa một context.

**Ranh giới context.** Sau G4, kết thúc Context A. `ask-matt` khuyên giữ grill, spec và tickets trong một context liền mạch rồi mới `/clear`. Từ đây mỗi ticket bắt đầu một context mới, đọc từ ticket và spec, không đọc từ trí nhớ hội thoại.

### Phase 5. Implement (cho từng ticket, context mới)

- **Mục tiêu:** hiện thực đúng một ticket bằng các bước nhỏ có phản hồi.
- **Skill:**
  - `implementing-tickets` (Matt): lấy ticket, nêu tiêu đề, gọi `tdd`, chạy typecheck và từng file test thường xuyên, chạy cả bộ test một lần ở cuối, gọi `code-review`, commit.
  - `implement-spec` (Matt), khi muốn chạy cả đồ thị ticket: các subagent implementer chạy song song trên "frontier", mỗi cái một worktree, một merger subagent gộp về nhánh tích hợp, cuối cùng chạy `code-review` một lần.
  - `tdd` (Matt): red trước green, một slice dọc mỗi lần, chỉ test ở seam đã duyệt. Refactor không nằm trong vòng lặp mà thuộc phase review.
  - `principle-test-behavior-not-implementation` (pstack): phép thử hai chiều cho từng test (phá behavior thì test phải fail; đổi internals thì test phải vẫn pass).
- **Artifact:** commit nhỏ, mỗi commit ứng với một slice red→green.
- **[Đề xuất] Cưỡng chế phạm vi lúc code** (chi tiết ở mục 7). Các skill hiện có chỉ cắt việc ở Phase 4 và không chặn gì lúc đang code:
  - Hook PreToolUse đọc `scope.json`: sửa file trong danh sách thì cho qua; tạo file mới hoặc sửa ngoài danh sách thì hỏi; chạm file cấm thì từ chối.
  - Kiểm tra máy móc sau khi sửa: lint, type, và các kiểu thừa lặp lại (tham số/export không dùng, hàm bọc một nơi gọi, `catch` rỗng, dependency mới).
  - Hook Stop so `git diff` với `scope.json` trước khi agent được kết thúc.
  - Thay cho ngưỡng cố định ~400 dòng ở bản trước (không có căn cứ): so diff với phạm vi dự kiến của ticket. Một nguồn cộng đồng dùng ngưỡng ~20 dòng hoặc một file mới để dừng và hỏi; đó là kinh nghiệm của một bài viết, không phải số liệu đo.
- **Cổng G5:** seam test đã duyệt, mỗi slice có test fail trước khi pass, diff nằm trong phạm vi hoặc phần vượt đã được giải thích và duyệt.
- **Xử lý:** P3, P4, P5 (nguyên tắc `laziness-protocol`, `subtract-before-you-add` của pstack).

### Phase 6. Review

- **Mục tiêu:** bắt sai lệch spec, vi phạm chuẩn, slop, test yếu, trước khi chạm vào thế giới thật.
- **Skill:**
  - `code-review` (Matt): hai trục chạy song song bằng subagent, không trộn kết quả. **Standards** (chuẩn của repo, cộng baseline 12 code smell của Fowler như Duplicated Code, Speculative Generality, Shotgun Surgery). **Spec** (yêu cầu thiếu, scope creep, yêu cầu được hiện thực sai).
  - `deslop` (cursor-team-kit): gỡ comment thừa, try/catch bất thường, ép kiểu `any`, lồng sâu, so với main.
  - `deslop-shared-libs` (gstack): tìm đoạn đáng gom thành code dùng chung trong công việc gần đây.
  - `test-audit` (gstack): quét test giá trị thấp hoặc trùng lặp, cùng code chỉ tồn tại vì test đó.
  - `reviewing-changes` (gstack): review trước khi land, có phát hiện scope drift (so với kế hoạch) và slop scan.
  - `interrogate` (pstack), khi cần nhiều model phản biện lẫn nhau.
- **[Đề xuất]** Reviewer chạy trong **ngữ cảnh mới**, không phải phiên đã viết code, để dễ thấy phần thừa. Lưu ý bước này phát hiện sau khi code thừa đã viết; giảm chi phí thật nằm ở các cổng ở Phase 5.
- **Artifact:** báo cáo Standards và Spec riêng biệt, kèm các sửa đã áp dụng.
- **Cổng G6:** không còn finding nghiêm trọng ở cả hai trục.
- **Xử lý:** P3, P5, và kiểm tra lại P4.

### Phase 7. Verify e2e

- **Mục tiêu:** chứng minh tính năng chạy như người dùng thật dùng, bằng bằng chứng quan sát được.
- **Skill:**
  - `verify-<app>` sinh từ `create-verification-skill` (Phase 0): chạy app thật, đi theo feature map, thu thập bằng chứng, dọn dẹp mà không xóa bằng chứng.
  - `control-ui` (cursor-team-kit): harness browser/CDP cho web, IDE, Electron (screenshot, accessibility snapshot, console/network log, trace).
  - `control-cli` (cursor-team-kit): harness PTY cho CLI/TUI, gửi từng hành động rồi chờ một mẫu màn hình cụ thể mới gửi tiếp.
  - `verify-this` (cursor-team-kit): phát biểu claim ở dạng có thể bác bỏ, chụp baseline và treatment, so sánh artifact thô, trả đúng một kết quả: `VERIFIED`, `NOT VERIFIED`, `INCONCLUSIVE`.
  - `qa` / `qa-only` (gstack): QA bằng browser thật, và cả API, CLI, job, webhook. Bằng chứng before/after, và viết regression test trước khi sửa lỗi.
  - `principle-prove-it-works` (pstack): kiểm tra artifact thật, không kiểm tra proxy hay lời tự báo cáo.
  - `diagnosing-bugs` (Matt), khi verify phát hiện lỗi: dựng vòng phản hồi fail được, thu nhỏ, đặt giả thuyết, đo, sửa, thêm regression test.
- **[Đề xuất]** Lái cả các sub-feature lân cận trong feature map, và so tập bề mặt người dùng thấy được với phần ticket đã khai báo. Bề mặt mới xuất hiện ngoài khai báo là dấu hiệu tính năng thừa (mục 6).
- **Artifact:** thư mục bằng chứng (transcript, screenshot, log) và một kết luận VERIFIED / NOT VERIFIED / INCONCLUSIVE cho mỗi claim trong "kịch bản e2e" của ticket.
- **Cổng G7:** VERIFIED với bằng chứng nằm trong PR. Mọi thứ khác quay về Phase 5.
- **Xử lý:** P6 là chính, và kiểm chứng ngược P3.

### Phase 8. Ship & Learn

- **Mục tiêu:** đưa vào repo, và để lần sau agent ít sai hơn.
- **Skill:**
  - `pr` (Matt): thân PR gồm tóm tắt dạng hình nhỏ nhất đủ rõ, bằng chứng before/after, và nhận định một chiều hay hai chiều của thay đổi cùng blast radius.
  - `make-pr-easy-to-review` (cursor-team-kit): dọn lịch sử commit, mô tả PR, hướng dẫn cho reviewer.
  - `learn-from-mistakes` (Matt): sau session, đề xuất cải thiện **môi trường** của agent (con trỏ điều hướng, kiểm tra tự động, coding standards, tooling). Lỗi máy móc thành kiểm tra tất định, lỗi phán đoán thành coding standard cho `code-review`.
  - `correct` (pstack): gom nhóm các lỗi agent lặp lại (một nhóm tính khi đã xảy ra hai lần), rồi chặn ở tầng cao nhất khả thi: kiến trúc, rồi type, rồi lint, rồi test, và tài liệu là cuối cùng. Chứng minh mỗi kiểm tra mới fail trên một lỗi quá khứ có thật.
  - `show-me-your-work` (pstack), cho công việc dài hoặc chạy không giám sát: một file TSV, mỗi quyết định một dòng (what, why, evidence, result).
  - **[Đề xuất]** Cập nhật feature map cùng PR nếu bề mặt người dùng thay đổi.
- **Artifact:** PR, quy tắc/lint/test mới, cập nhật chuẩn code, feature map.
- **Xử lý:** P5 (phòng ngừa lâu dài), P2 (ghi lại quyết định).

---

## 5. Xuyên suốt: quản lý context (P7)

Đây là vấn đề được các bộ skill phủ yếu nhất, nên mô hình nhấn mạnh cơ chế bên ngoài skill.

| Quy tắc | Nguồn / trạng thái |
|---|---|
| Phase 1 đến 4 trong một context liền mạch; nếu gần smart zone thì `/compact` ở ranh giới phase | `ask-matt` (có sẵn) |
| Mỗi ticket ở Phase 5 trở đi là context mới (`/clear` hoặc subagent), đọc từ ticket + spec | `ask-matt`, `implement-spec` (có sẵn) |
| Ticket đủ nhỏ để vừa một context | `to-tickets` (có sẵn) |
| Chuyển giao giữa session bằng tài liệu: chỉ tham chiếu artifact đã có, không chép lại, lược bỏ bí mật | `handoff` (có sẵn) |
| Phân việc nhiều dữ liệu cho subagent, trong context chính chỉ giữ tóm tắt | `principle-guard-the-context-window` (có sẵn nhưng rất ngắn) |
| Lưu và khôi phục ngữ cảnh | `context-save` / `context-restore` (gstack) |
| **Không** chạy vòng lặp trong cùng session với prompt lặp lại | `ralph-loop` đi ngược nguyên tắc này, vì context tích lũy qua các lượt lặp |
| **[Đề xuất]** Đo mức dùng context và cảnh báo khi vào ~70–80% smart zone | Chưa skill nào làm; cần cơ chế như hook hoặc status line, không phải thêm hướng dẫn |
| **[Đề xuất]** Mỗi cuối phase ghi một dòng vào decision log (`show-me-your-work`) để agent context mới đọc lại được | Ghép từ hai skill có sẵn |

---

## 6. Feature map

### 6.1 Là gì và đang ở đâu trong mô hình

`create-verification-skill` (pstack) sinh thư mục `verify-<app>/features/`: một `README.md` làm chỉ mục và mỗi tính năng người dùng nhìn thấy một file riêng. Mỗi file có đúng 4 mục theo thứ tự:

| Mục | Nội dung |
|---|---|
| Sub-features | Các hành vi nhỏ, mỗi hành vi một ID ngắn (ví dụ `search-match`, `search-empty`) |
| How to get to it (user POV) | Mọi đường vào: nút trên toolbar, phím tắt, lệnh CLI |
| Driving it with `<harness>` | Điều kiện đầu và các bước; mỗi bước ghép hành động người dùng với lệnh chính xác và kết quả quan sát được. Chọn phần tử theo ARIA role và tên, không theo CSS hay vị trí |
| Gotchas | Các bẫy, ví dụ: nhấn `n` khi đang ở ô nhập thì gõ ra chữ `n` thay vì mở editor |

`maintain-verification-skill` giữ bản đồ đúng: mỗi tính năng một subagent đọc source, rồi một phiên chạy app thật lái từng tính năng, kết quả tối đa một PR sửa tài liệu và không bao giờ sửa code sản phẩm.

Ba loại "bản đồ" trong mô hình trả lời ba câu hỏi khác nhau, không thay được nhau:

| Artifact | Trả lời | Nguồn |
|---|---|---|
| `GLOSSARY.md` + ADR | Từ vựng và quyết định nào đã chốt? | Matt, `domain-modeling` |
| Sketch kiến trúc | Code được chia module và kiểu như thế nào? | pstack, `designing-architecture` |
| Feature map | Người dùng làm được gì, vào bằng đường nào, thao tác ra sao? | pstack, `create-verification-skill` |

### 6.2 Dùng ở đâu

| Phase | Việc với feature map |
|---|---|
| 0 Setup | Tạo; lập lịch `maintain-verification-skill` |
| 1 đến 2 | Đọc để biết cái đã có; spec dùng ID sub-feature |
| 4 Slice | Ticket ghi sub-feature sẽ thêm/sửa; kịch bản e2e lấy từ file tính năng |
| 7 Verify | Lái tính năng bị ảnh hưởng và các sub-feature lân cận; so bề mặt xuất hiện với phần ticket đã khai báo |
| 8 Ship | Cập nhật bản đồ cùng PR |

### 6.3 Tác động đến code thừa (giả thuyết, chưa có số liệu)

Feature map được thiết kế để kiểm chứng, không phải để kiềm chế code thừa. Các tác động dưới đây là suy luận.

- **Có thể giúp:**
  - Phát hiện **tính năng thừa nhìn thấy được**: bề mặt mới không có trong bản đồ và không có trong ticket.
  - Cho ticket một **ngôn ngữ phạm vi**: "chỉ sửa `search-match`, các sub-feature khác của search không đổi", và Phase 7 kiểm tra các tính năng lân cận.
  - Giảm **làm lại cái đã có** ở mức tính năng. Bản đồ mô tả hành vi, không chỉ chỗ code nằm đâu; muốn tránh trùng code cần `how` hoặc `blast-radius` (pstack).
- **Không giúp được:**
  - **Phần thừa bên trong code** (abstraction, wrapper, tham số tùy chọn, validation thừa): một tính năng chạy qua 13 dòng hay qua ba lớp trừu tượng đều pass cùng một kịch bản trên giao diện. Phần này do mục 7 xử lý.
- **Rủi ro:** bản đồ cũ làm agent tin vào mô tả sai và sinh cảnh báo giả. Có chi phí duy trì; với repo nhỏ hoặc thay đổi nhanh, chi phí này có thể lớn hơn lợi ích.

---

## 7. Kiểm soát code thừa và over-engineering (P4, P5)

### 7.1 Vấn đề

Hai chiều, nguyên nhân khác nhau:

- **Việc đơn giản mà agent viết thêm nhiều thứ.** Agent muốn "làm cho tử tế": thêm validation, option, log, xử lý lỗi, test cho đường chưa ai yêu cầu. Lời dặn "đừng" thường không đủ, vì với agent mỗi thứ thêm vào đều có lý do.
- **Việc giản dị mà agent làm phức tạp.** Agent không thấy toàn repo nên tự dựng abstraction thay vì dùng cái có sẵn hoặc sửa tại chỗ, và hay chọn cấu trúc "chuẩn sách giáo khoa" mà bài toán không cần.

Các skill hiện có xử lý chủ yếu **sau khi code đã viết**: `tdd` dặn "chỉ đủ để pass", `code-review` trục Spec báo scope creep, `deslop` gỡ slop. Lúc đang code gần như chỉ có lời dặn. Thiết kế ticket kiểu tracer-bullet còn có thể làm tệ hơn nếu agent hiểu là phải dựng đủ các tầng.

### 7.2 Sáu tầng kiểm soát

| Tầng | Cơ chế | Thời điểm | Nguồn / trạng thái | Mức bằng chứng |
|---|---|---|---|---|
| 0 | `scope.json` theo ticket: file được sửa, file cấm, "không làm", thay đổi feature map dự kiến | Trước khi code | Cộng đồng khuyên prompt có phạm vi; bài OverEager cho thấy khai báo phạm vi giảm hành động ngoài phạm vi. **[Đề xuất]** định dạng file | Có số liệu, nhưng chỉ cho hành động ngoài phạm vi (xóa file, đổi config) |
| 1 | Hook PreToolUse chặn hoặc hỏi khi sửa ngoài danh sách | Lúc agent sửa file | Cơ chế có trong tài liệu hooks. **[Đề xuất]** thiết kế hook | Cơ chế đã xác minh; hiệu quả chưa đo |
| 2 | Kiểm tra máy móc sau khi sửa: lint, type, kiểu thừa lặp lại | Sau mỗi lần sửa | HumanLayer, gstack `slop:diff` (chỉ cảnh báo), pstack `correct` | Là hướng đi, chưa có số liệu |
| 3 | Hook Stop so `git diff` với `scope.json` | Khi agent định kết thúc | Cơ chế có trong tài liệu (một số chi tiết mới ở mức tóm tắt). **[Đề xuất]** nội dung kiểm tra | Chưa đo |
| 4 | Review trong ngữ cảnh mới | Sau khi code xong | Codersera; Matt `code-review`, `learn-from-mistakes`; pstack `minimize-reader-load`; cursor `deslop` | Đồng thuận cộng đồng, không có đo lường |
| 5 | Phòng ngừa bằng cấu trúc | Thiết kế | pstack `correct`, `boundary-discipline`; Matt `codebase-design`, `tdd` | Không có số liệu |
| 6 | Giữ file chỉ dẫn ngắn | Cấu hình | Bài AGENTS.md (ETH Zurich), HumanLayer | Có số liệu |

### 7.3 Chi tiết từng tầng

**Tầng 0. Hợp đồng phạm vi.** **[Đề xuất]** `scope.json` mẫu:

```json
{
  "ticket": "search-match-fix",
  "allowed": ["src/search/match.ts", "src/search/match.test.ts"],
  "forbidden": ["package.json", "package-lock.json", "src/config/**"],
  "not_doing": ["Không đổi cách xếp hạng kết quả", "Không thêm tùy chọn mới"],
  "feature_map_delta": ["search-match: sửa"]
}
```

Bài OverEager cảnh báo agent có thể chỉ khớp mẫu đoạn khai báo chứ không hiểu giới hạn, nên tầng này không đứng một mình.

**Tầng 1. Hook PreToolUse.** Theo tài liệu hooks: hook nhận JSON qua stdin; với `Write` và `Edit`, `tool_input.file_path` luôn là đường dẫn tuyệt đối; thoát mã 2 thì chặn lệnh gọi và stderr đến tay Claude; hoặc xuất JSON với `permissionDecision` là `allow`, `deny` hoặc `ask` kèm lý do; matcher viết như `Edit|Write`. Thiết kế đề xuất:

| Tình huống | Quyết định |
|---|---|
| Sửa file trong `allowed` | Không có quyết định, đi theo luồng quyền thông thường |
| Tạo file mới hoặc sửa file ngoài `allowed` | `ask`: agent nêu lý do, người duyệt (bắt chước kiểu ask-to-continue của OpenHands trong bài OverEager) |
| Chạm file trong `forbidden` | `deny` kèm lý do cụ thể |

Hạn chế:
- Hook này chỉ chặn `Edit` và `Write`. Agent vẫn ghi file được qua Bash (`sed -i`, chuyển hướng `>`). Muốn chặn kín cần hook cho `Bash` hoặc chạy trong sandbox.
- Tài liệu tôi lấy được không có mục cho `MultiEdit`.
- Đây là cơ chế đã xác minh về mặt kỹ thuật, nhưng chưa ai chứng minh nó giảm code thừa.

**Tầng 2. Kiểm tra máy móc.** pstack `correct` chặn lỗi lặp ở tầng cao nhất khả thi (kiến trúc > type > lint > test > docs), lint phải có thông báo nêu rõ dùng gì thay thế, và nếu mẫu xấu đã phổ biến thì chỉ fail khi thay đổi **thêm** mẫu đó. **[Đề xuất]** các kiểm tra nhắm vào kiểu thừa của agent: tham số và export không dùng, hàm bọc chỉ một nơi gọi, file mới không được import, `catch` rỗng hoặc nuốt lỗi, dependency mới trong manifest. gstack `reviewing-changes` có slop scan tìm `catch` rỗng, `return await` thừa và abstraction không cần thiết, nhưng chỉ ở mức cảnh báo, không chặn.

**Tầng 3. Hook Stop.** Theo tài liệu, hook Stop có thể ngăn Claude dừng và buộc tiếp tục bằng `decision: "block"` kèm lý do. Chi tiết chống lặp vô hạn (`stop_hook_active`, giới hạn 8 lần tiếp tục liên tiếp) mới có ở bản tóm tắt, cần kiểm tra lại trên trang gốc. **[Đề xuất]** hook so `git diff` với `scope.json`: file nào chạm ngoài danh sách, file nào mới, số dòng đổi so với dự kiến, dependency mới. Có sai lệch thì agent phải chọn: hoàn tác phần đó, hoặc giải thích vì sao ticket thiếu sót để người duyệt. Đây là cách biến quy tắc "mỗi dòng thay đổi phải truy ngược về yêu cầu" (có trong nhiều bài cộng đồng và trong `karpathy-guidelines` dưới dạng "Every changed line should trace directly to the user's request", đều chỉ ở dạng lời dặn) thành cơ chế.

**Tầng 4. Review ngữ cảnh mới.** Codersera khuyên một phiên riêng đọc diff tìm phần thừa; tài liệu `learn-from-mistakes` của Matt lập luận chuẩn code thuộc về reviewer vì agent đang code chịu áp lực context nhiều nhất. pstack `minimize-reader-load` cho phép thử: người đọc mới trả lời được "X đến từ đâu, cái gì đổi được X" trong 30 giây không. `deslop` (cursor) gỡ comment thừa, try/catch lạ, ép kiểu `any`, nhưng không nhắm vào việc thêm tính năng.

**Tầng 5. Cấu trúc.**
- pstack `boundary-discipline`: kiểm tra và xử lý lỗi tập trung ở ranh giới hệ thống, bên trong tin vào type. Nguyên tắc này chặn phòng thủ rải rác mà vẫn giữ kiểm tra an toàn ở nơi cần.
- Matt `codebase-design`: "một adapter là seam giả định, hai adapter mới là seam thật".
- Matt `tdd`: chỉ viết đủ code để test fail chuyển sang pass.
- pstack `subtract-before-you-add`, `laziness-protocol`: giảm trước khi thêm, diff nhỏ nhất.

**Tầng 6. File chỉ dẫn ngắn.** Bài AGENTS.md cho thấy file ngữ cảnh nhìn chung không cải thiện tỷ lệ thành công và tăng chi phí suy luận trên 20%. Hàm ý: quy tắc theo ticket đặt trong ticket (tầng 0), quy tắc lặp lại chuyển thành lint (tầng 2), đừng nhồi hàng chục quy tắc "đừng over-engineer" vào CLAUDE.md.

### 7.4 Hai lưu ý ngược chiều

- **Đừng bắt viết ít đến mức bỏ kiểm tra an toàn.** Một bài cộng đồng kể bài kiểm tra mà prompt "chỉ viết một dòng" bỏ sót lớp bảo vệ path-traversal. Quy tắc "ít code nhất" cần ghi kèm "giữ kiểm tra an toàn tại ranh giới". `karpathy-guidelines` có dòng "No error handling for impossible scenarios" mà không kèm ngoại lệ này; pstack `boundary-discipline` là phần bổ sung còn thiếu (mục 9.5).
- **Lập kế hoạch trước không đồng nghĩa diff nhỏ hơn.** Bài CodeTaste cho thấy plan mode nâng độ khớp với refactoring của con người, nhưng theo bản tóm tắt diff to hơn khoảng 2 đến 3 lần và tỷ lệ pass có lúc giảm. Cần cả tầng 1 và 3 để kiểm soát lượng code.

### 7.5 Đề xuất thử nghiệm

Chưa có nghiên cứu nào đo trực tiếp việc giảm code thừa của các biện pháp này. Nên thử tầng 0, 1 và 3 trên khoảng 10 ticket thật và đo: số lần chạm file ngoài danh sách, số dòng diff so với dự kiến, số dòng bị loại ở bước review. Chỉ sau đó mới đưa vào quy trình mặc định.

---

## 8. Ma trận vấn đề × phase × skill

`●` là chính, `○` là phụ.

| Phase | P1 Giả định | P2 Kiến trúc | P3 Test | P4 Quá nhiều code | P5 Slop | P6 E2E | P7 Context |
|---|---|---|---|---|---|---|---|
| 0 Setup | ○ | ○ | | | ○ | ● | |
| 1 Brainstorm | ● | ○ | | | | | ○ |
| 2 Spec | ● | | ○ | | | | |
| 3 Architecture | | ● | | | ○ | | |
| 4 Slice | | | | ● | | ○ | ● |
| 5 Implement | | | ● | ● | ○ | | ○ |
| 6 Review | | | ● | ○ | ● | | |
| 7 Verify e2e | | | ○ | | | ● | |
| 8 Ship & Learn | | ○ | | | ● | | ○ |

---

## 9. Nghiên cứu các skill trong `reference/`

### 9.1 Năm bộ và triết lý của chúng

| Bộ | Tác giả | Triết lý | Điểm mạnh nhất | Điểm yếu nhất |
|---|---|---|---|---|
| **skills_matt** | Matt Pocock | Nhỏ, ghép được, không sở hữu quy trình. Nền tảng là kỹ thuật phần mềm cơ bản (shared language, feedback loop, deep module) | Luồng liền mạch `grill → spec → tickets → implement → review`; xử lý rất sâu P1, P3, P4 | Gần như không có e2e thật; quản lý context chỉ ở mức khuyến nghị |
| **gstack** | Garry Tan | "Đội ngũ ảo" với các vai trò (CEO, eng manager, designer, QA, security, release); skill dài, có nhiều bước tiền xử lý | QA bằng browser thật và nhiều loại bề mặt; spec và review rất chi tiết; có bộ phát hiện slop UI | Skill rất dài (nhiều skill 500–900 dòng, phần lớn là preamble dùng chung); gắn với hạ tầng gstack, và hướng dẫn cài đặt đòi dùng browser riêng của nó thay vì tool khác |
| **plugins/pstack** | Lauren Tan | "Đi sâu trước khi đi nhanh": nguyên tắc nhỏ (`principle-*`) cộng playbook; mã hóa bài học vào cấu trúc | Mã hóa bài học (`correct`), tạo skill xác minh cho từng repo, `designing-architecture` | Nhiều skill là nguyên tắc rất ngắn, ít chỉ dẫn thao tác; một số mặc định chạy không dừng chờ người |
| **plugins/cursor-team-kit** | Cursor | Bộ tiện ích cho đội: CI, review, ship, harness chạy thử | Harness UI/CLI cụ thể; `verify-this` có định dạng kết luận rõ | Thiên về thao tác (CI, PR), không có khâu hiểu yêu cầu hay kiến trúc |
| **andrej-karpathy-skills** | Cộng đồng (`forrestchang` theo `plugin.json`), rút ra từ một bài đăng của Andrej Karpathy | Không phải quy trình mà là bốn nguyên tắc ứng xử viết một lần cho mọi tác vụ code; chủ động "thiên về cẩn trọng hơn tốc độ" | Nhỏ nhất trong năm bộ (~65 dòng); nhắm đúng lỗi hành vi gốc: giả định ngầm, làm quá, sửa lan, "xong" không có tiêu chí; không gắn hạ tầng nào | Chỉ là lời dặn: không artifact, không cổng, không công cụ cưỡng chế; không phủ e2e, kiến trúc hay context |

`skill-creator` chỉ dùng để viết/đánh giá skill, nằm ngoài mô hình session.

### 9.2 Bảng so sánh theo từng skill

Cột "Gọi bởi": **U** = chỉ người dùng gõ (frontmatter có `disable-model-invocation: true`); **M** = agent có thể tự gọi (không có cờ đó). Đã đối chiếu frontmatter của từng skill trong bảng, trừ các skill gstack (xem ghi chú ở mục 11).

| Skill | Bộ | Phase | Vấn đề | Làm gì | Mạnh | Hạn chế | Gọi bởi |
|---|---|---|---|---|---|---|---|
| `grill-with-docs` | Matt | 1 | P1, P2 | Phỏng vấn dai dẳng; ghi glossary và ADR ngay khi hỏi | Giải quyết giả định tận gốc; sinh từ vựng chung giúp giảm dài dòng | Không tạo artifact user journey riêng | U |
| `grilling` | Matt | 1 | P1 | Primitive phỏng vấn tái sử dụng | Ghép được vào nhiều skill khác | Chỉ là kỹ thuật, không tạo tài liệu | M |
| `in-your-own-words` | pstack | 1 | P1 | Agent diễn đạt lại mục tiêu của bạn | Bắt hiểu sai rất rẻ | Rất ngắn, không có cấu trúc | U |
| `prototyping-designs` | Matt | 1, 3 | P1, P2 | Code vứt đi để trả lời một câu hỏi (HTML logic hoặc nhiều biến thể UI) | Trả lời bằng thứ chạy được thay vì tranh luận | Chỉ dùng khi câu hỏi cần chạy thử | M |
| `research` | Matt | 1 | P1 | Điều tra từ nguồn chính thống, ghi vào Markdown có trích dẫn, chạy nền | Không làm đầy context chính | Chỉ thu thập sự thật | M |
| `to-spec` | Matt | 2 | P1 | Tổng hợp hội thoại thành spec, có user stories và seam | Gắn seam test vào spec, khớp `tdd` | Không phỏng vấn (phụ thuộc phase 1 đã làm tốt) | U |
| `spec-it` | gstack | 2 | P1, P3 | Spec 5 phase, hỏi "vì sao", đọc code rồi mới tra vấn kỹ thuật | Rất đầy đủ: acceptance criteria, rollback, out of scope | Dài, gắn với hạ tầng gstack | M |
| `domain-modeling` | Matt | 1, 3 | P2 | Làm sắc từ vựng và ghi ADR | Giữ nhất quán tên gọi trong code | Cần duy trì liên tục | M |
| `codebase-design` | Matt | 3 | P2, P5 | Từ vựng deep module, seam, deletion test | Cho ngôn ngữ chung để thảo luận kiến trúc | Là tài liệu tham chiếu, không tự tạo artifact | M |
| `designing-architecture` | pstack | 3 | P2 | Phác kiểu, signature, module với body `not implemented`; nhiều ứng viên | Sketch là hợp đồng; có điều kiện bỏ sketch | Mặc định không dừng chờ duyệt; phụ thuộc skill `how`, `why`, `arena` | U |
| `plan-eng-review` | gstack | 3 | P2 | Review kế hoạch kiến trúc, có sơ đồ | Bắt buộc cập nhật sơ đồ cùng code | Skill dài, gắn gstack | M |
| `improve-codebase-architecture` | Matt | 3 | P2, P5 | Quét cơ hội làm module sâu hơn, báo cáo HTML | Nhắm vào phần code vừa thay đổi | Khảo sát, không dọn nợ cũ hộ | U |
| `to-tickets` | Matt | 4 | P4, P7 | Cắt tracer-bullet ticket có cạnh chặn | Ticket vừa một context; có xử lý expand–contract | Dễ cắt quá vụn (tài liệu của skill thừa nhận) | U |
| `wayfinder` | Matt | 4 | P4, P7 | Bản đồ ticket quyết định cho việc quá lớn | Chia việc lớn thành nhiều session | Chỉ lập kế hoạch, không thực thi | U |
| `sequence-verifiable-units` | pstack | 4, 5 | P4 | Mỗi đơn vị kết thúc ở trạng thái kiểm tra được | Thứ tự commit tự chứng minh | Nguyên tắc, không có thao tác cụ thể | U |
| `blast-radius` | pstack | 4 | P4, P5 | Tìm chỗ khác có thể vỡ, chứng minh bằng chạy thật | Nhìn ra ngoài diff | - | U |
| `implementing-tickets` | Matt | 5 | P4 | Một ticket: tdd, typecheck, code-review, commit | Gọn, rõ thứ tự | Chạy trong một agent đơn | U |
| `implement-spec` | Matt | 5 | P4, P7 | Cả spec trên một nhánh tích hợp bằng subagent song song | Song song tối đa, context sạch cho mỗi ticket | Phức tạp hơn; cần tracker | U |
| `tdd` | Matt | 5 | P3 | Red→green theo slice dọc, test ở seam đã duyệt | Chống test tautological và test dính implementation | Refactor bị đẩy sang review | M |
| `tdd` | pstack | 5 | P3 | Chỉ khi người dùng yêu cầu hoặc có đích test rẻ | Tránh ép TDD khi không hợp | Không phải mặc định | U |
| `test-behavior-not-implementation` | pstack | 5, 6 | P3 | Phép thử hai chiều cho từng test | Tiêu chí kiểm chứng test rõ ràng nhất | Nguyên tắc, agent phải tự áp dụng | U |
| `test-audit` | gstack | 6 | P3, P5 | Quét test giá trị thấp, trùng, và code chỉ để phục vụ test đó | Dọn test rác | Skill dài | M |
| `code-review` | Matt | 6 | P5, P3 | Hai trục Standards + Spec song song; baseline Fowler | Hai trục không che nhau; bắt scope creep | Cần có spec; chuẩn repo phải được viết sẵn | M |
| `reviewing-changes` | gstack | 6 | P5 | Review trước khi land; scope drift, slop scan | Có công cụ quét tự động | Slop scan chỉ là cảnh báo không chặn | M |
| `review-and-ship` | cursor | 6, 8 | P5 | Review, chạy test, commit, mở PR | Gọn | Chung chung hơn các bộ trên | M |
| `deslop` | cursor | 6 | P5 | Gỡ slop so với main | Cụ thể, ngắn | Chỉ xử lý sau khi code đã viết | M |
| `deslop-shared-libs` | gstack | 6 | P5 | Tìm chỗ gom code dùng chung | Chống trùng lặp ngang diff | Chỉ đọc, đề xuất | M |
| `correct` | pstack | 8 | P5 | Biến lỗi lặp thành cơ chế (kiến trúc > type > lint > test > docs) | Phòng ngừa lâu dài, bắt buộc chứng minh | Cần lịch sử lỗi để khai thác | U |
| `create-verification-skill` | pstack | 0, 7 | P6 | Sinh skill chạy thử app thật cho repo | Tạo tài sản dùng lại; bắt buộc chạy thử | Tốn công ban đầu | U |
| `control-ui` | cursor | 7 | P6 | Harness browser/CDP | Bằng chứng screenshot, a11y snapshot, trace | Cần dựng harness nếu repo chưa có | M |
| `control-cli` | cursor | 7 | P6 | Harness PTY cho CLI/TUI | Gửi từng hành động, chờ mẫu màn hình | Như trên | M |
| `verify-this` | cursor | 7 | P6, P3 | Claim bác bỏ được, baseline vs treatment, 3 kết luận | Kết luận rõ ràng, không "chắc là ổn" | Cần claim đo lường được | M |
| `qa` / `qa-only` | gstack | 7 | P6 | QA bằng browser/API/CLI/job/webhook; regression test trước khi sửa | Nhiều bề mặt; bằng chứng before/after | Gắn gstack browse | M |
| `principle-prove-it-works` | pstack | 7 | P6 | Kiểm chứng artifact thật | Nguyên tắc đúng | Rất ngắn | U |
| `diagnosing-bugs` | Matt | 7 | P3, P6 | Vòng debug có cổng từng bước | Bắt đầu từ vòng phản hồi fail được | Dành cho bug, không phải kiểm chứng tính năng | M |
| `pr` | Matt | 8 | P4 | Định dạng thân PR có evidence và nhận định blast radius | Giúp reviewer duyệt nhanh | Chỉ là định dạng | M |
| `learn-from-mistakes` | Matt | 8 | P5, P2 | Đề xuất cải thiện môi trường agent | Sửa nguyên nhân, không sửa triệu chứng | Cần log session | U |
| `show-me-your-work` | pstack | 8 | P7 | Nhật ký quyết định TSV | Cho phép người xem lại việc chạy không giám sát | Thêm chi phí ghi chép | U |
| `handoff` | Matt | giữa phase | P7 | Nén hội thoại thành tài liệu cho agent mới | Không chép lại những gì đã có artifact | Phụ thuộc chất lượng tóm tắt | U |
| `context-save` / `restore` | gstack | giữa phase | P7 | Lưu/khôi phục ngữ cảnh | Tiếp tục việc dở | Gắn gstack | M |
| `guard-the-context-window` | pstack | xuyên suốt | P7 | Đẩy dữ liệu lớn cho subagent | Hướng đúng | Chỉ vài dòng | U |
| `karpathy-guidelines` | Karpathy | xuyên suốt (chủ yếu 5, 6) | P5, P4, P1, P3 | Bốn nguyên tắc: nêu giả định và hỏi khi mơ hồ; code tối thiểu; sửa đúng chỗ cần; đổi việc thành mục tiêu kiểm chứng được | Rất ngắn; có phép thử dễ nhớ ("mỗi dòng đổi truy được về yêu cầu"); dùng được qua SKILL.md, CLAUDE.md hoặc rule Cursor; kèm 9 ví dụ sai/đúng | Chỉ là lời dặn, không cưỡng chế; "ngắn gọn" do agent tự đánh giá sau khi viết; không phủ P2, P6, P7; "hỏi khi chưa chắc" ngược `never-block-on-the-human` của pstack (mục 9.5) | M |
| `ralph-loop` | cursor | không dùng | P7 (ngược) | Nạp lại cùng prompt mỗi lượt | Tự lặp tới khi hoàn thành | Context tích lũy trong cùng session, đi ngược P7 | M |

### 9.3 So sánh các nhóm skill cùng chức năng

**Spec: `to-spec` (Matt) và `spec-it` (gstack)**

| Tiêu chí | `to-spec` | `spec-it` |
|---|---|---|
| Phỏng vấn | Không, chỉ tổng hợp | Có, 5 phase |
| Seam test | Có, phải được bạn xác nhận | Có Testing Pyramid và Testing Plan |
| Phần khác | User stories dài | Rollback, effort, dependency graph, "do not touch" |
| Phù hợp khi | Đã grill xong ở phase 1 | Cần spec rất đầy đủ để giao cho người khác |

**Kiến trúc: `codebase-design`, `designing-architecture`, `plan-eng-review`**

| Tiêu chí | `codebase-design` | `designing-architecture` | `plan-eng-review` |
|---|---|---|---|
| Loại | Từ vựng và nguyên tắc | Quy trình tạo sketch | Review kế hoạch |
| Đầu ra | Không | Sketch kiểu/signature | Nhận xét, sơ đồ |
| Cổng duyệt | Không | Tắt mặc định | Có hỏi tương tác |
| Dùng khi | Nền chung | Việc không tầm thường, tránh khóa sai hình dạng | Đã có kế hoạch |

**Review: `code-review`, `reviewing-changes`, `review-and-ship`**

| Tiêu chí | Matt `code-review` | gstack `reviewing-changes` | cursor `review-and-ship` |
|---|---|---|---|
| Trục | Standards + Spec tách biệt | Gộp, có scope drift | Đúng sai, ý định, test |
| Song song | Có, subagent | - | Có với diff lớn |
| Slop | Baseline Fowler | Slop scan | Không riêng |
| Đi kèm | - | Nhiều bước land | Commit, PR |

**E2E: `create-verification-skill`, `control-ui`/`control-cli`, `qa`, `verify-this`**

| Tiêu chí | `create-verification-skill` | `control-ui` / `control-cli` | `qa` | `verify-this` |
|---|---|---|---|---|
| Vai trò | Tạo tài sản chạy thử cho repo | Công cụ lái UI/CLI | Quy trình QA tìm và sửa lỗi | Khung kết luận cho một claim |
| Bề mặt | Mọi bề mặt (do repo quyết định) | Web/Electron; CLI/TUI | Browser, API, CLI, job, webhook | Mọi bề mặt có thể đo |
| Kết luận | Bằng chứng theo feature map | Screenshot, trace, transcript | Before/after, regression test | VERIFIED / NOT VERIFIED / INCONCLUSIVE |
| Dùng cùng nhau | Sinh `verify-<app>` | Làm lõi cho phần "Drive" | Khi muốn chạy QA rộng | Làm khung kết luận cho từng claim |

**Chống slop: `deslop`, `deslop-shared-libs`, `correct`**

| Tiêu chí | `deslop` | `deslop-shared-libs` | `correct` |
|---|---|---|---|
| Thời điểm | Sau khi viết | Sau khi viết | Sau nhiều session |
| Hành động | Xóa slop trong diff | Đề xuất gom code chung | Chặn lỗi lặp bằng kiến trúc/type/lint/test |
| Phòng ngừa | Không | Không | Có |

**Context: `handoff`, `context-save`, `guard-the-context-window`, `ralph-loop`**

| Tiêu chí | `handoff` | `context-save` | `guard-the-context-window` | `ralph-loop` |
|---|---|---|---|---|
| Cách xử lý | Chuyển sang agent mới bằng tài liệu | Lưu và khôi phục | Đẩy khối lượng lớn cho subagent | Lặp lại cùng prompt |
| Hợp với P7 | Có | Có | Có (rất ngắn) | Ngược lại |

**Hiểu yêu cầu trước khi code: "Think Before Coding" (`karpathy-guidelines`), `in-your-own-words`, `grilling` / `grill-with-docs`**

| Tiêu chí | Think Before Coding | `in-your-own-words` | `grilling` / `grill-with-docs` |
|---|---|---|---|
| Cách làm | Agent tự nêu giả định, liệt kê các cách hiểu, hỏi khi mơ hồ | Agent diễn đạt lại mục tiêu và vấn đề | Phỏng vấn nhiều vòng trên cây quyết định, mỗi câu kèm đáp án đề xuất |
| Điều kiện kết thúc | Không có, agent tự phán đoán | Bạn xác nhận hoặc sửa | Hết nhánh chưa giải quyết và bạn xác nhận đã hiểu chung |
| Artifact | Không | Không | Có với `grill-with-docs` (glossary, ADR) |
| Phù hợp khi | Mỗi tác vụ code, nhất là việc nhỏ chưa đáng grill | Kiểm tra nhanh, rẻ | Phase 1 của việc mới hoặc lớn |

**Giữ phạm vi và chống làm thừa: `karpathy-guidelines`, nhóm `principle-*` của pstack, `scope.json` + hook [Đề xuất]**

| Tiêu chí | `karpathy-guidelines` | pstack `principle-*` (`subtract-before-you-add`, `laziness-protocol`, `boundary-discipline`, `never-block-on-the-human`) | `scope.json` + hook [Đề xuất] |
|---|---|---|---|
| Loại | Bốn nguyên tắc, lời dặn | Các nguyên tắc ngắn (10 đến 34 dòng), lời dặn | Cơ chế cưỡng chế, chưa xây |
| Thước đo phạm vi | "Mỗi dòng đổi truy được về yêu cầu" | "Thay đổi nhỏ nhất giải quyết được vấn đề" | Danh sách file được sửa, file cấm, "không làm" |
| Code chết có sẵn | Chỉ nhắc, không xóa trừ khi được yêu cầu | Xóa trước khi thêm | Do ticket quyết định |
| Khi mơ hồ | Dừng và hỏi | Làm rồi trình bày với việc đảo ngược được; chỉ hỏi với việc không đảo ngược được | `ask` khi sửa ngoài danh sách |
| Kiểm tra an toàn | "Không xử lý lỗi cho tình huống bất khả thi", không nêu ngoại lệ ở ranh giới | Tập trung kiểm tra ở ranh giới hệ thống | Không đề cập |
| Gọi bởi | M | U | Hook, không phải skill |

### 9.4 Nghiên cứu bên ngoài về code thừa

Nguồn tìm trên web, không nằm trong `reference/`. Hầu hết là bài viết thứ cấp; số liệu trong bảng bài báo đến từ báo cáo của agent đọc bài, trong đó con số ở abstract được trích nguyên văn còn số trong bảng và các mục sâu hơn là bản tóm tắt do mô hình sinh ra, cần đối chiếu PDF trước khi trích đi nơi khác.

| Nguồn | Loại | Phát hiện chính | Giới hạn |
|---|---|---|---|
| [Overeager Coding Agents, arXiv 2605.18583](https://arxiv.org/abs/2605.18583) | Bài báo, 500 kịch bản, ~7.500 lượt chạy | Bỏ đoạn khai báo phạm vi thì tỷ lệ làm ngoài phạm vi của Claude Code tăng từ 0,0% lên 17,1%. Nhóm framework dễ dãi 5,4–27,7%; OpenHands (dừng hỏi để tiếp tục) 0,2–4,5% | Đo hành động ngoài phạm vi (xóa file, đổi config), không đo code thừa. Không đề xuất hay thử biện pháp phòng thủ. So sánh giữa framework là quan sát chéo |
| [Evaluating AGENTS.md, arXiv 2602.11988](https://arxiv.org/abs/2602.11988) | Bài báo, ETH Zurich | File ngữ cảnh nhìn chung không cải thiện tỷ lệ thành công, tăng chi phí trên 20%. File người viết hơn file LLM sinh khoảng 7% | Không thử riêng quy tắc kiểu "đừng over-engineer" |
| [CodeTaste, arXiv 2603.04177](https://arxiv.org/abs/2603.04177) | Bài báo, 100 instance | Plan mode nâng độ khớp refactoring nhưng diff to hơn 2–3 lần (tóm tắt) | Câu "agent tích lũy độ phức tạp" chỉ là lời dẫn, bài không đo điều đó |
| [Codersera](https://codersera.com/blog/how-to-stop-claude-code-over-engineering-2026/), [MCP.Directory](https://mcp.directory/blog/stop-claude-code-over-engineering-2026) | Blog | Quy tắc "thay đổi nhỏ nhất", ngưỡng dừng, plan mode, review bằng phiên mới | Không có số liệu đo. Con số "ít hơn ~54% code" là tự báo cáo từ một bài Reddit chưa kiểm chứng |
| [andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) | Repo cộng đồng; đã có bản trong `reference/andrej-karpathy-skills`, đánh giá ở mục 9.5 | Bốn nguyên tắc: Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution | Không có số liệu hiệu quả (README chỉ nêu dấu hiệu định tính). Karpathy là nguồn ý tưởng (README trích một bài đăng trên X, tôi chưa đọc bài gốc), không phải tác giả repo: `plugin.json` ghi `forrestchang`, còn git remote của bản local là `multica-ai/andrej-karpathy-skills`; chưa xác minh quan hệ giữa hai tài khoản |
| [HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md) | Blog | CLAUDE.md ngắn; dùng linter và hook thay vì lời dặn | Số liệu tự báo cáo |
| [Hooks reference](https://code.claude.com/docs/en/hooks) | Tài liệu chính thức | Cơ chế chặn (PreToolUse), phản hồi (PostToolUse), giữ agent làm tiếp (Stop) | Phần Stop và PostToolUse mới ở mức tóm tắt; không có mục `MultiEdit` |

Điều chưa tìm thấy: không có nghiên cứu độc lập nào đo trực tiếp "agent viết thừa code" hay "làm phức tạp quá mức" rồi so sánh các biện pháp; chưa xác minh trang hướng dẫn prompt chính thức của Anthropic.

### 9.5 Đánh giá `andrej-karpathy-skills`

**Là gì.** Một skill duy nhất, `karpathy-guidelines` (SKILL.md 67 dòng), phát hành thành bốn bản cùng nội dung: SKILL.md cho plugin Claude Code, `CLAUDE.md` để chép vào repo, rule Cursor `alwaysApply: true`, và phần giải thích trong README. Các bản chỉ khác dòng "These guidelines are working if" ở cuối. `EXAMPLES.md` (522 dòng) có 9 cặp ví dụ sai/đúng. Bộ này không có quy trình, artifact, hook hay script.

**Đối chiếu từng nguyên tắc với bảy vấn đề.**

| Nguyên tắc | Vấn đề | Chỗ tương ứng trong mô hình | Đánh giá |
|---|---|---|---|
| Think Before Coding | P1 (một phần) | Phase 1, bản nhẹ của `grilling` và `in-your-own-words` | Chặn giả định ngầm ngay trong từng tác vụ code. Nhưng giả định ở đây là về phạm vi và định dạng (ví dụ "export user data" hỏi về trường dữ liệu, nơi lưu), không phải user journey. Không có artifact, không có điều kiện kết thúc, nên không thay được G1 |
| Simplicity First | P5, P4 | Tầng 5, 6 (lời dặn) | Trúng đích nhất: liệt kê đúng các kiểu thừa ở mục 7.1 (tính năng không ai yêu cầu, abstraction cho code dùng một lần, cấu hình thừa). Ví dụ `DiscountStrategy` so với một hàm hai dòng minh họa rõ. Điểm yếu: "200 dòng mà 50 là đủ thì viết lại" chỉ phát hiện sau khi đã viết, và do chính agent đánh giá |
| Surgical Changes | P5, P4 | Tầng 0 và 3 dưới dạng văn xuôi | Là phiên bản bằng lời của `scope.json`: mỗi dòng đổi phải truy được về yêu cầu, không "cải thiện" code kế bên, dọn đồ mồ côi do chính mình tạo ra. Thiếu danh sách file cụ thể và không có gì chặn khi vi phạm |
| Goal-Driven Execution | P3 (một phần) | Phase 5 (`tdd`), `sequence-verifiable-units` | Đổi "việc" thành "mục tiêu có kiểm tra" rất gọn; mẫu `[Bước] → verify: [kiểm tra]` ghép được vào ticket. Nhưng "kiểm tra" chỉ là test hoặc `curl` thủ công: không phân biệt test tốt/xấu, không e2e như người dùng thật (P6) |

Giới hạn của nguyên tắc thứ tư tự lộ ở Ví dụ 3 của `EXAMPLES.md` (sorting): đoạn "sai" và đoạn "đúng" dùng cùng một lời gọi `sorted(scores, key=lambda x: (-x['score'], x['name']))`, `sorted` của Python tất định, và test trong ví dụ chỉ assert điểm theo thứ tự giảm dần, nên test sẽ pass ngay trước khi sửa. Ví dụ này khẳng định "fails with inconsistent ordering" mà không có bước red thật. Quy tắc "red before green" của `tdd` (Matt) được viết ra để bắt đúng trường hợp này.

**Điểm mạnh.**
- Nhỏ (~65 dòng) và nhắm vào vài lỗi hành vi lặp lại, khớp nguyên tắc 8 (giữ chỉ dẫn chung ngắn) và tầng 6.
- Không gắn tracker, đường dẫn artifact hay hạ tầng nào, nên không thêm xung đột quy ước ở mục 10.10.
- Tự giới hạn phạm vi: "Tradeoff... For trivial tasks, use judgment", tránh biến mỗi lần sửa typo thành một nghi lễ.
- `EXAMPLES.md` có "Key insight" đáng giữ: các bản over-engineered không sai về mặt kỹ thuật, vấn đề là thời điểm thêm độ phức tạp (trước khi cần).

**Hạn chế.**
- **Chỉ là lời dặn.** Theo mục 7, thiếu các tầng cưỡng chế (1 đến 3). Repo không có số liệu hiệu quả; phần "How to Know It's Working" chỉ nêu dấu hiệu định tính. Bài AGENTS.md (ETH Zurich) cho thấy file ngữ cảnh nhìn chung không cải thiện tỷ lệ thành công, nhưng chưa ai thử riêng file này, nên không kết luận được hướng nào. Việc nó ngắn là điểm có lợi.
- **Tự đánh giá trong cùng context.** "Would a senior engineer say this is overcomplicated?" phụ thuộc vào phán đoán của chính agent đang chịu áp lực context.
- **Không phủ P2, P6, P7.**
- **Cách kích hoạt.** SKILL.md không có `disable-model-invocation` nên agent có thể tự gọi, và mô tả khá rộng ("writing, reviewing, or refactoring code"). Nhưng skill có được nạp hay không là do agent quyết định, còn `CLAUDE.md` hay rule `alwaysApply` thì luôn được nạp. Với bộ nguyên tắc cần áp dụng ở mọi lượt, đường `CLAUDE.md` có vẻ đáng tin hơn đường plugin (suy luận từ cơ chế, chưa đo).
- **Thiếu ngoại lệ an toàn** cho "No error handling for impossible scenarios" (mục 7.4).

**Xung đột với các skill khác.**

| Karpathy | Skill khác | Xung đột | Hướng xử lý [Đề xuất] |
|---|---|---|---|
| "If uncertain, ask", "stop, name what's confusing, ask" | pstack `never-block-on-the-human`: làm rồi trình bày, chỉ hỏi với hành động không đảo ngược được | Cùng một tình huống (việc đảo ngược được mà mơ hồ), hai chỉ dẫn ngược nhau | Hỏi ở Phase 1 đến 4, nơi bạn đang ngồi và có G1 đến G4. Từ Phase 5, việc đã nằm trong ticket được duyệt: mơ hồ nhỏ thì ghi vào decision log (`show-me-your-work`) rồi tiếp tục, chỉ dừng hỏi với hành động không đảo ngược được |
| "Don't remove pre-existing dead code unless asked" | pstack `subtract-before-you-add`: xóa code chết trước khi thêm | Một bên cấm, một bên bắt buộc | Tách việc dọn thành ticket hoặc commit riêng đứng trước ticket tính năng. Khi đó cả hai cùng đúng: không lẫn dọn dẹp vào diff tính năng, vẫn "xóa trước khi thêm" |
| "No error handling for impossible scenarios" | pstack `boundary-discipline` | Karpathy không nêu ngoại lệ ranh giới | Thêm một dòng: giữ kiểm tra và xử lý lỗi tại ranh giới hệ thống |

Hợp nhau, không xung đột: "không abstraction cho code dùng một lần" tương ứng "một adapter là seam giả định" (Matt `codebase-design`); Simplicity First tương ứng "chỉ viết đủ code để pass" (Matt `tdd`); Surgical Changes tương ứng `scope.json`; Goal-Driven tương ứng `tdd` cộng `sequence-verifiable-units`. Về tính chất, bộ này gần nhóm `principle-*` của pstack (nguyên tắc ngắn, không có thao tác) hơn là Matt hay gstack (quy trình có artifact).

**Cách dùng trong mô hình [Đề xuất].**
1. Phase 0: lấy `CLAUDE.md` của bộ này làm nền cho file chỉ dẫn ngắn của repo (tầng 6), sau khi sửa dòng "hỏi khi chưa chắc" theo bảng trên và thêm ngoại lệ ranh giới.
2. Phase 4: dùng Surgical Changes làm khuôn cho mục "Không làm" của ticket và `scope.json`. Phần cưỡng chế vẫn phải bằng hook (tầng 1, 3).
3. Phase 4 đến 7: dùng mẫu `[Bước] → verify: [kiểm tra]` cho "kịch bản e2e" của ticket, với ô verify ghi hành động của người dùng thật, không chỉ tên test.
4. Không dùng thay cho cổng nào trong G1 đến G7.

**Kết luận.** Bổ sung rẻ và rõ ràng cho tầng 6 và cho cách viết ticket, xử lý tốt nhất P5 ở mức lời dặn. Hiệu quả thực tế chưa ai đo, và nó không thay được cơ chế cưỡng chế phạm vi, cổng duyệt hay e2e. Nên coi là lớp nền hành vi, không phải một phase.

---

## 10. Khoảng trống và việc cần làm tiếp

1. **Artifact user journey** (Phase 1) chưa có skill nào tạo. Cần viết thêm, hoặc thêm mục này vào template spec.
2. **Cổng G3 cứng** cho kiến trúc: cần cấu hình hoặc bọc `designing-architecture` với checkpoint luôn bật.
3. **"Kịch bản e2e" trong ticket** (Phase 4) để nối Phase 4 với Phase 7. Cần sửa template ticket.
4. **Cưỡng chế phạm vi** (Phase 5): chưa có skill nào làm hook theo `scope.json`. Cần viết, và vẫn còn lỗ hổng ghi file qua Bash (mục 7.3).
5. **Đo context** (P7): cần hook hoặc status line, vì hướng dẫn bằng chữ không đủ.
6. **Validate test thật sự**: các skill chỉ dựa vào phán đoán của agent. Chưa có mutation testing hay công cụ tương đương.
7. **Đánh giá skill có được tuân theo không:** `skill-creator` và eval trong `skills_gen/` có thể làm nền.
8. **Thử nghiệm các tầng kiểm soát code thừa** (mục 7.5): chưa có số liệu, cần thử trên ticket thật.
9. **Feature map:** cần quyết định có bắt buộc với mọi repo không, và ai chạy `maintain-verification-skill` (mục 6.3 nêu rõ chi phí duy trì).
10. **Ghép bộ:** ba nguồn dùng quy ước khác nhau (tracker, đường dẫn artifact, cách gọi skill). Cần một lớp cấu hình thống nhất trước khi dùng chung, ví dụ chọn một tracker và nơi lưu tài liệu ở Phase 0.

## 11. Lưu ý về độ tin cậy

- Nội dung các skill được đọc trực tiếp từ các thư mục trong `reference/`. Với một số skill, tôi chỉ đọc phần mô tả và các tiêu đề chính (đặc biệt các skill gstack dài như `plan-eng-review`, `reviewing-changes`, `qa`, `test-audit`), nên các nhận xét về chúng chỉ ở mức tổng quát.
- Với `andrej-karpathy-skills`, tôi đã đọc toàn bộ `SKILL.md`, `CLAUDE.md`, `README.md`, `EXAMPLES.md`, `CURSOR.md`, `plugin.json`, `marketplace.json`, và đối chiếu từng dòng nội dung rule Cursor với SKILL.md. Chưa đọc `README.zh.md` (bản dịch). Chưa đọc bài đăng gốc của Karpathy trên X; mọi trích dẫn về nó lấy từ README của repo. Các nhận xét so sánh với pstack dựa trên việc đọc `subtract-before-you-add`, `laziness-protocol`, `boundary-discipline`, `never-block-on-the-human`, `in-your-own-words`, và với Matt dựa trên `tdd`, `grilling`, `implementing-tickets`.
- Cột "Gọi bởi" lấy từ cờ `disable-model-invocation` trong frontmatter. Skill gstack không có cờ này nên ghi M, nhưng bộ này có cơ chế kích hoạt riêng (`triggers` trong frontmatter, tên lệnh), nên coi cột này chỉ là tham khảo với gstack.
- Ngưỡng cụ thể (~150k token smart zone, ~70–80% cảnh báo context) chỉ là điểm xuất phát. Con số 150k lấy từ `ask-matt`; con số còn lại là đề xuất, cần chỉnh theo thực tế dự án. Ngưỡng ~400 dòng diff ở bản trước đã bỏ vì không có căn cứ.
- Mục 6, 7 và 9.4 dựa trên nguồn web (bài viết, bài báo, tài liệu hooks) và nội dung `create-verification-skill`, `maintain-verification-skill` trong `reference/`. Các tầng 0, 1, 2, 3 và tác động của feature map đến code thừa là đề xuất và giả thuyết của tài liệu này, chưa được thử.

## 12. Chỗ còn nghi ngờ trong mô hình

Mô hình chưa chốt. Mục này để ghi các điểm cần xem lại; để trống phần "quyết định" cho đến khi có kết luận.

| Điểm | Câu hỏi | Quyết định |
|---|---|---|
| Hỏi hay đi tiếp khi mơ hồ | `karpathy-guidelines` bảo dừng và hỏi, pstack `never-block-on-the-human` bảo làm rồi trình bày. Ranh giới "hỏi ở Phase 1 đến 4, đi tiếp từ Phase 5" có hợp với việc thực tế không, hay có tình huống ở Phase 5 mà đi tiếp là sai? (mục 9.5) |  |
| Dọn code chết | Tách thành ticket riêng đứng trước ticket tính năng có làm Phase 4 cồng kềnh quá mức với những dọn dẹp nhỏ không? (mục 9.5) |  |
