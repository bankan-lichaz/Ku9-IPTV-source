const fs = require("fs");
const fetch = require("node-fetch");

// ⭐ 真正可中断的 fetch（3 秒）
function fetchWithTimeout(url, timeout = 3000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  return fetch(url, { signal: controller.signal, redirect: "follow" })
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

// ⭐ 判断最终链接是否能播放（拉流 1 秒）
async function canPlay(finalUrl) {
  try {
    const res = await fetchWithTimeout(finalUrl, 3000);
    if (!res.ok) return false;

    const reader = res.body.getReader();
    const start = Date.now();

    while (Date.now() - start < 1000) { // ⭐ 拉流 1 秒
      const chunk = await reader.read();
      if (chunk.done) break;

      if (chunk.value && chunk.value.length > 0) {
        return true; // ⭐ 只要读到数据就算能播放
      }
    }

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

    try {
      // ⭐ 第一步：访问原始 URL（允许跳转）
      const res = await fetchWithTimeout(url, 3000);
      const finalUrl = res.url || "";

      console.log("最终跳转：", finalUrl);

      // ⭐ 第二步：真正判断能不能播放
      const ok = await canPlay(finalUrl);

      if (ok) {
        const m = url.match(/^https?:\/\/([^/]+)/);
        if (m) {
          goodHosts.push(m[1]);
          console.log("✔ 合格：", m[1]);
        }
      } else {
        console.log("✖ 不合格：", url);
      }

    } catch (e) {
      console.log("✖ 错误：", url);
    }
  }

  fs.writeFileSync("RLMG", goodHosts.join(";"));

  console.log("完成！合格源数量：", goodHosts.length);
})();
