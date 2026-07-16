const fs = require("fs");
const fetch = require("node-fetch");

// 读取 ZGHT 文件
const hosts = fs.readFileSync("ZGHT", "utf8")
  .split(/\r?\n/)
  .map(s => s.trim())
  .filter(Boolean);

// ⭐ 真正可中断的 fetch（3 秒）
function fetchWithTimeout(url, timeout = 3000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  return fetch(url, { signal: controller.signal })
    .finally(() => clearTimeout(id));
}

// ⭐ 频道映射表（你的规则）
const CHANNEL_MAP = [
  { reg: /兵器科技/i, norm: "CCTV兵器科技" },
  { reg: /风云音乐/i, norm: "CCTV风云音乐" },
  { reg: /第一剧场/i, norm: "CCTV第一剧场" },
  { reg: /风云足球/i, norm: "CCTV风云足球" },
  { reg: /风云剧场/i, norm: "CCTV风云剧场" },
  { reg: /怀旧剧场/i, norm: "CCTV怀旧剧场" },
  { reg: /女性时尚/i, norm: "CCTV女性时尚" },
  { reg: /世界地理/i, norm: "CCTV世界地理" },
  { reg: /央视台球/i, norm: "CCTV央视台球" },
  { reg: /高.*网/i, norm: "CCTV高尔夫网球" },
  { reg: /文化精品/i, norm: "CCTV文化精品" },
  { reg: /卫生健康/i, norm: "CCTV卫生健康" },
  { reg: /电视指南/i, norm: "CCTV电视指南" },
  { reg: /发现之旅/i, norm: "发现之旅" },
  { reg: /老故事/i, norm: "老故事" },
  { reg: /中学生/i, norm: "中学生" },

  // CGTN
  { reg: /^CGTN.*录.*$/i, norm: "CGTN外语纪录" },
  { reg: /^CGTN.*阿.*$/i, norm: "CGTN阿拉伯语" },
  { reg: /^CGTN.*西.*$/i, norm: "CGTN西班牙语" },
  { reg: /^CGTN.*法.*$/i, norm: "CGTN法语" },
  { reg: /^CGTN.*俄.*$/i, norm: "CGTN俄语" },

  // CETV
  { reg: /早.*教/i, norm: "CETV早期教育" },
  { reg: /^CETV[- ]?1(?![\dA-Za-z]).*$/i, norm: "CETV1" },
  { reg: /^CETV[- ]?2(?![\dA-Za-z]).*$/i, norm: "CETV2" },
  { reg: /^CETV[- ]?3(?![\dA-Za-z]).*$/i, norm: "CETV3" },
  { reg: /^CETV[- ]?4(?![\dA-Za-z]).*$/i, norm: "CETV4" },

  // CHC
  { reg: /动作电影/i, norm: "CHC动作电影" },
  { reg: /家庭影院/i, norm: "CHC家庭影院" },
  { reg: /影迷电影/i, norm: "CHC影迷电影" },
  { reg: /高清电影/i, norm: "CHC影迷电影" },

  // CCTV4 国际版
  { reg: /^CCTV[- ]?4.*欧洲.*$/i, norm: "CCTV4欧洲" },
  { reg: /^CCTV[- ]?4.*美洲.*$/i, norm: "CCTV4美洲" },

  // 特殊频道
  { reg: /^CCTV[- ]?5\+.*$/i, norm: "CCTV5+体育赛事" },
  { reg: /^CCTV[- ]?4K.*$/i, norm: "CCTV4K" },
  { reg: /^CCTV[- ]?8K.*$/i, norm: "CCTV8K" },

  // CCTV 两位数
  { reg: /^CCTV[- ]?10.*$/i, norm: "CCTV10科教" },
  { reg: /^CCTV[- ]?11.*$/i, norm: "CCTV11戏曲" },
  { reg: /^CCTV[- ]?12.*$/i, norm: "CCTV12社会与法" },
  { reg: /^CCTV[- ]?13.*$/i, norm: "CCTV13新闻" },
  { reg: /^CCTV[- ]?14.*$/i, norm: "CCTV14少儿" },
  { reg: /^CCTV[- ]?15.*$/i, norm: "CCTV15音乐" },
  { reg: /^CCTV[- ]?16.*$/i, norm: "CCTV16奥林匹克" },
  { reg: /^CCTV[- ]?17.*$/i, norm: "CCTV17农业农村" },

  // CCTV 一位数
  { reg: /^CCTV[- ]?1(?![\dA-Za-z]).*$/i, norm: "CCTV1综合" },
  { reg: /^CCTV[- ]?2(?![\dA-Za-z]).*$/i, norm: "CCTV2财经" },
  { reg: /^CCTV[- ]?3(?![\dA-Za-z]).*$/i, norm: "CCTV3综艺" },
  { reg: /^CCTV[- ]?4(?![\dA-Za-z]).*$/i, norm: "CCTV4中文国际" },
  { reg: /^CCTV[- ]?5(?![\dA-Za-z]).*$/i, norm: "CCTV5体育" },
  { reg: /^CCTV[- ]?6(?![\dA-Za-z]).*$/i, norm: "CCTV6电影" },
  { reg: /^CCTV[- ]?7(?![\dA-Za-z]).*$/i, norm: "CCTV7国防军事" },
  { reg: /^CCTV[- ]?8(?![\dA-Za-z]).*$/i, norm: "CCTV8电视剧" },
  { reg: /^CCTV[- ]?9(?![\dA-Za-z]).*$/i, norm: "CCTV9纪录" },

  // 全国卫视
  { reg: /北京卫视/i, norm: "北京卫视" },
  { reg: /东方卫视/i, norm: "东方卫视" },
  { reg: /湖南卫视/i, norm: "湖南卫视" },
  { reg: /浙江卫视/i, norm: "浙江卫视" },
  { reg: /江苏卫视/i, norm: "江苏卫视" },
  { reg: /广东卫视/i, norm: "广东卫视" },
  { reg: /山东卫视/i, norm: "山东卫视" },
  { reg: /东南卫视/i, norm: "东南卫视" },
  { reg: /深圳卫视/i, norm: "深圳卫视" },
  { reg: /安徽卫视/i, norm: "安徽卫视" },
  { reg: /四川卫视/i, norm: "四川卫视" },
  { reg: /重庆卫视/i, norm: "重庆卫视" },
  { reg: /天津卫视/i, norm: "天津卫视" },
  { reg: /湖北卫视/i, norm: "湖北卫视" },
  { reg: /河北卫视/i, norm: "河北卫视" },
  { reg: /河南卫视/i, norm: "河南卫视" },
  { reg: /海南卫视/i, norm: "海南卫视" },
  { reg: /山西卫视/i, norm: "山西卫视" },
  { reg: /江西卫视/i, norm: "江西卫视" },
  { reg: /广西卫视/i, norm: "广西卫视" },
  { reg: /陕西卫视/i, norm: "陕西卫视" },
  { reg: /吉林卫视/i, norm: "吉林卫视" },
  { reg: /黑龙江卫视/i, norm: "黑龙江卫视" },
  { reg: /辽宁卫视/i, norm: "辽宁卫视" },
  { reg: /青海卫视/i, norm: "青海卫视" },
  { reg: /宁夏卫视/i, norm: "宁夏卫视" },
  { reg: /甘肃卫视/i, norm: "甘肃卫视" },
  { reg: /贵州卫视/i, norm: "贵州卫视" },
  { reg: /云南卫视/i, norm: "云南卫视" },
  { reg: /新疆卫视/i, norm: "新疆卫视" },
  { reg: /内蒙古卫视/i, norm: "内蒙古卫视" },
  { reg: /西藏卫视/i, norm: "西藏卫视" },
];

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

async function tryJsonApi(host) {
  const url = `${host}/iptv/live/1000.json?key=txiptv`;

  try {
    const json = await fetchWithTimeout(url, 3000).then(r => r.json());
    const list = json.data || json;

    let found = [];

    for (const item of list) {
      if (!item.name || !item.chid) continue;

      const name = normalize(item.name);
      const chid = item.chid.toString().padStart(4, "0");

      const playUrl =
        `${host}/tsfile/live/${chid}_1.m3u8?key=txiptv&playlive=1`;

      found.push({ name, url: playUrl });
    }

    return { ok: true, list: found, log: `✔ ${host} JSON接口成功，频道数量：${found.length}` };

  } catch (e) {
    return { ok: false, log: `✖ ${host} JSON接口失败：${e.name === "AbortError" ? "超时中断" : e.message}` };
  }
}

async function tryStreamerApi(host) {
  const url = `${host}/streamer/list`;

  try {
    const json = await fetchWithTimeout(url, 3000).then(r => r.json());

    if (!Array.isArray(json)) {
      return { ok: false, log: `✖ ${host} Streamer接口返回非数组` };
    }

    let found = [];

    for (const d of json) {
      const name = normalize(d.name || "");
      const key = (d.key || "").trim();

      if (!name || !key) continue;

      const playUrl = `${host}/hls/${key}/index.m3u8`;

      found.push({ name, url: playUrl });
    }

    return { ok: true, list: found, log: `✔ ${host} Streamer接口成功，频道数量：${found.length}` };

  } catch (e) {
    return { ok: false, log: `✖ ${host} Streamer接口失败：${e.name === "AbortError" ? "超时中断" : e.message}` };
  }
}

(async () => {
  let channels = [];
  let logs = [];
  let errors = [];

  console.log("开始抓取频道，共有源：", hosts.length);

  for (const host of hosts) {
    console.log(`⏳ 正在请求：${host}`);

    // ① 先尝试 JSON API
    let r1 = await tryJsonApi(host);
    logs.push(r1.log);

    if (r1.ok) {
      channels.push(...r1.list);
      continue;
    }

    // ② JSON 失败 → 尝试 streamer/list
    let r2 = await tryStreamerApi(host);
    logs.push(r2.log);

    if (r2.ok) {
      channels.push(...r2.list);
      continue;
    }

    // 两种都失败
    errors.push(`${host} 请求失败`);
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

  let out = channels.map(ch => `${ch.name},${ch.url}`).join("\n");

  out += "\n\n# Fetch Logs:\n" + logs.join("\n");

  if (errors.length) {
    out += "\n\n# Errors:\n" + errors.join("\n");
  }

  fs.writeFileSync("result.txt", out);

  console.log("完成！总频道数：", channels.length);
})();
