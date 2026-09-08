/* Kernel makiety: modal / formularz / mail / plik / HITL. Nie bundel, nie produkt. */
window.OR_KERNEL = (function () {
  const $ = (s, c) => (c || document).querySelector(s);
  let kind = null;
  let payload = null;
  let fileInput = null;

  function toast(m) {
    if (typeof window.toast === "function") window.toast(m);
  }

  function open(html, nextKind) {
    kind = nextKind || "generic";
    const scrim = $("#viewScrim");
    const modal = $("#viewModal");
    if (!scrim || !modal) return;
    modal.innerHTML = html;
    scrim.classList.add("on");
    scrim.setAttribute("aria-hidden", "false");
    const first = modal.querySelector("input, select, textarea, button");
    if (first) first.focus();
  }

  function close() {
    kind = null;
    payload = null;
    const scrim = $("#viewScrim");
    const modal = $("#viewModal");
    if (scrim) {
      scrim.classList.remove("on");
      scrim.setAttribute("aria-hidden", "true");
    }
    if (modal) modal.innerHTML = "";
    if (typeof window.shipHeaderDraft !== "undefined") window.shipHeaderDraft = null;
  }

  function isOpen() {
    return Boolean($("#viewScrim")?.classList.contains("on"));
  }

  function fieldHtml(f) {
    const req = f.required ? " required" : "";
    const val = f.value == null ? "" : String(f.value);
    if (f.type === "select") {
      const opts = (f.options || []).map((o) => {
        const v = typeof o === "string" ? o : o.v;
        const t = typeof o === "string" ? o : o.t;
        return `<option value="${esc(v)}"${v === val ? " selected" : ""}>${esc(t)}</option>`;
      }).join("");
      return `<label class="kf"><span>${esc(f.label)}${f.required ? " *" : ""}</span><select name="${esc(f.id)}"${req}>${opts}</select></label>`;
    }
    if (f.type === "textarea") {
      return `<label class="kf"><span>${esc(f.label)}${f.required ? " *" : ""}</span><textarea name="${esc(f.id)}" rows="4"${req}>${esc(val)}</textarea></label>`;
    }
    return `<label class="kf"><span>${esc(f.label)}${f.required ? " *" : ""}</span><input name="${esc(f.id)}" type="${f.type || "text"}" value="${esc(val)}"${req} placeholder="${esc(f.placeholder || "")}"></label>`;
  }

  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function collect(form) {
    const data = {};
    form.querySelectorAll("[name]").forEach((el) => {
      data[el.name] = el.value.trim();
    });
    return data;
  }

  function form(opts) {
    payload = opts;
    const fields = (opts.fields || []).map(fieldHtml).join("");
    const hitl = opts.hitl
      ? `<p class="note">HITL: zapis dopiero po potwierdzeniu operatora. Makieta nie woła bazy.</p>`
      : "";
    open(`<div class="vm-head">
      <h2 id="vmTitle">${esc(opts.title)}</h2>
      <p class="note" style="margin:0">${opts.note || ""}</p>
    </div>
    <div class="vm-body"><form id="kForm" class="kform">${fields}${hitl}<p class="kerr" id="kErr" hidden></p></form></div>
    <div class="vm-foot">
      <button class="btn" type="button" data-act="k-cancel" style="margin-right:auto">Anuluj</button>
      <button class="btn btn-p" type="button" data-act="k-save">${esc(opts.saveLabel || (opts.hitl ? "Potwierdź i zapisz" : "Zapisz"))}</button>
    </div>`, "form");
  }

  function mail(opts) {
    payload = opts;
    open(`<div class="vm-head">
      <h2 id="vmTitle">${esc(opts.title || "Szkic maila")}</h2>
      <p class="note" style="margin:0">mail_draft · podgląd przed wysłaniem · klucz idempotentny</p>
    </div>
    <div class="vm-body"><form id="kForm" class="kform">
      <label class="kf"><span>Do</span><input name="to" value="${esc(opts.to || "")}"></label>
      <label class="kf"><span>Temat</span><input name="subject" value="${esc(opts.subject || "")}"></label>
      <label class="kf"><span>Treść</span><textarea name="body" rows="7">${esc(opts.body || "")}</textarea></label>
      <p class="note">Nie Graph / SMTP. Po „Wyślij” — mailto albo znacznik wysłano.</p>
    </form></div>
    <div class="vm-foot">
      <button class="btn" type="button" data-act="k-cancel" style="margin-right:auto">Anuluj</button>
      <button class="btn btn-p" type="button" data-act="k-send-mail">${esc(opts.sendLabel || "Wyślij")}</button>
    </div>`, "mail");
  }

  function confirm(opts) {
    payload = opts;
    open(`<div class="vm-head">
      <h2 id="vmTitle">${esc(opts.title || "Potwierdzenie")}</h2>
      <p class="note" style="margin:0">${opts.note || "HITL — człowiek zatwierdza zanim cokolwiek wejdzie do SoR."}</p>
    </div>
    <div class="vm-body"><p>${opts.text || ""}</p></div>
    <div class="vm-foot">
      <button class="btn" type="button" data-act="k-cancel" style="margin-right:auto">${esc(opts.cancelLabel || "Anuluj")}</button>
      <button class="btn btn-p" type="button" data-act="k-accept">${esc(opts.acceptLabel || "Akceptuj")}</button>
    </div>`, "confirm");
  }

  function detail(opts) {
    payload = opts;
    const rows = (opts.rows || []).map((r) => `<div class="krow"><dt>${esc(r.k)}</dt><dd>${r.html || esc(r.v)}</dd></div>`).join("");
    const acts = (opts.actions || []).map((a) => `<button class="btn" type="button" data-act="${esc(a.act)}" ${a.attrs || ""}>${esc(a.label)}</button>`).join("");
    open(`<div class="vm-head">
      <h2 id="vmTitle">${esc(opts.title)}</h2>
      <p class="note" style="margin:0">${opts.note || ""}</p>
    </div>
    <div class="vm-body"><dl class="kdetail">${rows}</dl></div>
    <div class="vm-foot">
      <button class="btn" type="button" data-act="k-cancel" style="margin-right:auto">Zamknij</button>
      ${acts}
    </div>`, "detail");
  }

  function blocked(reason) {
    open(`<div class="vm-head">
      <h2 id="vmTitle">Akcja zablokowana</h2>
      <p class="note" style="margin:0">Powód widoczny — nie cichy toast.</p>
    </div>
    <div class="vm-body"><p>${reason}</p></div>
    <div class="vm-foot"><button class="btn btn-p" type="button" data-act="k-cancel">Rozumiem</button></div>`, "blocked");
  }

  function pickFile(onPick) {
    if (!fileInput) {
      fileInput = document.createElement("input");
      fileInput.type = "file";
      fileInput.hidden = true;
      document.body.appendChild(fileInput);
    }
    fileInput.value = "";
    fileInput.onchange = () => {
      const f = fileInput.files && fileInput.files[0];
      if (!f) return;
      onPick({ name: f.name, size: f.size, kind: f.type || "wskazanie" });
    };
    fileInput.click();
  }

  function exportCsv(filename, headers, rows) {
    const line = (arr) => arr.map((c) => `"${String(c).replace(/"/g, '""')}"`).join(";");
    const body = [line(headers)].concat(rows.map((r) => line(r))).join("\n");
    const blob = new Blob(["\uFEFF" + body], { type: "text/csv;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
    toast("Eksport podglądu z seedu sesji. Nie produkcja.");
  }

  function saveForm() {
    const formEl = $("#kForm");
    if (!formEl || !payload) return;
    const data = collect(formEl);
    const missing = (payload.fields || []).filter((f) => f.required && !data[f.id]);
    const err = $("#kErr");
    if (missing.length) {
      if (err) {
        err.hidden = false;
        err.textContent = "Uzupełnij: " + missing.map((f) => f.label).join(", ") + ".";
      }
      return;
    }
    if (payload.requireSource && !data.source_ref) {
      if (err) {
        err.hidden = false;
        err.textContent = "Bez source_ref rekord nie wchodzi.";
      }
      return;
    }
    const done = payload.onSave;
    close();
    if (typeof done === "function") done(data);
  }

  function sendMail() {
    const formEl = $("#kForm");
    if (!formEl || !payload) return;
    const data = collect(formEl);
    if (!data.to || !data.subject) {
      const err = $("#kErr");
      if (err) {
        err.hidden = false;
        err.textContent = "Do i temat są wymagane.";
      }
      return;
    }
    const after = payload.onSend;
    const to = data.to;
    const subject = data.subject;
    const body = data.body;
    close();
    if (typeof after === "function") after(data);
    else {
      const href = `mailto:${encodeURIComponent(to)}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      window.location.href = href;
      toast("Wysłano (idempotentny klucz). Szkic oznaczony jako sent.");
    }
  }

  function accept() {
    const after = payload && payload.onAccept;
    close();
    if (typeof after === "function") after();
  }

  function dispatch(act, el) {
    if (act === "k-cancel" || act === "ship-docs-close") {
      close();
      return true;
    }
    if (act === "k-save") {
      saveForm();
      return true;
    }
    if (act === "k-send-mail") {
      sendMail();
      return true;
    }
    if (act === "k-accept") {
      accept();
      return true;
    }
    return false;
  }

  return {
    open,
    close,
    isOpen,
    form,
    mail,
    confirm,
    detail,
    blocked,
    pickFile,
    exportCsv,
    dispatch,
    esc,
    get kind() { return kind; }
  };
})();
