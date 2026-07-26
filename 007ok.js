function main(item) {

    const episodes = [
        { "name": "007之你死我活（国语）", "duration": "2:02:56", "url": "https://vip1.lz-cdn6.com/20220920/28065_7d414c77/index.m3u8", "skip_start": 60, "skip_end": 90 },
        { "name": "007之俄罗斯之恋（国语）", "duration": "1:56:30", "url": "https://vip1.lz-cdn6.com/20220920/28046_607d2aa4/index.m3u8", "skip_start": 45, "skip_end": 90 },
        { "name": "007之八爪女（国语）", "duration": "2:12:06", "url": "https://vip1.lz-cdn6.com/20220920/28044_2a3dcf6f/index.m3u8", "skip_start": 60, "skip_end": 90 },
        // ……你的所有电影继续保留……
    ];

    function timeToSeconds(t) {
        const p = t.split(":");
        if (p.length === 3) return p[0] * 3600 + p[1] * 60 + p[2] * 1;
        if (p.length === 2) return p[0] * 60 + p[1] * 1;
        return t * 1;
    }

    // 计算总净时长
    let total = 0;
    episodes.forEach(ep => {
        total += timeToSeconds(ep.duration) - (ep.skip_start || 0) - (ep.skip_end || 0);
    });

    const now = Math.floor(Date.now() / 1000);
    const todayStart = Math.floor(new Date().setHours(0,0,0,0) / 1000);
    const secondsSinceMidnight = now - todayStart;

    const lastPos = parseInt(ku9.getCache("last_play_position") || "0");
    const lastTime = parseInt(ku9.getCache("last_play_time") || "0");

    let pos;
    if (lastPos > 0 && lastTime > 0) {
        const diff = now - lastTime;
        pos = (lastPos + diff) % total;
        if (diff > 86400) pos = secondsSinceMidnight % total;
    } else {
        pos = secondsSinceMidnight % total;
    }

    // 找到当前应该播放的电影
    let acc = 0;
    let epIndex = 0;
    let epTime = 0;

    for (let i = 0; i < episodes.length; i++) {
        const ep = episodes[i];
        const dur = timeToSeconds(ep.duration);
        const net = dur - (ep.skip_start || 0) - (ep.skip_end || 0);

        if (pos < acc + net) {
            epIndex = i;
            epTime = (ep.skip_start || 0) + (pos - acc);
            break;
        }
        acc += net;
    }

    // 保存进度
    ku9.setCache("last_play_position", pos.toString(), 86400000);
    ku9.setCache("last_play_time", now.toString(), 86400000);

    const ep = episodes[epIndex];

    return {
        url: ep.url,
        seek: epTime,
        name: ep.name
    };
}
