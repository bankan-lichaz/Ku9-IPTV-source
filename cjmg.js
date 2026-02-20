function main(item) {
    const apiUrl = 'http://ik.mengzx.cn:3300/' + item.id;
    const res = ku9.request(apiUrl, "GET", null, null, false);
    const response = JSON.parse(res.body);
    return { url: response.data.url };
}
