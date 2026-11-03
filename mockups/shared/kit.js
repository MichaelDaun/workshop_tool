/* ==========================================================================
   Verkstan kit – liten gemensam verktygslåda för mockuparna.
   - Språk (sv/en) via data-en="..." på element, eller K.t({sv, en}) i kod
   - Smeknamn, framsteg och tema sparas lokalt i webbläsaren
   - Toppfält, uppdragslista, toast och konfetti
   Ingen server, inga beroenden.
   ========================================================================== */
(function () {
  const store = {
    get(key, fallback) {
      try { const v = localStorage.getItem("verkstan." + key); return v == null ? fallback : JSON.parse(v); }
      catch (e) { return fallback; }
    },
    set(key, value) {
      try { localStorage.setItem("verkstan." + key, JSON.stringify(value)); } catch (e) { /* privat läge */ }
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

  function setLang(l) {
    lang = l; store.set("lang", l);
    applyLang();
    listeners.forEach(fn => fn(lang));
  }

  /* ---------- Tema ---------- */
  function applyTheme() {
    const th = store.get("theme", null);
    if (th) document.documentElement.setAttribute("data-theme", th);
  }
  function toggleTheme() {
    const cur = document.documentElement.getAttribute("data-theme")
      || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    const next = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    store.set("theme", next);
  }

  /* ---------- Smeknamn ---------- */
  const ADJ = ["Snabba", "Kloka", "Modiga", "Lugna", "Glada", "Nyfikna", "Listiga", "Starka", "Pigga", "Smarta"];
  const DJUR = ["Uttern", "Räven", "Ugglan", "Bävern", "Igelkotten", "Lodjuret", "Älgen", "Tranan", "Säln", "Haren"];
  function randomNick() {
    return ADJ[Math.floor(Math.random() * ADJ.length)] + " " + DJUR[Math.floor(Math.random() * DJUR.length)];
  }
  function nick() {
    let n = store.get("nick", null);
    if (!n) { n = randomNick(); store.set("nick", n); }
    return n;
  }
  function setNick(n) { store.set("nick", n.trim().slice(0, 24) || randomNick()); }
  function initials(n) { return n.split(/\s+/).map(w => w[0]).join("").slice(0, 2).toUpperCase(); }

  /* ---------- Framsteg ---------- */
  function progress(mod) { return store.get("progress", {})[mod] || []; }
  function markDone(mod, id) {
    const all = store.get("progress", {});
    const list = new Set(all[mod] || []);
    const isNew = !list.has(id);
    list.add(id); all[mod] = [...list]; store.set("progress", all);
    return isNew;
  }
  function resetProgress(mod) {
    const all = store.get("progress", {}); delete all[mod]; store.set("progress", all);
  }

  /* ---------- Toast + konfetti ---------- */
  let toastWrap;
  function toast(msg, badge = "✓") {
    if (!toastWrap) { toastWrap = document.createElement("div"); toastWrap.className = "toast-wrap"; toastWrap.setAttribute("aria-live", "polite"); document.body.append(toastWrap); }
    const el = document.createElement("div");
    el.className = "toast";
    el.innerHTML = `<span class="badge">${badge}</span><span></span>`;
    el.lastChild.textContent = msg;
    toastWrap.append(el);
    setTimeout(() => { el.classList.add("out"); setTimeout(() => el.remove(), 400); }, 2600);
  }

  function confetti(x, y) {
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const box = document.createElement("div"); box.className = "confetti";
    const cs = getComputedStyle(document.documentElement);
    const colors = ["--c-el", "--c-logik", "--c-signal", "--c-ai", "--c-nat", "--c-kod", "--c-matte"].map(v => cs.getPropertyValue(v).trim());
    x = x ?? innerWidth / 2; y = y ?? innerHeight / 3;
    for (let i = 0; i < 40; i++) {
      const p = document.createElement("i");
      const a = Math.random() * Math.PI * 2, d = 80 + Math.random() * 220;
      p.style.left = x + "px"; p.style.top = y + "px";
      p.style.background = colors[i % colors.length];
      p.style.setProperty("--dx", Math.cos(a) * d + "px");
      p.style.setProperty("--dy", Math.sin(a) * d + 160 + "px");
      p.style.setProperty("--rot", (Math.random() * 720 - 360) + "deg");
      p.style.animationDelay = Math.random() * 0.1 + "s";
      box.append(p);
    }
    document.body.append(box);
    setTimeout(() => box.remove(), 1700);
  }

  /* ---------- Toppfält ---------- */
  function topbar() {
    const bar = document.querySelector("header.topbar");
    if (!bar || !bar.hasAttribute("data-title-sv")) return;
    const back = bar.dataset.back || "../index.html";
    const titleSv = bar.dataset.titleSv || "", titleEn = bar.dataset.titleEn || titleSv;
    bar.innerHTML = `
      <a class="back" href="${back}" aria-label="Tillbaka till kartan" data-aria-en="Back to the map">
        <svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M12.5 4 6.5 10l6 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
      <div class="title"><span class="dot" aria-hidden="true"></span><h1 data-en="${titleEn}">${titleSv}</h1></div>
      <div class="tools">
        <button class="chip lang-chip" type="button" aria-label="Byt språk" data-aria-en="Change language"></button>
        <button class="chip theme-chip" type="button" aria-label="Byt mellan ljust och mörkt" data-aria-en="Toggle light and dark">
          <svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5a6.5 6.5 0 1 0 0 13z" fill="currentColor"/><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>
        </button>
        <span class="chip nick-chip" title=""><span class="avatar"></span><span class="nm"></span></span>
      </div>`;
    const langChip = bar.querySelector(".lang-chip");
    const paintLang = () => { langChip.textContent = lang === "sv" ? "EN" : "SV"; };
    langChip.addEventListener("click", () => { setLang(lang === "sv" ? "en" : "sv"); paintLang(); });
    paintLang();
    bar.querySelector(".theme-chip").addEventListener("click", toggleTheme);
    const n = nick();
    bar.querySelector(".nick-chip .avatar").textContent = initials(n);
    bar.querySelector(".nick-chip .nm").textContent = n;
    if (innerWidth < 520) bar.querySelector(".nick-chip .nm").hidden = true;
  }

  /* ---------- Uppdrag ---------- */
  function tasks(container, mod, list, opts = {}) {
    const ul = document.createElement("ol"); ul.className = "tasks";
    const meter = document.createElement("div"); meter.className = "meter"; meter.innerHTML = "<i></i>";
    container.append(ul, meter);
    const done = new Set(progress(mod));

    function render() {
      ul.innerHTML = "";
      let currentSet = false;
      list.forEach(task => {
        const li = document.createElement("li");
        const isDone = done.has(task.id);
        li.className = "task" + (isDone ? " done" : "");
        if (!isDone && !currentSet) { li.classList.add("current"); currentSet = true; }
        li.innerHTML = `<span class="tick" aria-hidden="true">✓</span><div><p></p>${task.hint ? '<p class="hint"></p>' : ""}</div>`;
        li.querySelector("p").textContent = t(task.text);
        if (task.hint) li.querySelector(".hint").textContent = t(task.hint);
        li.setAttribute("aria-label", t(task.text) + (isDone ? " – " + t("klart", "done") : ""));
        ul.append(li);
      });
      meter.firstChild.style.width = (done.size / list.length * 100) + "%";
    }
    render();
    onLang(render);

    return {
      complete(id) {
        if (done.has(id)) return false;
        done.add(id); markDone(mod, id); render();
        const task = list.find(x => x.id === id);
        toast(t(task.text), "✓");
        const li = [...ul.children][list.indexOf(task)];
        const r = li ? li.getBoundingClientRect() : null;
        confetti(r ? r.left + 20 : undefined, r ? r.top + 10 : undefined);
        if (done.size === list.length && opts.onAllDone) setTimeout(opts.onAllDone, 900);
        return true;
      },
      isDone: id => done.has(id),
      reset() { done.clear(); resetProgress(mod); render(); }
    };
  }

  function onLang(fn) { listeners.push(fn); }

  applyTheme();
  document.addEventListener("DOMContentLoaded", () => { topbar(); applyLang(); });

  window.K = { t, setLang, get lang() { return lang; }, onLang, applyLang, nick, setNick, randomNick, initials, progress, markDone, toast, confetti, tasks, store, toggleTheme };
})();
