// Full-page screenshots of local pages with headless Chrome over CDP.
// Usage: node pageshot.mjs outDir width file1.html [file2.html ...]
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync, readFileSync } from "node:fs";
import { basename, join, resolve } from "node:path";
const [outDir, width, ...files] = process.argv.slice(2);
mkdirSync(outDir, { recursive: true });
const PORT = 9334, sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const chrome = spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", ["--headless=new", `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${join(outDir, ".prof")}`, "--hide-scrollbars", "--no-first-run", "about:blank"], { stdio: "ignore" });
let t; for (let i = 0; i < 50; i++) { try { t = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json(); if (t.length) break; } catch {} await sleep(200); }
const ws = new WebSocket(t.find((x) => x.type === "page").webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0; const pend = new Map();
ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
await send("Page.enable");
for (const f of files) {
  const w = +width;
  await send("Emulation.setDeviceMetricsOverride", { width: w, height: +(process.env.VH || 900), deviceScaleFactor: 2, mobile: w < 600 });
  await send("Page.navigate", { url: "file://" + resolve(f) });
  await sleep(2500);
  await send("Runtime.evaluate", { expression: `(() => {
    const b = document.body.firstElementChild; if (b && /Offline snapshot/.test(b.textContent)) b.remove();
    [...document.querySelectorAll('div')].filter(d => d.children.length === 0 && d.textContent.trim() === 'Development').forEach(d => d.style.visibility = 'hidden');
    document.querySelectorAll('[data-slot="avatar-fallback"]').forEach(a => { const f = a.closest('[data-slot="sidebar-footer"],[data-sidebar="footer"]') || a.parentElement.parentElement; f.style.visibility = 'hidden'; });
    if (${process.env.KEEP_SIDEBAR ? 'false' : 'true'}) { document.querySelectorAll('[data-slot="sidebar"],[data-slot="sidebar-trigger"]').forEach(e => e.style.display = 'none'); }
  })()` });
  const ed = await send("Runtime.evaluate", { expression: readFileSync(new URL("./edits.js", import.meta.url), "utf8"), returnByValue: true });
  console.log(basename(f), "edits", ed.result.result?.value ?? JSON.stringify(ed.result.exceptionDetails?.exception?.description));
  await sleep(1800);
  const h = (await send("Runtime.evaluate", { expression: "document.documentElement.scrollHeight", returnByValue: true })).result.result.value;
  const sw = (await send("Runtime.evaluate", { expression: "document.documentElement.scrollWidth", returnByValue: true })).result.result.value;
  const r = await send("Page.captureScreenshot", { format: "jpeg", quality: 82, captureBeyondViewport: true, clip: { x: 0, y: +(process.env.CLIP_Y || 0), width: w, height: Math.min(h - +(process.env.CLIP_Y || 0), +(process.env.CLIP_H || h)), scale: 1 } });
  writeFileSync(join(outDir, `${basename(f, ".html")}-${w}.jpg`), Buffer.from(r.result.data, "base64"));
  console.log(basename(f), "height", h, "scrollWidth", sw);
}
ws.close(); chrome.kill();
