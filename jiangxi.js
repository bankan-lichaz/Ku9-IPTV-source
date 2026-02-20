//婀樿タ鍗@2025/12/4
function main(item) {
    
    const channelId = item.id;
    
    
    const channelMap = {
        "jx2": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_jxtv2.m3u8",//江西都市
        "jx3": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_jxtv3.m3u8",//江西经济
        "jx5": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_jxtv5.m3u8",//江西农业
         "jx6": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_jxtv6.m3u8",//江西少儿
          "jx7": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_jxtv7.m3u8",//江西新闻
           "nanchang": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_nanchang.m3u8",//江西南昌
            "jiujiang": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_jiujiang.m3u8",//江西九江
             "jdz": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_jingdezhen.m3u8",//江西景德镇
           "px": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_pingxiang.m3u8",//江西萍乡
        "xy": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_xinyu.m3u8",//江西新余
            "yt": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_yingtan.m3u8",//江西鹰潭
            "yc": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_yichun.m3u8",//江西宜春
        "sr": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_shangrao.m3u8", //江西上饶
         "fuzhou": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_fuzhou.m3u8",//江西抚州
         "ja": "https://play-live-hls.jxtvcn.com.cn/live-city/tv_jian.m3u8"//江西吉安
    };
    
    
    const playUrl = channelMap[channelId];
    
    if (!playUrl) {
        return { url: "", headers: {} }; 
    }
    
    
    const headers = {
        "Referer": "https://api.chinaaudiovisual.cn",
        "User-Agent": "aliplayer(appv=1.1.4&av=7.2.0&av2=7.2.0_44961357&os=android&ov=12&dm=M2007J17C)",
        "Origin": "https://api.chinaaudiovisual.cn"
    };
    
    
    return {
        url: playUrl,
        headers: headers
    };
}
