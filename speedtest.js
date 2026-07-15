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

async function testUrl(url) {
  try {
    const res = await fetchWithTimeout(url, 3000);

    // ⭐ 最终跳转后的 URL
    const finalUrl = res.url || "";

    // ⭐ 判断是否含有 .m3u8
    if (finalUrl.includes(".m3u8")) {
      return true;
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

    const ok = await testUrl(url);

    if (ok) {
      // 提取域名/IP+端口：在 // 和 下一个 / 之间
      const m = url.match(/^https?:\/\/([^/]+)/);
      if (m) {
        goodHosts.push(m[1]);
        console.log("✔ 合格：", m[1]);
      } else {
        console.log("⚠ 无法解析域名端口：", url);
      }
    } else {
      console.log("✖ 不合格：", url);
    }
  }

  // 多个用 ; 分隔，输出为 RLMG
  fs.writeFileSync("RLMG", goodHosts.join(";"));

  console.log("完成！合格源数量：", goodHosts.length);
})();
