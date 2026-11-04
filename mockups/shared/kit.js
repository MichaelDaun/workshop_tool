// Verkstan kit: language, nickname, progress, top bar, tasks, status line and the box panel.
(function () {
  const store = {
    get(key, fallback) {
      try { const v = localStorage.getItem("verkstan." + key); return v == null ? fallback : JSON.parse(v); }
      catch (e) { return fallback; }
    },
    set(key, value) {
      try { localStorage.setItem("verkstan." + key, JSON.stringify(value)); } catch (e) { /* private mode */ }
    }
  };

  const listeners = [];
  let lang = store.get("lang", "sv");

  function t(sv, en) {
    if (sv && typeof sv === "object") return sv[lang] ?? sv.sv;
    return lang === "en" ? en : sv;
  }

  function applyLang(root = document) {
    document.documentElement.lang = lang;
    root.querySelectorAll("[data-en]").forEach(el => {
      if (el.dataset.sv == null) el.dataset.sv = el.innerHTML;
      el.innerHTML = lang === "en" ? el.dataset.en : el.dataset.sv;
    });
    root.querySelectorAll("[data-ph-en]").forEach(el => {
      if (el.dataset.phSv == null) el.dataset.phSv = el.getAttribute("placeholder") || "";
      el.setAttribute("placeholder", lang === "en" ? el.dataset.phEn : el.dataset.phSv);
    });
    root.querySelectorAll("[data-aria-en]").forEach(el => {
      if (el.dataset.ariaSv == null) el.dataset.ariaSv = el.getAttribute("aria-label") || "";
      el.setAttribute("aria-label", lang === "en" ? el.dataset.ariaEn : el.dataset.ariaSv);
    });
  }
  function setLang(l) { lang = l; store.set("lang", l); applyLang(); listeners.forEach(fn => fn(lang)); }
  function onLang(fn) { listeners.push(fn); }

  function applyTheme() { const th = store.get("theme", null); if (th) document.documentElement.setAttribute("data-theme", th); }
  function toggleTheme() {
    const cur = document.documentElement.getAttribute("data-theme")
      || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    const next = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    store.set("theme", next);
  }

  const ADJ = ["Snabba", "Kloka", "Modiga", "Lugna", "Glada", "Nyfikna", "Listiga", "Starka", "Pigga", "Envisa"];
  const ANIMALS = ["Uttern", "Räven", "Ugglan", "Bävern", "Igelkotten", "Lodjuret", "Älgen", "Tranan", "Sälen", "Haren"];
  const pick = a => a[Math.floor(Math.random() * a.length)];
  const randomNick = () => pick(ADJ) + " " + pick(ANIMALS);
  function nick() { let n = store.get("nick", null); if (!n) { n = randomNick(); store.set("nick", n); } return n; }
  function setNick(n) { store.set("nick", n.trim().slice(0, 24) || randomNick()); }
  const initials = n => n.split(/\s+/).map(w => w[0]).join("").slice(0, 2).toUpperCase();

  function progress(mod) { return store.get("progress", {})[mod] || []; }
  function markDone(mod, id) {
    const all = store.get("progress", {});
    const list = new Set(all[mod] || []); list.add(id); all[mod] = [...list]; store.set("progress", all);
  }
  function resetProgress(mod) { const all = store.get("progress", {}); delete all[mod]; store.set("progress", all); }

  const CHECK = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5 10 17 19 7" fill="none" stroke="var(--active)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  function statusEl() {
    let el = document.querySelector(".status");
    if (!el) {
      const stage = document.querySelector(".stage"); if (!stage) return null;
      el = document.createElement("p"); el.className = "status"; el.setAttribute("aria-live", "polite"); el.setAttribute("role", "status");
      const scene = stage.querySelector(".scene");
      scene ? scene.after(el) : stage.prepend(el);
    }
    return el;
  }
  let last = { msg: "", kind: "info", at: -1e9 };
  function status(msg, kind = "info") {
    const el = statusEl(); if (!el) return;
    last = { msg, kind, at: performance.now() };
    el.className = "status" + (kind === "danger" ? " danger" : "");
    el.innerHTML = (kind === "done" ? CHECK : "") + '<span class="new"></span>';
    el.lastChild.textContent = msg;
  }

  function topbar() {
    const bar = document.querySelector("header.topbar");
    if (!bar || !bar.hasAttribute("data-title-sv")) return;
    const back = bar.dataset.back || "../index.html";
    const titleSv = bar.dataset.titleSv || "", titleEn = bar.dataset.titleEn || titleSv;
    bar.innerHTML = `
      <a class="back" href="${back}" aria-label="Tillbaka" data-aria-en="Back">
        <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M11 3.5 5.5 9l5.5 5.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
      <div class="title"><span class="dot" aria-hidden="true"></span><h1 data-en="${titleEn}">${titleSv}</h1></div>
      <div class="tools">
        <button class="chip lang-chip" type="button" aria-label="Byt språk" data-aria-en="Change language"></button>
        <button class="chip theme-chip" type="button" aria-label="Ljust eller mörkt" data-aria-en="Light or dark">
          <svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5a6.5 6.5 0 1 0 0 13z" fill="currentColor"/><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>
        </button>
        <span class="nick"></span>
      </div>`;
    const langChip = bar.querySelector(".lang-chip");
    const paint = () => { langChip.textContent = lang === "sv" ? "EN" : "SV"; };
    langChip.addEventListener("click", () => { setLang(lang === "sv" ? "en" : "sv"); paint(); });
    paint();
    bar.querySelector(".theme-chip").addEventListener("click", toggleTheme);
    const nk = bar.querySelector(".nick"); nk.textContent = nick();
    if (innerWidth < 560) nk.hidden = true;
  }

  const TICK = '<svg class="tick" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5 10 17 19 7"/></svg>';
  function tasks(container, mod, list, opts = {}) {
    const ol = document.createElement("ol"); ol.className = "tasks";
    container.append(ol);
    const done = new Set(progress(mod).filter(id => list.some(x => x.id === id)));
    let justDone = null;

    function render() {
      ol.innerHTML = "";
      let currentSet = false;
      list.forEach((task, i) => {
        const li = document.createElement("li");
        const isDone = done.has(task.id);
        li.className = "task" + (isDone ? " done" : "") + (task.id === justDone ? " drawing" : "");
        if (!isDone && !currentSet) { li.classList.add("current"); currentSet = true; }
        li.innerHTML = `<span class="nr">${i + 1}</span><p></p>${isDone ? TICK : "<span></span>"}`;
        li.querySelector("p").textContent = t(task.text);
        if (isDone) li.setAttribute("aria-label", t(task.text) + ". " + t("Klart.", "Done."));
        ol.append(li);
      });
      justDone = null;
    }
    render();
    onLang(render);

    return {
      complete(id) {
        if (done.has(id)) return false;
        done.add(id); markDone(mod, id); justDone = id; render();
        // keep a status the page wrote a moment ago and add the step note after it
        const i = list.findIndex(x => x.id === id);
        const step = t(`Uppgift ${i + 1} av ${list.length} klar.`, `Task ${i + 1} of ${list.length} done.`);
        const recent = performance.now() - last.at < 60 && last.msg && !/^(Uppgift|Task) \d/.test(last.msg);
        status(recent ? last.msg.replace(/([^.?])$/, "$1.") + " " + step : step, recent && last.kind === "danger" ? "danger" : "done");
        if (opts.onComplete) opts.onComplete(id);
        return true;
      },
      isDone: id => done.has(id),
      reset() { done.clear(); resetProgress(mod); render(); }
    };
  }

  // the physical box: id, connection state and a drawing
  function box(container, o) {
    container.classList.add("box");
    container.innerHTML = `<h3><i aria-hidden="true"></i><span>${o.node}</span></h3><div class="plan">${o.svg}</div><button class="btn ghost" type="button"></button>`;
    const btn = container.querySelector(".btn");
    let on = false;
    function paint() {
      container.classList.toggle("connected", on);
      container.querySelector("h3").setAttribute("aria-label", `${o.node}, ${on ? t("ansluten", "connected") : t("inte ansluten", "not connected")}`);
      btn.textContent = on ? t("Koppla från", "Disconnect") : t("Anslut", "Connect");
    }
    btn.addEventListener("click", () => { on = !on; paint(); if (o.onConnect) o.onConnect(on); });
    onLang(paint); paint();
    return { root: container, svg: container.querySelector("svg"), connected: () => on };
  }

  applyTheme();
  document.addEventListener("DOMContentLoaded", () => { topbar(); applyLang(); });

  window.K = {
    t, setLang, get lang() { return lang; }, onLang, applyLang,
    nick, setNick, randomNick, initials, progress, markDone, store, toggleTheme,
    status, tasks, box
  };
})();
