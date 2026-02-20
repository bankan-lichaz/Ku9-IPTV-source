function main(item) {
    const n = {
        //省台
        'hnws': 145, //河南卫视
        'hnds': 141, //河南都市
        'hnms': 146, //河南民生
        'hmfz': 147, //河南法治
        'hndsj': 148, //河南电视剧
        'hnxw': 149, //河南新闻
        'htgw': 150, //欢腾购物
        'hngg': 151, //河南公共
        'hnxc': 152, //河南乡村
        'hnly': 154, //河南梨园
        'wwbk': 155, //文物宝库
        'wspd': 156, //武术世界
        'hnqy': 157, //河南曲艺
        'ydxj': 163, //移动戏曲
        'xsj': 183, //象视界
        'gxpd': 194, //国学频道
        //市台
        'zz1': 197, //郑州新闻综合
        'kf1': 198, //开封新闻综合
        'ly1': 204, //洛阳新闻综合
        'pds1': 205, //平顶山新闻综合可能看不了仅保留ID
        'ay1': 206, //安阳新闻综合
        'hb1': 207, //鹤壁新闻综合
        'xx1': 208, //新乡新闻综合
        'jz1': 209, //焦作新闻综合
        'py1': 219, //濮阳新闻综合
        'xc1': 220, //许昌新闻综合
        'lh1': 221, //漯河新闻综合
        'smx1': 222, //三门峡新闻综合
        'ny1': 223, //南阳新闻综合
        'sq1': 224, //商丘新闻综合
        'xy1': 225, //信阳新闻综合
        'zk1': 226, //周口新闻综合
        'zmd1': 227, //驻马店新闻综合
        'jy1': 228  //济源新闻综合
    };
    const id = ku9.getQuery(item.url, "id") || 'hnws';
    const channelId = n[id] || n['hnws'];
    const t = Math.floor(Date.now() / 1000);
    const signStr = '6ca114a836ac7d73' + t;
    const sign = ku9.sha256(signStr);
    const apiUrl = 'https://pubmod.hntv.tv/program/getAuth/channel/channelIds/1/' + channelId;
    const headers = {
        'timestamp': t.toString(),
        'sign': sign
    };
    const response = ku9.get(apiUrl, headers);
    
    try {
        const jsonData = JSON.parse(response);
        if (jsonData && jsonData.length > 0 && jsonData[0].video_streams && jsonData[0].video_streams.length > 0) {
            const playurl = jsonData[0].video_streams[0];
            return JSON.stringify({ url: playurl });
        }
    } catch (e) {
        console.error('解析失败:', e);
    }
    
    return JSON.stringify({ url: '解析失败' });
}
