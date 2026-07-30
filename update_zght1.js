const fs = require("fs");

// ⭐ Node18 自带 fetch，不需要 node-fetch
async function fetchWithTimeout(url, timeout = 5000) {
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
    
    // const blockList = ["219.137", "220.122"];
    const blockList = ["219.137"];
    let list = json.results
      .map(item => "http://" + item.host)
      .filter(Boolean)
      .filter(line => !blockList.some(b => line.includes(b)));

    //let list = json.results
    //  .map(item => "http://" + item.host)
    //  .filter(Boolean)
    //  .filter(line => !line.includes("219.137"));   // ⭐ 去除含 219.137 的行

    // ⭐ 取中间开头 21-50 行（你原来的逻辑）
    // list = list.slice(21, 50);

    fs.writeFileSync("ZGHT1", list.join("\n"));

    console.log("✅ ZGHT1 更新成功，输出:", list.length, "条");

  } catch (e) {
    console.error("❌ 更新 ZGHT1 失败:", e);
    process.exit(1);
  }
})();
