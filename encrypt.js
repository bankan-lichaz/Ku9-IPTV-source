const fs = require('fs');

// Base64 Encode (UTF‑8 → binary → btoa)
function base64Encode(str) {
    const bytes = new TextEncoder().encode(str);
    let binary = "";
    bytes.forEach(b => binary += String.fromCharCode(b));
    return Buffer.from(binary, 'binary').toString('base64');
}

// XOR
function xorProcess(str, key) {
    let out = "";
    for (let i = 0; i < str.length; i++) {
        out += String.fromCharCode(
            str.charCodeAt(i) ^ key.charCodeAt(i % key.length)
        );
    }
    return out;
}

// Encrypt file
function encryptFile(input, output, key) {
    const plain = fs.readFileSync(input, 'utf8');
    const xor = xorProcess(plain, key);
    const b64 = base64Encode(xor);
    fs.writeFileSync(output, b64);
    console.log(`加密完成 → ${output}`);
}

// -----------------------------
// 读取命令行参数
// -----------------------------
const args = process.argv.slice(2);

let file = "merged_province.txt";
let key = "xhi886";

args.forEach(arg => {
    if (arg.startsWith("file=")) {
        file = arg.replace("file=", "");
    }
    if (arg.startsWith("key=")) {
        key = arg.replace("key=", "");
    }
});

// 覆盖原文件
encryptFile(file, file, key);
