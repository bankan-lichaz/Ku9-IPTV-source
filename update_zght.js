const fs = require("fs");
const fetch = require("node-fetch");

// ⭐ 带超时的 fetch（避免卡住）
function fetchWithTimeout(url, timeout = 5000) {
  return Promise.race([
    fetch(url),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("timeout")), timeout)
    )
  ]);
}

(async () => {
  const url = "https://iptvs.pes.im/";

  try {
    const json = await fetchWithTimeout(url, 5000).then(r => r.json());

    if (!json.results || !Array.isArray(json.results)) {
      console.error("❌ JSON 中没有 results 字段，无法提取 IP:PORT");
      process.exit(1);
    }

    // ⭐ 在每行前加 http://
    const list = json.results
      .map(item => "http://" + item.host)
      .filter(Boolean);

    fs.writeFileSync("ZGHT", list.join("\n"));

    console.log("✅ ZGHT 更新成功，总计:", list.length, "条");

  } catch (e) {
    console.error("❌ 更新 ZGHT 失败:", e);
    process.exit(1);
  }
})();
