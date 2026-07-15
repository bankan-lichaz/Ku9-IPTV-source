const fs = require("fs");
const fetch = require("node-fetch");

// ⭐ 真正可中断的 fetch（3 秒）
function fetchWithTimeout(url, timeout = 3000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  return fetch(url, { signal: controller.signal })
    .finally(() => clearTimeout(id));
}

// 读取 ipv4.txt
const lines = fs.readFileSync("ipv4.txt", "utf8")
  .split(/\r?\n/)
  .map(s => s.trim())
  .filter(Boolean);

// ⭐ 只保留含有 608807420 的链接
const targets = lines.filter(line => line.includes("608807420"));

console.log("需要测试的数量：", targets.length);

async function testUrl(url) {
  try {
    const res = await fetchWithTimeout(url, 3000);

    if (!res.ok) return false;

    // 读取前 1KB 判断是否是 m3u8
    const reader = res.body.getReader();
    const chunk = await reader.read();

    if (chunk.done || !chunk.value) return false;

    const text = Buffer.from(chunk.value).toString("utf8");

    // ⭐ 判断是否返回 m3u8
    if (text.includes("#EXTM3U")) return true;

    return false;

  } catch (e) {
    return false;
  }
}

(async () => {
  let goodHosts = [];

  for (const line of targets) {
    const [name, url] = line.split(",");
    if (!url) continue;

    console.log("测试：", url);

    const ok = await testUrl(url);

    if (ok) {
      const m = url.match(/http:\/\/(.+?)\//);
      if (m) {
        goodHosts.push(m[1]);
        console.log("✔ 合格：", m[1]);
      }
    } else {
      console.log("✖ 不合格：", url);
    }
  }

  fs.writeFileSync("RLMG", goodHosts.join(";"));

  console.log("完成！合格源数量：", goodHosts.length);
})();
