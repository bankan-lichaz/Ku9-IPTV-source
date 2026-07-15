const fs = require("fs");
const fetch = require("node-fetch");

// 读取 ipv4.txt
const lines = fs.readFileSync("ipv4.txt", "utf8")
  .split(/\r?\n/)
  .map(s => s.trim())
  .filter(Boolean);

// ⭐ 拉流测速函数（拉流 5 秒）
async function testSpeed(url) {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);

    const res = await fetch(url, { signal: controller.signal });

    clearTimeout(timeout);

    if (!res.ok) return false;

    // 读取 5 秒数据
    const reader = res.body.getReader();
    let total = 0;
    const start = Date.now();

    while (Date.now() - start < 5000) {
      const chunk = await reader.read();
      if (chunk.done) break;
      total += chunk.value.length;
    }

    const speedKB = total / 1024 / 5; // KB/s

    return speedKB > 50; // ⭐ 速度阈值（你可以调整）
  } catch (e) {
    return false;
  }
}

(async () => {
  let goodHosts = [];

  for (const line of lines) {
    const [name, url] = line.split(",");
    if (!url) continue;

    console.log("测速中：", url);

    const ok = await testSpeed(url);

    if (ok) {
      // 提取 IP:PORT
      const m = url.match(/http:\/\/(.+?)\//);
      if (m) {
        goodHosts.push(m[1]);
        console.log("✔ 合格：", m[1]);
      }
    } else {
      console.log("✖ 不合格：", url);
    }
  }

  // 输出 RLMG 文件
  fs.writeFileSync("RLMG", goodHosts.join(";"));

  console.log("完成！合格源数量：", goodHosts.length);
})();
