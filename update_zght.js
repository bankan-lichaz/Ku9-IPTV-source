const fs = require("fs");
const fetch = require("node-fetch");

(async () => {
  const url = "https://iptvs.pes.im";

  try {
    const json = await fetch(url).then(r => r.json());

    // iptvs.pes.im 的真实数据结构是 storageData 数组
    // 每个元素里有 resultCount，但真正的源在 json.sources
    // 我们需要从 json.sources 提取 host:port

    const sources = json.sources || [];

    const list = sources
      .map(s => `${s.ip}:${s.port}`)
      .filter(Boolean);

    fs.writeFileSync("ZGHT", list.join("\n"));

    console.log("ZGHT updated, total:", list.length);

  } catch (e) {
    console.error("Failed to update ZGHT:", e);
    process.exit(1);
  }
})();
