const fs = require("fs");
const fetch = require("node-fetch");

(async () => {
  const url = "https://iptvs.pes.im/";

  try {
    const json = await fetch(url).then(r => r.json());

    if (!json.results || !Array.isArray(json.results)) {
      console.error("❌ JSON 中没有 results 字段，无法提取 IP:PORT");
      process.exit(1);
    }

    // 提取 host 字段（已经是 ip:port）
    const list = json.results
      .map(item => item.host)
      .filter(Boolean);

    // 写入 ZGHT 文件
    fs.writeFileSync("ZGHT", list.join("\n"));

    console.log("✅ ZGHT 更新成功，总计:", list.length, "条");

  } catch (e) {
    console.error("❌ 更新 ZGHT 失败:", e);
    process.exit(1);
  }
})();
