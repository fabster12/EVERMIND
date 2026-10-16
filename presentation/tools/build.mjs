#!/usr/bin/env node
/**
 * scenes.json + measured narration -> index.html (+ parts/partN.html)
 *
 * Each part is a standalone composition so it can be rendered alone:
 *   npx hyperframes render --composition parts/part3.html
 */
import { execFileSync } from "child_process";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const FPS = 30;

const LEAD = 0.4;   // silence before narration starts
const TAIL = 0.9;   // breathing room after it ends
const FLOOR = { title: 6, statement: 5, steps: 7, numbers: 7, shots: 8,
                bars: 7, list: 7, boxes: 6, years: 7, gallery: 8, outro: 5,
                diagram: 9 };

const PART_TITLES = {
  1: "The Cost of Forgetting", 2: "Introducing EverMind",
  3: "How It’s Actually Built", 4: "Why a Human Still Approves",
  5: "The Ask",
};

function dur(file) {
  try {
    return parseFloat(execFileSync("ffprobe", [
      "-v", "quiet", "-show_entries", "format=duration",
      "-of", "csv=p=0", file,
    ], { encoding: "utf-8" }).trim()) || 0;
  } catch { return 0; }
}

const scenes = JSON.parse(fs.readFileSync(path.join(ROOT, "scenes.json"), "utf-8"));

// ---- timing -------------------------------------------------------------
let total = 0;
scenes.forEach((s, i) => {
  const wav = path.join(ROOT, "audio", `scene-${String(i + 1).padStart(2, "0")}.wav`);
  const spoken = fs.existsSync(wav) ? dur(wav) : 0;
  const d = Math.max(FLOOR[s.kind] ?? 6, spoken + LEAD + TAIL);
  s.idx = i + 1;
  s.spoken = spoken;
  s.duration = Math.round(d * FPS) / FPS;
  s.audio = `../audio/scene-${String(i + 1).padStart(2, "0")}.wav`;
  total += s.duration;
});

// group into parts, with each part's local timeline starting at 0
const parts = new Map();
for (const s of scenes) {
  if (!parts.has(s.part)) parts.set(s.part, []);
  parts.get(s.part).push(s);
}
for (const list of parts.values()) {
  let t = 0;
  for (const s of list) { s.localStart = Math.round(t * FPS) / FPS; t += s.duration; }
}

const esc = (v) => String(v ?? "")
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
  .replace(/"/g, "&quot;");

// Caption chunking. Mirrors tools/make_subs.py so the burned-in bar and the
// .srt sidecar carry identical text and timing.
const CAP_MAX = 84;
function capChunks(text) {
  const out = [];
  for (const raw of (text.match(/[^.!?]+[.!?]?/g) || [])) {
    const s = raw.trim();
    if (!s) continue;
    if (s.length <= CAP_MAX) { out.push(s); continue; }
    let buf = "";
    for (const piece of s.split(/(?<=,)\s+/)) {
      if ((buf + " " + piece).trim().length <= CAP_MAX) {
        buf = (buf + " " + piece).trim();
      } else {
        if (buf) out.push(buf);
        buf = piece;
      }
    }
    if (buf) out.push(buf);
  }
  // hard-split anything still over length
  const final = [];
  for (let p of out) {
    while (p.length > CAP_MAX) {
      let cut = p.lastIndexOf(" ", CAP_MAX);
      if (cut <= 0) cut = CAP_MAX;
      final.push(p.slice(0, cut).trim());
      p = p.slice(cut).trim();
    }
    if (p) final.push(p);
  }
  return final;
}

function capWrap(line) {
  if (line.length <= 44) return line;
  const cut = line.lastIndexOf(" ", 46);
  return cut <= 0 ? line : line.slice(0, cut) + "\n" + line.slice(cut + 1);
}

function captionsFor(list) {
  const cues = [];
  for (const s of list) {
    const parts = capChunks(s.narration || "");
    const total = parts.reduce((a, p) => a + p.length, 0) || 1;
    let at = s.localStart + LEAD;
    const speechEnd = at + s.spoken;
    for (const p of parts) {
      const share = s.spoken * (p.length / total);
      const end = Math.min(at + Math.max(1.2, share), speechEnd + 0.35);
      cues.push({ a: at, b: end, t: capWrap(p) });
      at = end;
    }
  }
  return cues;
}

// ---- per-kind markup ----------------------------------------------------
function body(s) {
  const head = `
    <div class="head">
      <div class="eyebrow">Part ${s.part} &middot; ${esc(PART_TITLES[s.part])}</div>
      <h2>${esc(s.heading)}</h2>
      ${s.sub ? `<p class="sub">${esc(s.sub)}</p>` : ""}
    </div>`;

  const shotImgs = (s.shots || []).map((n, i) =>
    `<figure class="shot r" data-r="${i}"><img src="../assets/shots/${esc(n)}.png" alt=""></figure>`).join("");
  const docImgs = (s.docs || []).map((n, i) =>
    `<figure class="doc r" data-r="${i}"><img src="../assets/docs/${esc(n)}.png" alt=""></figure>`).join("");

  switch (s.kind) {
    case "title":
      return `<div class="hero">
        <h1 class="r" data-r="0">${esc(s.heading)}</h1>
        <p class="r" data-r="1">${esc(s.sub)}</p>
        <div class="rule r" data-r="2"></div>
      </div>`;

    case "statement":
      return `${head}<div class="statement">${
        (s.lines || []).map((l, i) => `<div class="line r" data-r="${i}">${esc(l)}</div>`).join("")
      }</div>`;

    case "numbers":
      return `${head}<div class="grid2">${
        (s.numbers || []).map((n, i) =>
          `<div class="num r" data-r="${i}"><b>${esc(n.value)}</b><span>${esc(n.label)}</span></div>`).join("")
      }</div>`;

    case "bars":
      return `${head}<div class="bars">${
        (s.bars || []).map((b, i) => `
          <div class="barrow r" data-r="${i}">
            <div class="barlab"><b>${esc(b.value)}</b><span>${esc(b.label)}</span></div>
            <div class="bartrack"><div class="barfill ${esc(b.tone)}" style="--w:${b.pct}%"></div></div>
            <div class="barsub">${esc(b.sub)}</div>
          </div>`).join("")
      }</div>${shotImgs ? `<div class="aside">${shotImgs}</div>` : ""}`;

    case "list":
      return `${head}<ul class="checks">${
        (s.items || []).map((it, i) => `<li class="r" data-r="${i}">${esc(it)}</li>`).join("")
      }</ul>${docImgs ? `<div class="aside">${docImgs}</div>` : ""}`;

    case "steps":
      return `${head}<div class="steps${(s.items || []).length % 3 === 0 ? " six" : ""}">${
        (s.items || []).map((it, i) =>
          `<div class="step r" data-r="${i}"><i>${i + 1}</i><span>${esc(it)}</span></div>`).join("")
      }</div>`;

    case "boxes":
      return `${head}<div class="boxes">${
        (s.boxes || []).map((b, i) =>
          `<div class="box r" data-r="${i}"><b>${esc(b.title)}</b><span>${esc(b.sub)}</span></div>`).join("")
      }</div>${(shotImgs + docImgs) ? `<div class="aside">${shotImgs}${docImgs}</div>` : ""}`;

    case "years":
      return `${head}<div class="years">${
        (s.years || []).map((y, i) =>
          `<div class="yr r" data-r="${i}"><div class="ybar${y.hot ? " hot" : ""}" style="--h:${y.pct}%"></div><span>${esc(y.y)}</span></div>`).join("")
      }</div>${docImgs ? `<div class="aside">${docImgs}</div>` : ""}`;

    case "diagram": {
      // A horizontal flow of labelled boxes, each one lighting up in turn
      // (see flowBoxTimeline below) while a connecting line traces ahead
      // of the active box. One box - the human step - gets a visually
      // distinct "gate" treatment: an outline only, no fill, so the human
      // decision reads as categorically different from the automated steps
      // either side of it.
      const boxes = (s.flow || []).map((b, i) => `
        <div class="flowbox${b.gate ? " gate" : ""} r" data-r="${i}" data-flow-i="${i}">
          <b>${esc(b.label)}</b><span>${esc(b.sub)}</span>
        </div>
        ${i < (s.flow || []).length - 1 ? `<div class="flowline" data-flow-line="${i}"></div>` : ""}
      `).join("");
      return `${head}<div class="flow">${boxes}</div>`;
    }

    case "shots": {
      // Documents listed alongside shots are equal subjects, so a scene can
      // hand off between an app capture and a workbook sheet. "order" gives
      // the on-screen sequence explicitly; the captures are shown one at a
      // time in this order, and the voice describes them in the same order,
      // so getting it wrong puts every caption a shot behind. Without it,
      // shots come first and then docs.
      const seq = s.order || [
        ...(s.shots || []).map(n => ({ n, doc: false })),
        ...(s.docs || []).map(n => ({ n, doc: true })),
      ].map(x => x.n);
      const isDoc = new Set(s.docs || []);
      const panels = seq.map((n, i) => {
        const dir = isDoc.has(n) ? "docs" : "shots";
        // excel_* are screenshots of the live Excel window, a different shape
        // from the portrait PDF pages, so they get their own fit.
        const cls = isDoc.has(n)
          ? ` doc${n.startsWith("excel_") ? " sheet" : ""}` : "";
        return `<figure class="shot${cls} r" data-r="${i}">` +
          `<img src="../assets/${dir}/${esc(n)}.png" alt=""></figure>`;
      }).join("");
      return `${head}<div class="shots">${panels}</div>`;
    }

    case "gallery": {
      // Same full-bleed one-at-a-time cycle as the screenshot scenes: a
      // fanned-out row of thumbnails is unreadable no matter how far it is
      // zoomed, because each one only ever occupies a quarter of the width.
      // most business documents are portrait pages; the rebuilt payslip is
      // landscape, and must not be fitted by height like the others
      const LANDSCAPE = new Set(["sample_payslip_rebuilt"]);
      const panels = (s.docs || []).map((n, i) =>
        `<figure class="shot doc${LANDSCAPE.has(n) ? "" : " portrait"} r" data-r="${i}">` +
        `<img src="../assets/docs/${esc(n)}.png" alt=""></figure>`
      ).join("");
      return `${head}<div class="shots">${panels}</div>`;
    }

    case "outro":
      return `<div class="hero">
        <h1 class="r" data-r="0">${esc(s.heading)}</h1>
        <p class="r" data-r="1">${esc(s.sub)}</p>
        ${s.credit ? `<p class="credit r" data-r="2">${esc(s.credit)}</p>` : ""}
      </div>`;

    default:
      return head;
  }
}

function sceneMarkup(s) {
  const wide = ["shots", "gallery"].includes(s.kind);
  const big = ["title", "outro"].includes(s.kind);
  // the pointing pose faces right, so it belongs on the left of the content
  const mleft = s.mascotPose === "pointing";
  // captures and documents both need the whole frame to stay legible
  const bleed = s.kind === "shots" || s.kind === "gallery";
  return `
  <section class="scene${wide ? " wide" : ""}${big ? " big" : ""}${mleft ? " mleft" : ""}${bleed ? " bleed" : ""}" id="${esc(s.id)}">
    <div class="stage">
      <div class="content">${body(s)}</div>
      <div class="mascot">
        <img src="../assets/mind-${esc(s.mascotPose)}.png" alt="">
      </div>
    </div>
  </section>`;
}

const CSS = `
:root{--p:#1E1E54;--o:#D39F32;--ink:#1b1b3a;--mut:#6b6b84;--bg:#f4f4f7;--card:#fff;}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden}
body{background:var(--bg);color:var(--ink)}
html,body,#root,#root *{font-family:Inter,system-ui,sans-serif}
#root{position:relative;width:1920px;height:1080px;overflow:hidden;
  background:
    radial-gradient(1100px 680px at 82% -12%,rgba(255,98,0,.10),transparent 60%),
    radial-gradient(900px 620px at -8% 108%,rgba(46,11,84,.12),transparent 60%),
    var(--bg);}
.scene{position:absolute;inset:0;opacity:0}
.stage{position:absolute;inset:0;display:grid;grid-template-columns:1fr 620px;
  gap:56px;padding:66px 76px 70px;align-items:center}
.scene.wide .stage{grid-template-columns:1fr 400px;gap:42px}
/* The sheet's pointing pose aims right. On scenes that use it, the mascot
   moves to the left column so the arm points INTO the content rather than
   off the edge of the frame. */
.scene.mleft .stage{grid-template-columns:620px 1fr}
.scene.mleft.wide .stage{grid-template-columns:400px 1fr}
.scene.mleft .mascot{order:-1}
.scene.mleft .content{order:1}
.content{min-width:0;display:flex;flex-direction:column;justify-content:center;
  height:100%}
.mascot{display:flex;align-items:center;justify-content:center;height:100%}
.mascot img{width:100%;max-height:880px;object-fit:contain;
  filter:drop-shadow(0 30px 42px rgba(46,11,84,.24))}
.scene.wide .mascot img{max-height:660px}
/* title and outro: mascot gets equal billing with the wordmark */
.scene.big .stage{grid-template-columns:1fr 760px}
.scene.big .mascot img{max-height:940px}

.head{margin-bottom:34px}
.eyebrow{font-size:19px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
  color:#A67A24;margin-bottom:12px}
  /* Darker than --o (#D39F32): the bright brand gold fails 3:1 text contrast
     on the light scene background. This stays visibly "gold" while passing. */
h1{font-size:112px;font-weight:800;letter-spacing:-.03em;line-height:.98;color:var(--p)}
h2{font-size:62px;font-weight:800;letter-spacing:-.02em;line-height:1.04;color:var(--p)}
.sub{font-size:27px;color:var(--mut);margin-top:14px;max-width:1000px;line-height:1.35}
.hero{display:flex;flex-direction:column;justify-content:center;height:100%}
.hero p{font-size:34px;color:var(--mut);margin-top:20px}
.hero .credit{font-size:21px;color:#9a93a8;margin-top:40px;font-weight:600;
  letter-spacing:.02em}
.rule{width:190px;height:9px;border-radius:5px;background:var(--o);margin-top:34px}

.statement{display:flex;flex-direction:column;gap:20px}
.line{font-size:60px;font-weight:800;color:var(--p);letter-spacing:-.02em}
.line::before{content:"";display:inline-block;width:20px;height:20px;border-radius:50%;
  background:var(--o);margin-right:22px;vertical-align:middle}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.num{background:var(--card);border-radius:18px;padding:34px 38px;
  box-shadow:0 10px 26px rgba(46,11,84,.09);border-left:9px solid var(--o)}
.num b{display:block;font-size:76px;font-weight:800;color:var(--p);line-height:1;
  letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.num span{display:block;font-size:22px;color:var(--mut);margin-top:10px;font-weight:600}

.bars{display:flex;flex-direction:column;gap:26px}
.barrow{display:grid;grid-template-columns:220px 1fr 230px;align-items:center;gap:22px}
.barlab b{font-size:50px;font-weight:800;color:var(--p);font-variant-numeric:tabular-nums}
.barlab span{display:block;font-size:17px;font-weight:700;letter-spacing:.11em;color:var(--mut)}
.bartrack{height:34px;background:#e3dfea;border-radius:17px;overflow:hidden}
.barfill{height:100%;width:var(--w);border-radius:17px;transform-origin:left center}
.barfill.go{background:var(--o)}
.barfill.warn{background:#f0a23c}
.barfill.off{background:#bdb7c7}
.barsub{font-size:19px;color:var(--mut)}

.cols{display:grid;grid-template-columns:1.25fr .75fr;gap:34px;align-items:center}
.checks{list-style:none;display:flex;flex-direction:column;gap:11px;min-width:0}
.checks li{position:relative;padding:14px 18px 14px 56px;background:var(--card);
  border-radius:11px;font-size:22px;line-height:1.25;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis;box-shadow:0 5px 16px rgba(46,11,84,.07)}
.checks li::before{content:"";position:absolute;left:20px;top:50%;width:19px;height:10px;
  margin-top:-7px;border-left:4px solid var(--o);border-bottom:4px solid var(--o);
  transform:rotate(-45deg)}

.steps{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.steps.six{grid-template-columns:repeat(3,1fr)}
.step{background:var(--p);color:#fff;border-radius:16px;padding:28px 26px;
  display:flex;align-items:center;gap:18px;box-shadow:0 10px 24px rgba(46,11,84,.22)}
.step i{flex:none;width:46px;height:46px;border-radius:50%;background:var(--o);
  display:grid;place-items:center;font-style:normal;font-weight:800;font-size:23px}
.step span{font-size:23px;font-weight:600;line-height:1.2}

.boxes{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px}
.box{background:var(--card);border-radius:18px;padding:36px 32px;text-align:center;
  border-top:8px solid var(--o);box-shadow:0 10px 26px rgba(46,11,84,.09)}
.box b{display:block;font-size:44px;font-weight:800;color:var(--p);letter-spacing:-.02em}
.box span{display:block;font-size:21px;color:var(--mut);margin-top:10px}

.years{display:flex;align-items:flex-end;gap:16px;height:310px}
.yr{flex:1;display:flex;flex-direction:column;justify-content:flex-end;
  align-items:center;height:100%;gap:12px}
.ybar{width:100%;height:var(--h);min-height:10px;border-radius:10px 10px 0 0;
  background:#cfc8da;transform-origin:bottom center}
.ybar.hot{background:var(--o)}
.yr span{font-size:19px;color:var(--mut);font-weight:600}

.flow{display:flex;align-items:stretch;gap:0;flex-wrap:wrap;row-gap:28px}
.flowbox{flex:1 1 150px;background:var(--card);border-radius:16px;padding:22px 18px;
  text-align:center;box-shadow:0 8px 20px rgba(30,30,84,.08);border:3px solid transparent;
  transition:none;display:flex;flex-direction:column;justify-content:center;min-height:120px}
.flowbox b{font-size:21px;font-weight:800;color:var(--p);line-height:1.15}
.flowbox span{font-size:14px;color:var(--mut);margin-top:8px;line-height:1.25}
.flowbox.active{border-color:var(--o);background:#fdf6ea;box-shadow:0 10px 26px rgba(211,159,50,.35)}
.flowbox.gate{background:transparent;border:3px solid var(--o);box-shadow:none}
.flowbox.gate b{color:var(--o)}
.flowline{flex:0 0 36px;align-self:center;height:4px;background:#d8d4e0;position:relative;
  overflow:hidden}
.flowline::after{content:"";position:absolute;inset:0;background:var(--o);
  transform:scaleX(0);transform-origin:left center}
.flowline.drawn::after{transform:scaleX(1)}

/* Screenshot scenes run FULL BLEED.
   A capture shown in a side panel is downsampled ~3.5x from its 3300px
   source, which destroys the UI text that is the whole reason for showing
   it. Full bleed is ~1.7x, and the text survives. The mascot and heading
   float over the image instead of sharing a grid with it. */
.scene.bleed .stage{display:block;padding:0}
.scene.bleed .content{position:absolute;inset:0;display:block;height:100%}
/* sit the title over the app's own sidebar column, which carries no detail
   worth reading, rather than over the data panes on the right */
.scene.bleed .head{position:absolute;left:0;right:0;top:0;z-index:6;
  margin:0;padding:26px 76px 22px;
  background:linear-gradient(180deg,rgba(244,242,247,.97) 0%,
    rgba(244,242,247,.93) 62%,rgba(244,242,247,0) 100%)}
.scene.bleed .head h2{font-size:52px}
.scene.bleed .head .sub{font-size:23px;margin-top:8px}
.scene.bleed .mascot{position:absolute;right:40px;bottom:26px;width:330px;
  height:auto;z-index:7}
.scene.bleed .mascot img{max-height:420px}
.scene.bleed.mleft .mascot{right:auto;left:40px}

.shots{display:flex;gap:26px;align-items:center;justify-content:center;
  min-height:620px;padding:0 40px}
/* Full-bleed variant. Each capture is laid out at exactly frame size and
   then SCALED DOWN for the "small" state, so the zoomed-in hold sits at
   scale(1) — no resampling at all, which is what keeps the UI text sharp. */
.scene.bleed .shots{display:block;min-height:0;padding:0;position:absolute;
  inset:0}
/* Hidden by default in CSS, not via gsap.set at build time: a tween added
   later can re-assert its own start state at position 0 and reveal every
   capture at once. The timeline fades each one in when its turn comes. */
.scene.bleed .shot{position:absolute;inset:0;border:0;background:transparent;
  overflow:hidden;transform-origin:center center;will-change:transform;
  opacity:0}
/* FILL the frame, do not fit it. Every capture is about 1.45:1 against a
   1.78:1 frame, so fitting by height wastes ~350px of width and shrinks the
   text we are trying to make readable. Filling by width crops a little off
   the bottom, which is chrome and legend rather than content. */
.scene.bleed .shot img{position:absolute;top:0;left:50%;
  width:1920px;height:auto;transform:translateX(-50%);object-fit:unset;
  max-width:none;max-height:none}
/* Rendered sheets are short and wide. Scale them past the frame width and
   centre them, so the rows are as large as possible; the slight overhang is
   margin, not content. */
/* A rendered sheet must stay whole - its title row and column headers are
   the point - so it fits inside the frame rather than overflowing it. */
.scene.bleed .shot.doc img{width:auto;height:1040px;top:50%;
  transform:translate(-50%,-50%)}
/* A live Excel window is 1.68:1 against a 1.78:1 frame, so fitting by the
   full frame height leaves only a thin margin either side while keeping the
   ribbon, the sheet tabs and the formula bar intact. Filling by width instead
   would crop exactly those, and they are what makes it read as Excel rather
   than as another table on a slide. */
.scene.bleed .shot.doc.sheet img{width:auto;height:1080px;top:50%;
  transform:translate(-50%,-50%)}
/* A payslip or certificate is PORTRAIT. Filling by width would throw away
   most of the page, so these fit by height instead and run as tall as the
   frame allows. */
.scene.bleed .shot.doc.portrait img{width:auto;height:1060px;top:50%;
  transform:translate(-50%,-50%)}
/* card treatment only while pulled back; removed at full size */
.scene.bleed .shot.small{border-radius:14px;
  box-shadow:0 26px 60px rgba(46,11,84,.26)}
.shot{flex:1;min-width:0;background:#fff;border-radius:14px;overflow:hidden;
  box-shadow:0 18px 42px rgba(46,11,84,.17);border:1px solid #e0dbe8;
  transform-origin:center center;will-change:transform}
/* Panel-mode rules only. These crop to a fixed height on purpose, so they
   must never reach a full-bleed capture - a fixed height there fights the
   width rule and squashes the image out of proportion. */
.scene:not(.bleed) .shot img{display:block;width:100%;height:440px;
  object-fit:cover;object-position:top left;will-change:object-position}
.scene:not(.bleed) .shots:has(.shot:nth-child(3)) .shot img{height:510px}
.scene:not(.bleed) .shots .shot:only-child{flex:0 1 74%}
.scene:not(.bleed) .shots .shot:only-child img{height:470px}

/* the row sits high so a card scaled 2.15x from its top edge still fits */
.gallery{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;
  align-items:start;margin-top:4px}
.scene.wide:has(.gallery) .content{justify-content:flex-start;padding-top:40px}
.doc{background:#fff;border-radius:10px;overflow:hidden;
  box-shadow:0 14px 32px rgba(46,11,84,.16);border:1px solid #e0dbe8;
  transform-origin:center center;will-change:transform}
.doc img{display:block;width:100%;height:330px;object-fit:cover;
  object-position:top center;will-change:object-position}

/* caption bar - burned in, so it survives players that ignore soft subs */
#caps{position:absolute;left:50%;transform:translateX(-50%);bottom:46px;
  width:1400px;height:0;pointer-events:none;z-index:50}
#caps .cue{position:absolute;bottom:0;left:50%;transform:translateX(-50%);
  opacity:0;width:max-content;max-width:1320px;padding:15px 30px;border-radius:12px;
  background:rgba(22,8,42,.86);color:#fff;font-size:30px;line-height:1.34;
  font-weight:600;text-align:center;white-space:pre-line;
  box-shadow:0 8px 28px rgba(0,0,0,.26)}

.aside{display:flex;gap:20px;margin-top:28px;align-items:flex-start}
.aside .shot{flex:1;min-width:0}
.aside .shot img{max-height:270px;object-fit:cover;object-position:top left}
.aside .doc{flex:0 0 auto;width:300px}
.aside .doc img{max-height:300px;object-fit:cover;object-position:top center}
/* a single screenshot should not sprawl: cap it and keep it left-aligned
   (panel mode only - a cap here would distort a full-bleed capture) */
.scene:not(.bleed) .shots:has(.shot:only-child) .shot{flex:0 1 82%}
.scene:not(.bleed) .shots .shot:only-child img{max-height:540px}
.docside{display:flex;gap:16px}
.docside .doc img{max-height:330px}
`;

// The capture starts before a CDN stylesheet can resolve, so the first frames
// render in a fallback face. Inlining the family removes that race.
function fontFaces() {
  const dir = path.join(ROOT, "assets", "fonts");
  if (!fs.existsSync(dir)) return "";
  return fs.readdirSync(dir).filter(f => f.endsWith(".woff2")).map(f => {
    const m = /Inter-(\d+)/.exec(f);
    const b64 = fs.readFileSync(path.join(dir, f)).toString("base64");
    return `@font-face{font-family:Inter;font-style:normal;font-weight:${m ? m[1] : 400};` +
           `font-display:block;src:url(data:font/woff2;base64,${b64}) format("woff2")}`;
  }).join("\n");
}

const FONTS = fontFaces();

const RUNTIME = (list, totalDur, compId) => `
const SCENES = ${JSON.stringify(list.map((s, i) => ({
    id: s.id, start: s.localStart, dur: s.duration, kind: s.kind, idx: s.idx, i,
  })))};
const tl = gsap.timeline({paused:true});
const Q = (sel, root) => Array.from((root||document).querySelectorAll(sel));

SCENES.forEach(s => {
  const el = document.getElementById(s.id);
  const t = s.start;
  const out = t + s.dur;

  // Cross-dissolve: the incoming scene starts rising before the outgoing one
  // has finished falling, otherwise the stage is empty for a frame at every
  // boundary. Linear ramps so the two sum to roughly constant coverage.
  const XF = 0.5;
  tl.fromTo(el, {opacity:0}, {opacity:1, duration:XF, ease:"none"},
    Math.max(0, t - XF * 0.5));
  tl.to(el, {opacity:0, duration:XF, ease:"none"}, out - XF * 0.5);

  // heading + mascot entrance
  const head = el.querySelector('.head, .hero');
  if (head) tl.fromTo(head, {y:26, opacity:0},
    {y:0, opacity:1, duration:0.55, ease:"power3.out"}, t + 0.12);

  const mas = el.querySelector('.mascot img');
  if (mas) {
    // entrance: slide in from the outer edge of whichever column it occupies
    const onLeft = el.classList.contains('mleft');
    const fromX = onLeft ? -52 : (s.i % 2 ? 54 : -38);
    tl.fromTo(mas, {x:fromX, y:40, opacity:0, scale:0.92, rotation:s.i % 2 ? 4 : -4},
      {x:0, y:0, opacity:1, scale:1, rotation:0, duration:0.7,
       ease:"back.out(1.5)"}, t + 0.05);

    // a beat of emphasis as the content lands - the character "presents" it
    tl.to(mas, {scale:1.045, duration:0.26, ease:"power2.out"}, t + 0.78);
    tl.to(mas, {scale:1, duration:0.5, ease:"elastic.out(1,0.55)"}, t + 1.04);

    // layered idle: bob and sway on different periods so it never looks looped
    const span = Math.max(1.5, s.dur - 1.9);
    const bob = 2.3, sway = 3.7;
    tl.to(mas, {y:-14, duration:bob/2, yoyo:true,
      repeat:Math.max(0, Math.ceil(span/bob)*2 - 1), ease:"sine.inOut"}, t + 1.3);
    tl.to(mas, {rotation:2.2, duration:sway/2, yoyo:true,
      repeat:Math.max(0, Math.ceil(span/sway)*2 - 1), ease:"sine.inOut"}, t + 1.3);

    // mid-scene reaction so the character does something new partway through
    const beat = t + s.dur * 0.55;
    if (s.dur > 7) {
      tl.to(mas, {scale:1.03, rotation:-2.5, duration:0.34, ease:"power2.out"}, beat);
      tl.to(mas, {scale:1, rotation:0, duration:0.6, ease:"power2.inOut"}, beat + 0.34);
    }

    // exit: drift back out rather than hard-cutting
    tl.to(mas, {y:16, opacity:0, scale:0.97, duration:0.42,
      ease:"power2.in"}, out - 0.42);
  }

  // staggered reveals
  // Full-bleed captures manage their own show/hide cycle below, so they must
  // be left out of this generic stagger - it would reveal all of them at the
  // start of the scene and stack them on top of each other.
  Q('.r', el).filter(n => !n.classList.contains('shot')).forEach((n, i) => {
    tl.fromTo(n, {y:22, opacity:0},
      {y:0, opacity:1, duration:0.5, ease:"power3.out"}, t + 0.5 + i * 0.16);
  });

  // bars and year columns grow
  Q('.barfill', el).forEach((n, i) =>
    tl.fromTo(n, {scaleX:0}, {scaleX:1, duration:0.85, ease:"power2.out"}, t + 0.75 + i*0.16));
  Q('.ybar', el).forEach((n, i) =>
    tl.fromTo(n, {scaleY:0}, {scaleY:1, duration:0.6, ease:"power2.out"}, t + 0.6 + i*0.07));

  // diagram: each box lights up in sequence, the connecting line ahead of
  // it draws in step, and the final frame holds every box lit so the whole
  // flow reads as one picture before the scene ends.
  const flowBoxes = Q('[data-flow-i]', el);
  const flowLines = Q('[data-flow-line]', el);
  const FLOW_STEP = 1.15;
  flowBoxes.forEach((n, i) => {
    const at = t + 0.9 + i * FLOW_STEP;
    tl.call(() => n.classList.add('active'), [], at);
    if (flowLines[i]) tl.call(() => flowLines[i].classList.add('drawn'), [], at + 0.25);
  });

  // --- screenshot choreography -------------------------------------------
  // A static capture at thumbnail size is unreadable. Each shot instead gets
  // its own window of the scene: it scales up to fill the stage, holds while
  // the voice talks about it, pans slowly across the detail, then recedes so
  // the next one can take over.
  const shots = Q('.shots .shot', el);

  // Full-bleed captures: hold each one completely still and cross-fade to
  // the next. No zoom, no pan - any sub-pixel movement resamples the image
  // every frame and smears exactly the small UI text we are trying to show.
  if (shots.length && el.classList.contains('bleed')) {
    // Each capture runs a cycle: sit back as a small card for context, push
    // in to full frame, HOLD PERFECTLY STILL while the detail is discussed,
    // then pull back to the same small position before the next one.
    //
    // The still hold is the whole point. The element is laid out at frame
    // size, so "full" is scale(1) - the browser blits the image 1:1 with no
    // resampling, and the small state is the transformed one. Any drift
    // during the hold would resample every frame and soften the text.
    // Every capture now fills the frame at scale 1, so one pull-back factor
    // works for all of them.
    const SMALL = 0.66;
    const intro = 0.7;
    const push = 0.75;                       // zoom in / out duration
    const FADE_ = 0.4;
    // Budget the scene across the captures: each cycle costs two pushes plus
    // the fades between them, and whatever is left becomes the still hold.
    const overhead = push * 2 + FADE_ * 2 + 0.45;
    const span = (s.dur - intro - 0.4) / shots.length;
    const hold = Math.max(1.4, span - overhead);

    // Walk a single clock through the captures so each one's reveal is
    // derived from when the previous one actually finished hiding. Deriving
    // both from the nominal slot start let the windows overlap.
    const FADE = 0.4;
    let cursor = t + intro;

    shots.forEach((fig, i) => {
      const last = i === shots.length - 1;
      fig.classList.add('small');
      gsap.set(fig, {scale: SMALL});

      const show = cursor;
      // every capture starts hidden (CSS) and is explicitly faded in and out
      if (i === 0) {
        tl.fromTo(fig, {opacity:0, y:20},
          {opacity:1, y:0, duration:0.5, ease:"power3.out"}, t + 0.15);
      } else {
        tl.fromTo(fig, {opacity:0},
          {opacity:1, duration:FADE, ease:"none"}, show);
      }

      // small -> full
      const push0 = show + (i === 0 ? 0.35 : FADE + 0.1);
      tl.to(fig, {scale:1, duration:push, ease:"power2.inOut",
        onStart: () => fig.classList.remove('small'),
        onReverseComplete: () => fig.classList.add('small')}, push0);
      // ... then nothing animates at all for the length of the hold ...
      // full -> small, back to exactly where it started
      const pullBack = push0 + push + hold;
      tl.to(fig, {scale:SMALL, duration:push, ease:"power2.inOut",
        onComplete: () => fig.classList.add('small')}, pullBack);

      // hide only once it is fully back at the small size
      const hide = pullBack + push;
      if (!last) {
        tl.to(fig, {opacity:0, duration:FADE, ease:"none"}, hide);
        cursor = hide + FADE;   // next capture starts after this one is gone
      }

      // the title band would cover the capture at full size, so lift it
      // while the image is pushed in and bring it back when it pulls out
      const head = el.querySelector('.head');
      if (head) {
        tl.to(head, {opacity:0, y:-18, duration:0.4, ease:"power2.in"},
          push0 + push * 0.45);
        tl.to(head, {opacity:1, y:0, duration:0.45, ease:"power2.out"},
          pullBack + push * 0.4);
      }
      // Same for the mascot. At the small size it stands beside the card, but
      // at full frame it would cover the bottom corner - which on an Excel
      // capture is the sheet tabs and the row numbers, the two things that
      // say "this is the real workbook".
      const masFig = el.querySelector('.mascot');
      if (masFig) {
        tl.to(masFig, {opacity:0, y:24, duration:0.4, ease:"power2.in"},
          push0 + push * 0.45);
        tl.to(masFig, {opacity:1, y:0, duration:0.45, ease:"power2.out"},
          pullBack + push * 0.4);
      }
    });
  } else if (shots.length) {
    const intro = 1.0;                       // title/heading beat first
    const span  = Math.max(2.4, (s.dur - intro - 0.6) / shots.length);

    shots.forEach((fig, i) => {
      const img = fig.querySelector('img');
      const at  = t + intro + i * span;
      const solo = shots.length === 1;
      // Grow enough that UI text is actually readable. With three panels in
      // the row each starts narrow, so the focused one needs a bigger jump
      // than a two-panel scene to reach a legible size.
      const up = solo ? 1.30 : (shots.length >= 3 ? 2.30 : 1.62);
      // the focused shot pulls to centre; the others shrink back, not sideways
      const rest = 0.82;

      tl.fromTo(fig, {opacity:0, scale:rest, y:24},
        {opacity:1, scale:rest, y:0, duration:0.5, ease:"power3.out"}, at - 0.5);

      // Zoom and hold. The shots sit in a left column that is ~1180px wide; a
      // 1.6x scale about the centre overhangs it by ~35% on each side, so the
      // focused shot is nudged toward the middle of that column rather than
      // pushed outward, which would clip it against the frame edge.
      // Pull the focused panel back toward the middle of the content column.
      // Each panel sits at its own slot in the row, so the further it is from
      // centre the more it has to travel; at high zoom it would otherwise
      // grow straight off the edge of the frame.
      const dir = el.classList.contains('mleft') ? -1 : 1;
      const mid = (shots.length - 1) / 2;
      const slot = 330;
      // bias right so a big zoom clears the left edge of the frame
      const bias = shots.length >= 3 ? 150 : 0;
      const lean = solo ? 0 : Math.round(dir * ((mid - i) * slot + bias));
      tl.to(fig, {scale:up, x:lean, zIndex:5, duration:0.85,
        ease:"power2.inOut"}, at);
      // dim whichever shot is not being discussed
      shots.forEach((other, j) => {
        if (j !== i) tl.to(other, {opacity:0.25, scale:rest * 0.94, zIndex:1,
          duration:0.6, ease:"power2.inOut"}, at);
      });
      // slow pan across the capture while it is held
      tl.fromTo(img, {objectPosition:"top left"},
        {objectPosition:"22% 30%", duration:Math.max(1.2, span - 1.1),
         ease:"none"}, at + 0.85);
      // ease back before handing over to the next shot
      if (i < shots.length - 1) {
        tl.to(fig, {scale:rest, x:0, duration:0.7, ease:"power2.inOut"},
          at + span - 0.7);
      }
    });
  }

  // Documents now run through the same full-bleed cycle as the screenshot
  // captures above (they emit .shot elements), so the old fan-out-and-dim
  // gallery animation has been removed - it was what greyed them out.

  // small supporting captures in .aside drift slowly
  Q('.aside img', el).forEach((n, i) =>
    tl.fromTo(n, {scale:1.0}, {scale:1.05, duration:Math.max(2, s.dur-1.5),
      ease:"none"}, t + 0.6 + i*0.1));
});

// captions: one element per cue, faded in and out on the same timeline
const CAPS = ${JSON.stringify(captionsFor(list))};
const capRoot = document.getElementById('caps');
CAPS.forEach((c, i) => {
  const el = document.createElement('div');
  el.className = 'cue';
  el.id = 'cue-' + i;
  el.textContent = c.t;
  capRoot.appendChild(el);
  // hard cut in and out: a cross-fade would briefly stack two cues
  const span = Math.max(0.5, c.b - c.a);
  tl.set(el, {opacity:1}, c.a);
  tl.set(el, {opacity:0}, c.a + span - 0.02);
});

window.__timelines = window.__timelines || {};
window.__timelines[${JSON.stringify(compId)}] = tl;
`;

// UI accents, generated by tools/make_sfx.py. Kept quiet and sparse: a swoosh
// per scene change, a tick as each revealed item lands, a chime on the close.
function sfxFor(list) {
  const cues = [];
  for (const s of list) {
    if (s.localStart > 0.01) {
      cues.push({ src: "swoosh", at: s.localStart - 0.18 });
    }
    const items = (s.numbers || s.bars || s.items || s.boxes || s.documents || []).length;
    for (let i = 0; i < Math.min(items, 8); i++) {
      cues.push({ src: "tick", at: s.localStart + 0.5 + i * 0.16 });
    }
    if (s.kind === "outro") {
      cues.push({ src: "chime", at: s.localStart + 0.6 });
    }
  }
  return cues.map((c, i) =>
    `  <audio class="clip" id="sfx-${i}" src="../assets/sfx/${c.src}.wav" ` +
    `data-start="${Math.max(0, c.at).toFixed(2)}" data-track-index="3"></audio>`
  ).join("\n");
}

function page(compId, list, totalDur) {
  const audio = list.map(s =>
    `  <audio class="clip" src="${s.audio}" data-start="${(s.localStart + LEAD).toFixed(2)}" data-track-index="2"></audio>`
  ).join("\n") + "\n" + sfxFor(list);

  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Sage FR — ${esc(compId)}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>${FONTS}
${CSS}</style></head>
<body>
<div id="root" data-composition-id="${esc(compId)}" data-start="0"
     data-duration="${totalDur.toFixed(2)}" data-width="1920" data-height="1080" data-fps="${FPS}">
${list.map(sceneMarkup).join("\n")}
  <div id="caps"></div>
${audio}
</div>
<script>${RUNTIME(list, totalDur, compId)}</script>
</body></html>`;
}

// ---- write --------------------------------------------------------------
fs.mkdirSync(path.join(ROOT, "parts"), { recursive: true });

const partIds = [];
for (const [n, list] of [...parts.entries()].sort((a, b) => a[0] - b[0])) {
  const d = list.reduce((a, s) => a + s.duration, 0);
  const id = `sage-part${n}`;
  partIds.push({ n, id, dur: d, count: list.length });
  fs.writeFileSync(path.join(ROOT, "parts", `part${n}.html`), page(id, list, d), "utf-8");
  console.log(`part${n}.html  ${list.length} scenes  ${d.toFixed(1)}s  (${PART_TITLES[n]})`);
}

// index.html mounts every part in sequence
let off = 0;
const mounts = partIds.map(p => {
  const m = `  <div class="clip" id="mount-part${p.n}" data-composition-id="${p.id}" ` +
            `data-composition-src="parts/part${p.n}.html" ` +
            `data-start="${off.toFixed(2)}" data-duration="${p.dur.toFixed(2)}" data-track-index="0"></div>`;
  off += p.dur;
  return m;
}).join("\n");

fs.writeFileSync(path.join(ROOT, "index.html"), `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Sage FR — VP Explainer</title>
<style>html,body{margin:0;width:1920px;height:1080px;background:#f4f2f7;overflow:hidden}
#root{position:relative;width:1920px;height:1080px}
.clip{position:absolute;inset:0}</style></head>
<body>
<div id="root" data-composition-id="sage-fr-vp" data-start="0" data-no-timeline
     data-duration="${off.toFixed(2)}" data-width="1920" data-height="1080" data-fps="${FPS}">
${mounts}
</div>
</body></html>`, "utf-8");

const spoken = scenes.reduce((a, s) => a + s.spoken, 0);
console.log(`\nindex.html  ${scenes.length} scenes across ${partIds.length} parts`);
console.log(`narration ${(spoken/60).toFixed(1)} min -> runtime ${(off/60).toFixed(1)} min (${off.toFixed(0)}s)`);
if (spoken === 0) console.log("WARNING: no audio measured — run tools/narrate.py first");
