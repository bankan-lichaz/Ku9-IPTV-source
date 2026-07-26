
function main(item) {
	//ku9 web播放 js代码
	//duration本集为时长 
	//url为点播流   
	//skip_start为跳过片头时间以秒为计算单位 
	//skip_end为跳过片头时间以秒为计算单位
	// 完整的电影或者电视剧数据
const episodes = [
    {
        "name": "007之你死我活（国语）",
        "duration": "2:02:56",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28065_7d414c77\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之俄罗斯之恋（国语）",
        "duration": "1:56:30",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28046_607d2aa4\/index.m3u8",
        "skip_start": 45,
        "skip_end": 90
    },
    {
        "name": "007之八爪女（国语）",
        "duration": "2:12:06",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28044_2a3dcf6f\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之太空城（国语）",
        "duration": "2:07:46",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28074_3019ac69\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之女王密使（国语）",
        "duration": "2:23:36",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28069_27f977d7\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之择日而亡（国语）",
        "duration": "2:13:52",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220915\/27795_b95a204c\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之明日帝国（国语）",
        "duration": "2:00:38",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28063_3266194c\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之最高机密（国语）",
        "duration": "2:09:17",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28076_0c5a0353\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之杀人执照（国语）",
        "duration": "2:14:08",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28073_9080939d\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之海底城（国语）",
        "duration": "2:06:58",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28048_45d5bbc5\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之诺博士（国语）",
        "duration": "1:51:08",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28067_81ec849b\/index.m3u8",
        "skip_start": 45,
        "skip_end": 90
    },
    {
        "name": "007之金刚钻（国语）",
        "duration": "2:01:26",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28054_f2832d6f\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之金手指（国语）",
        "duration": "1:51:19",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28056_815da9bf\/index.m3u8",
        "skip_start": 45,
        "skip_end": 90
    },
    {
        "name": "007之金枪人（国语）",
        "duration": "2:04:26",
        "url": "https:\/\/vip1.lz-cdn.com\/20220917\/33093_bd6ef017\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之雷霆杀机（国语）",
        "duration": "2:11:22",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28059_163d7bcd\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之雷霆谷（国语）",
        "duration": "1:58:16",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28057_5598b594\/index.m3u8",
        "skip_start": 45,
        "skip_end": 90
    },
    {
        "name": "007之霹雳弹（国语）",
        "duration": "2:11:41",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28071_ee87d8e3\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之黄金眼（国语）",
        "duration": "2:11:18",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28052_3909df24\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之黎明生机（国语）",
        "duration": "2:12:11",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28061_716bdc98\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007之黑日危机（国语）",
        "duration": "2:07:01",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28050_ca5e4750\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007外传之巡弋飞弹（国语）",
        "duration": "2:14:52",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28042_faa432e1\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007大战猪肉王子（国语）",
        "duration": "39:23",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220915\/27794_e0a75e6d\/index.m3u8",
        "skip_start": 45,
        "skip_end": 60
    },
    {
        "name": "007大战皇家赌场（国语）",
        "duration": "2:25:51",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28038_4b50b28f\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007大破量子危机（国语）",
        "duration": "1:47:40",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28035_8dc6f598\/index.m3u8",
        "skip_start": 45,
        "skip_end": 90
    },
    {
        "name": "007幽灵党（国语）",
        "duration": "2:29:31",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220920\/28040_76c03409\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    },
    {
        "name": "007无暇赴死（国语）",
        "duration": "2:44:49",
        "url": "https:\/\/vip1.lz-cdn6.com\/20220915\/27792_6db8bec4\/index.m3u8",
        "skip_start": 60,
        "skip_end": 90
    }
];

// 将时间字符串转换为秒数 web播放的 js代码
function timeToSeconds(timeStr) {
    const parts = timeStr.split(':');
    if (parts.length === 3) {
        return (parseInt(parts[0]) * 3600) + (parseInt(parts[1]) * 60) + parseInt(parts[2]);
    } else if (parts.length === 2) {
        return (parseInt(parts[0]) * 60) + parseInt(parts[1]);
    }
    return parseInt(timeStr);
}

// 计算净内容总时长（减去所有片头片尾）
let totalNetDuration = 0;
episodes.forEach(episode => {
    const duration = timeToSeconds(episode.duration);
    const skipStart = episode.skip_start || 0;
    const skipEnd = episode.skip_end || 0;
    totalNetDuration += (duration - skipStart - skipEnd);
});

// 获取当前时间戳
const now = Math.floor(Date.now() / 1000);
const todayStart = Math.floor(new Date().setHours(0, 0, 0, 0) / 1000);
const secondsSinceMidnight = now - todayStart;

// 从缓存获取上次播放进度
const lastPlayPosition = parseInt(ku9.getCache('last_play_position') || '0');
const lastPlayTime = parseInt(ku9.getCache('last_play_time') || '0');

// 计算播放位置（基于净内容时长）- 保持原缓存逻辑
let positionInLoop;
if (lastPlayPosition > 0 && lastPlayTime > 0) {
    const timeDiff = now - lastPlayTime;
    positionInLoop = (lastPlayPosition + timeDiff) % totalNetDuration;
    if (timeDiff > 86400) {
        positionInLoop = secondsSinceMidnight % totalNetDuration;
    }
} else {
    positionInLoop = secondsSinceMidnight % totalNetDuration;
}

// 确定当前剧集和播放时间（考虑跳过片头片尾）
let currentEpisode = episodes[0];
let currentEpisodeIndex = 0;
let currentTime = 0;
let accumulatedNetDuration = 0;

for (let i = 0; i < episodes.length; i++) {
    const episode = episodes[i];
    const duration = timeToSeconds(episode.duration);
    const skipStart = episode.skip_start || 0;
    const skipEnd = episode.skip_end || 0;
    const netDuration = duration - skipStart - skipEnd;
    
    if (positionInLoop < (accumulatedNetDuration + netDuration)) {
        currentEpisode = episode;
        currentEpisodeIndex = i;
        currentTime = skipStart + (positionInLoop - accumulatedNetDuration);
        currentTime = Math.max(skipStart, Math.min(currentTime, duration - skipEnd - 1));
        break;
    }
    accumulatedNetDuration += netDuration;
}

// 保存当前播放位置到缓存
ku9.setCache('last_play_position', positionInLoop.toString(), 86400000);
ku9.setCache('last_play_time', now.toString(), 86400000);

// 生成简化的HTML播放器
const htmlContent = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>轮播</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: #000;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }
        #videoContainer {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #000;
        }
        #videoPlayer {
            width: 100%;
            height: 100%;
            object-fit: fill;
            cursor: pointer;
        }
        #progressPanel {
            position: fixed;
            top: 10px;
            right: 10px;
            background: transparent;
            color: white;
            padding: 8px;
            border-radius: 6px;
            font-size: 10px;
            z-index: 1000;
            width: 240px;
            max-height: 85vh;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        #progressPanel.hidden {
            opacity: 0;
            transform: translateX(20px);
            pointer-events: none;
        }
        .episode-item {
            margin-bottom: 6px;
            padding: 8px;
            border-radius: 6px;
            transition: all 0.2s ease;
            background: rgba(76, 175, 80, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 3px solid #4CAF50;
            box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
        }
        .episode-item.current {
            background: rgba(76, 175, 80, 0.5);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.5);
        }
        .episode-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 3px;
        }
        .episode-name {
            font-weight: bold;
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 11px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
        }
        .episode-status {
            font-size: 9px;
            color: #4CAF50;
            margin-left: 5px;
            background: rgba(76, 175, 80, 0.3);
            padding: 2px 6px;
            border-radius: 10px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
        }
        .episode-status.completed {
            color: #ccc;
            background: rgba(255,255,255,0.2);
        }
        .episode-status.pending {
            color: #ff9800;
            background: rgba(255,152,0,0.3);
        }
        .progress-bar {
            width: 100%;
            height: 4px;
            background: rgba(255,255,255,0.2);
            border-radius: 2px;
            overflow: hidden;
            margin: 2px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            border-radius: 2px;
            transition: width 0.5s ease;
            width: 0%;
            box-shadow: 0 0 4px rgba(76, 175, 80, 0.5);
        }
        .progress-time {
            font-size: 9px;
            color: #ddd;
            text-align: right;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
        }
        .panel-title {
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 8px;
            padding-bottom: 5px;
            border-bottom: 1px solid rgba(255,255,255,0.3);
            text-align: center;
            color: white;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
        }
        .current-time {
            font-size: 8px;
            color: #4CAF50;
            margin-top: 2px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
        }
        .skip-notice {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 14px;
            z-index: 1001;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .skip-notice.show {
            opacity: 1;
        }
    </style>
</head>
<body>
    <div id="videoContainer">
        <video id="videoPlayer" controls autoplay playsinline></video>
    </div>
    <div id="progressPanel" class="hidden">
        <div class="panel-title">🎬 当前播放进度列表</div>
        <div id="episodesList"></div>
    </div>
    <div id="skipNotice" class="skip-notice"></div>

    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        const videoPlayer = document.getElementById('videoPlayer');
        const progressPanel = document.getElementById('progressPanel');
        const episodesList = document.getElementById('episodesList');
        const skipNotice = document.getElementById('skipNotice');
        
        const allEpisodes = ${JSON.stringify(episodes)};
        let currentEpisodeIndex = ${currentEpisodeIndex};
        let currentNetPosition = ${positionInLoop};
        let isSaving = false;
        let hidePanelTimeout;
        let hls;
        
        // 时间格式化函数
        function formatTime(seconds) {
            const hrs = Math.floor(seconds / 3600);
            const mins = Math.floor((seconds % 3600) / 60);
            const secs = Math.floor(seconds % 60);
            
            if (hrs > 0) {
                return \`\${hrs}:\${mins.toString().padStart(2, '0')}:\${secs.toString().padStart(2, '0')}\`;
            } else {
                return \`\${mins}:\${secs.toString().padStart(2, '0')}\`;
            }
        }
        
        // 时间字符串转秒数
        function timeToSeconds(timeStr) {
            const parts = timeStr.split(':');
            if (parts.length === 3) {
                return (parseInt(parts[0]) * 3600) + (parseInt(parts[1]) * 60) + parseInt(parts[2]);
            } else if (parts.length === 2) {
                return (parseInt(parts[0]) * 60) + parseInt(parts[1]);
            }
            return parseInt(timeStr);
        }
        
        // 显示跳过提示
        function showSkipNotice(message) {
            skipNotice.textContent = message;
            skipNotice.classList.add('show');
            setTimeout(() => {
                skipNotice.classList.remove('show');
            }, 3000);
        }
        
        // 获取循环显示的剧集（当前集及前后各两集，支持循环）- 显示5集
        function getVisibleEpisodes() {
            const totalEpisodes = allEpisodes.length;
            const visibleEpisodes = [];
            
            for (let offset = -2; offset <= 2; offset++) {
                let index = (currentEpisodeIndex + offset + totalEpisodes) % totalEpisodes;
                const episode = allEpisodes[index];
                
                let type;
                if (offset === 0) {
                    type = 'current';
                } else if (offset < 0) {
                    type = 'past';
                } else {
                    type = 'future';
                }
                
                visibleEpisodes.push({
                    index: index,
                    episode: episode,
                    type: type
                });
            }
            
            return visibleEpisodes;
        }
        
        // 更新进度列表
        function updateProgressList() {
            const visibleEpisodes = getVisibleEpisodes();
            let html = '';
            
            visibleEpisodes.forEach(({index, episode, type}) => {
                const duration = timeToSeconds(episode.duration);
                const skipStart = episode.skip_start || 0;
                const skipEnd = episode.skip_end || 0;
                const playableDuration = duration - skipStart - skipEnd;
                
                let progress = 0;
                let status = 'pending';
                let statusText = '未开始';
                let timeText = formatTime(duration);
                let currentTimeText = '';
                
                if (type === 'past') {
                    progress = 100;
                    status = 'completed';
                    statusText = '已完成';
                } else if (type === 'current') {
                    const currentTime = videoPlayer.currentTime || ${currentTime};
                    progress = Math.min(100, Math.max(0, ((currentTime - skipStart) / playableDuration) * 100));
                    status = 'current';
                    statusText = '播放中';
                    currentTimeText = \`当前: \${formatTime(currentTime)}\`;
                    timeText = \`\${formatTime(currentTime)} / \${formatTime(duration)}\`;
                } else {
                    progress = 0;
                    status = 'pending';
                    statusText = '未开始';
                }
                
                html += \`
                    <div class="episode-item \${type === 'current' ? 'current' : ''}">
                        <div class="episode-header">
                            <div class="episode-name" title="\${episode.name}">\${index + 1}. \${episode.name}</div>
                            <div class="episode-status \${status}">\${statusText}</div>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: \${progress}%"></div>
                        </div>
                        <div class="progress-time">\${timeText}</div>
                        \${currentTimeText ? '<div class="current-time">' + currentTimeText + '</div>' : ''}
                    </div>
                \`;
            });
            
            episodesList.innerHTML = html;
        }
        
        // 切换进度面板显示
        function toggleProgressPanel() {
            if (progressPanel.classList.contains('hidden')) {
                showProgressPanel();
            } else {
                hideProgressPanel();
            }
        }
        
        // 显示进度面板
        function showProgressPanel() {
            progressPanel.classList.remove('hidden');
            resetHidePanelTimeout();
        }
        
        // 隐藏进度面板
        function hideProgressPanel() {
            progressPanel.classList.add('hidden');
            clearTimeout(hidePanelTimeout);
        }
        
        // 重置隐藏面板的定时器
        function resetHidePanelTimeout() {
            clearTimeout(hidePanelTimeout);
            hidePanelTimeout = setTimeout(() => {
                hideProgressPanel();
            }, 10000);
        }
        
        // 检查是否需要跳过片头片尾
        function checkSkipTimes() {
            const currentEpisode = allEpisodes[currentEpisodeIndex];
            const duration = timeToSeconds(currentEpisode.duration);
            const skipStart = currentEpisode.skip_start || 0;
            const skipEnd = currentEpisode.skip_end || 0;
            const currentTime = videoPlayer.currentTime;
            
            // 检查片头跳过
            if (currentTime < skipStart && currentTime > 1) {
                videoPlayer.currentTime = skipStart;
                showSkipNotice('跳过片头...');
                return;
            }
            
            // 检查片尾跳过
            const remainingTime = duration - currentTime;
            if (remainingTime <= skipEnd && remainingTime > 2) {
                playNextEpisode();
                return;
            }
        }
        
        // 播放下一集
        function playNextEpisode() {
            const nextIndex = (currentEpisodeIndex + 1) % allEpisodes.length;
            showSkipNotice('跳过片尾，播放下一集...');
            
            // 保存当前进度
            savePlaybackPosition(false);
            
            // 切换到下一集
            setTimeout(() => {
                switchToEpisode(nextIndex);
            }, 1000);
        }
        
        // 切换到指定剧集
        function switchToEpisode(index) {
            currentEpisodeIndex = index;
            const episode = allEpisodes[currentEpisodeIndex];
            const skipStart = episode.skip_start || 0;
            
            // 停止当前播放
            if (hls) {
                hls.destroy();
            }
            videoPlayer.pause();
            
            // 加载新剧集
            if (Hls.isSupported()) {
                hls = new Hls({
                    enableWorker: true,
                    lowLatencyMode: true,
                    backBufferLength: 90
                });
                
                hls.loadSource(episode.url);
                hls.attachMedia(videoPlayer);
                
                hls.on(Hls.Events.MANIFEST_PARSED, function() {
                    videoPlayer.currentTime = skipStart;
                    videoPlayer.play().catch(e => {
                        console.log('自动播放失败，显示控制条');
                        videoPlayer.controls = true;
                    });
                    updateProgressList();
                });
                
            } else if (videoPlayer.canPlayType('application/vnd.apple.mpegurl')) {
                videoPlayer.src = episode.url;
                videoPlayer.addEventListener('loadedmetadata', function() {
                    videoPlayer.currentTime = skipStart;
                    videoPlayer.play();
                    updateProgressList();
                });
            }
            
            // 更新进度显示
            updateCurrentPosition();
            updateProgressList();
        }
        
        // 更新当前播放位置
        function updateCurrentPosition() {
            const currentEpisode = allEpisodes[currentEpisodeIndex];
            const skipStart = currentEpisode.skip_start || 0;
            
            let accumulated = 0;
            for (let i = 0; i < currentEpisodeIndex; i++) {
                const ep = allEpisodes[i];
                const epDuration = timeToSeconds(ep.duration);
                const epSkipStart = ep.skip_start || 0;
                const epSkipEnd = ep.skip_end || 0;
                accumulated += (epDuration - epSkipStart - epSkipEnd);
            }
            
            currentNetPosition = accumulated + (videoPlayer.currentTime - skipStart);
            
            if (Math.floor(videoPlayer.currentTime) % 10 === 0 && !isSaving) {
                savePlaybackPosition(false);
            }
        }
        
        // 保存播放进度
        function savePlaybackPosition(forceReload) {
            if (isSaving) return;
            
            isSaving = true;
            const saveTime = Math.floor(Date.now() / 1000);
            
            try {
                if (typeof ku90 !== 'undefined' && ku9.setCache0) {
                    ku9.setCache('last_play_position', Math.floor(currentNetPosition).toString(), 86400000);
                    ku9.setCache('last_play_time', saveTime.toString(), 86400000);
                } else {
                    localStorage.setItem('last_play_position', Math.floor(currentNetPosition));
                    localStorage.setItem('last_play_time', saveTime);
                }
            } catch (e) {
                console.error('保存进度失败:', e);
            }
            
            isSaving = false;
            
            if (forceReload) {
                setTimeout(() => {
                    location.reload();
                }, 1000);
            }
        }
        
        // 初始化播放器
        function initPlayer() {
            // 立即显示进度列表
            updateProgressList();
            showProgressPanel();
            
            if (Hls.isSupported()) {
                hls = new Hls({
                    enableWorker: true,
                    lowLatencyMode: true,
                    backBufferLength: 90
                });
                
                hls.loadSource(allEpisodes[currentEpisodeIndex].url);
                hls.attachMedia(videoPlayer);
                
                hls.on(Hls.Events.MANIFEST_PARSED, function() {
                    videoPlayer.currentTime = ${currentTime};
                    videoPlayer.play().catch(e => {
                        console.log('自动播放失败，显示控制条');
                        videoPlayer.controls = true;
                    });
                });
                
            } else if (videoPlayer.canPlayType('application/vnd.apple.mpegurl')) {
                videoPlayer.src = allEpisodes[currentEpisodeIndex].url;
                videoPlayer.addEventListener('loadedmetadata', function() {
                    videoPlayer.currentTime = ${currentTime};
                    videoPlayer.play();
                });
            }
            
            // 监听时间更新
            videoPlayer.addEventListener('timeupdate', function() {
                checkSkipTimes();
                updateCurrentPosition();
                updateProgressList();
            });
            
            // 点击视频切换进度面板显示
            videoPlayer.addEventListener('click', function(event) {
                event.stopPropagation();
                toggleProgressPanel();
            });
            
            // 点击面板外部隐藏面板
            document.addEventListener('click', function(e) {
                if (!progressPanel.contains(e.target) && e.target !== videoPlayer) {
                    hideProgressPanel();
                }
            });
            
            // 面板内点击时不隐藏
            progressPanel.addEventListener('click', function(e) {
                e.stopPropagation();
                resetHidePanelTimeout();
            });
            
            // 监听播放结束
            videoPlayer.addEventListener('ended', function() {
                playNextEpisode();
            });
        }
        
        // 初始化
        window.addEventListener('DOMContentLoaded', initPlayer);
        
        // 页面关闭前保存进度
        window.addEventListener('beforeunload', function() {
            savePlaybackPosition(false);
        });
        
        // 定时保存进度（每30秒）
        setInterval(() => {
            savePlaybackPosition(false);
        }, 30000);
    </script>
</body>
</html>
`;

   // 返回webview播放器
   return { webview: "data:text/html;base64," + ku9.encodeBase64(htmlContent) };
}
