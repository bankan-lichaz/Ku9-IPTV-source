const fs = require("fs");
const fetch = require("node-fetch");

// 读取 ZGHT 文件
const hosts = fs.readFileSync("ZGHT", "utf8")
  .split(/\r?\n/)
  .map(s => s.trim())
  .filter(Boolean);

// ⭐ 自定义 fetch 超时函数（3 秒）
function fetchWithTimeout(url, timeout = 3000) {
  return Promise.race([
    fetch(url),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("timeout")), timeout)
    )
  ]);
}

// ⭐ 频道映射表（与你 PHP 完全一致）
const CHANNEL_MAP = [ /* 你的全部规则 */ ];

function normalize(name) {
  let clean = name.replace(/\s+/g, "").replace(/高清|HD|标清|SD/ig, "");
  for (const r of CHANNEL_MAP) {
    if (r.reg.test(clean)) return r.norm;
  }
  return clean;
}

function typeOf(name) {
  if (/^CCTV/i.test(name)) return 1;
  if (/^CGTN/i.test(name)) return 2;
  if (/卫视/i.test(name)) return 3;
  return 4;
}

function cctvNum(name) {
  const m = /^CCTV\s*([0-9]+)/i.exec(name);
  return m ? parseInt(m[1]) : null;
}

(async () => {
  let channels = [];
  let errors = [];

  for (const host of hosts) {
    const url = `http://${host}/iptv/live/1000.json?key=txiptv`;

    try {
      const json = await fetchWithTimeout(url, 3000).then(r => r.json());
      const list = json.data || json;

      for (const item of list) {
        if (!item.name || !item.chid) continue;

        const name = normalize(item.name);
        const chid = item.chid.toString().padStart(4, "0");

        const playUrl =
          `http://${host}/tsfile/live/${chid}_1.m3u8?key=txiptv&playlive=1`;

        channels.push({ name, url: playUrl });
      }

    } catch (e) {
      errors.push(`${host} 请求失败`);
      continue; // ⭐ 自动跳到下一个 host
    }
  }

  // 排序
  channels.sort((a, b) => {
    const ta = typeOf(a.name);
    const tb = typeOf(b.name);
    if (ta !== tb) return ta - tb;

    if (ta === 1) {
      const na = cctvNum(a.name);
      const nb = cctvNum(b.name);
      if (na !== null && nb !== null) return na - nb;
    }

    return a.name.localeCompare(b.name);
  });

  // 输出
  let out = channels.map(ch => `${ch.name},${ch.url}`).join("\n");

  if (errors.length) {
    out += "\n\n# Errors:\n" + errors.join("\n");
  }

  fs.writeFileSync("result.txt", out);
})();
