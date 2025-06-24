<template>
	<div>
		<!-- 		顶部跳过按钮
		<div class="header">
			<button class="skip-button" @click="skipPage">跳过</button>
		</div> -->

		<!-- 用于加载指定网页的iframe -->
		<iframe :src="iframeSrc" title="浏览网页"></iframe>
	</div>
</template>

<script>
	export default {
		data() {
			return {
请将此处修改为你的sugarbi地址
				iframeSrc: "http://sugar.aipage.com/dashboard/xxx", // 默认加载百度
				draw_name: "",

				context: null,
				ch2en: {
					'喜': 'x',
					'忧': 'y',
					'怒': 'n',
					'惊': 'j',
					'恐': 'k',
					'思': 's',
					'惊恐': 'jk',
					'恐惊': 'jk',
					'惊忧': 'jy',
					'忧惊': 'jy',
					'惊喜': 'jx',
					'喜惊': 'jx',
					'惊思': 'js',
					'思惊': 'js',
					'怒惊': 'nj',
					'惊怒': 'nj',
					'恐忧': 'ky',
					'忧恐': 'ky',
					'恐思': 'ks',
					'思恐': 'ks',
					'怒忧': 'ny',
					'忧怒': 'ny',
					'怒喜': 'nx',
					'喜怒': 'nx',
					'怒思': 'ns',
					'思怒': 'ns',
					'怒恐': 'nk',
					'恐怒': 'nk',
					'忧喜': 'yx',
					'喜忧': 'yx',
					'忧思': 'ys',
					'思忧': 'ys',
					'喜思': 'xs',
					'思喜': 'xs',
					'喜恐': 'xk',
					'恐喜': 'xk'

				}
			};
		},
		onLoad(options) {
			this.draw_name = options.draw_name;
		},
		methods: {
			back_to_draw() {
				console.log(this.draw_name);
				uni.showModal({
					title: '提示',
					content: '请进入下一阶段',
					showCancel: false,
					success: (res) => {
						if (res.confirm) {
							uni.redirectTo({
								url: '/pages/new_draw/new_draw?stage=3&draw_name=' + this.draw_name
							})
						}
					}
				});
			},
			play_bgm(bgm_name) {
				console.log(bgm_name);
				var music_path = '/static/watch_data/' + this.ch2en[bgm_name] + '.mp3';
				this.context = uni.createInnerAudioContext()
				console.log(music_path);
				this.context.src = music_path;
				this.context.autoplay = true;

				// 开始播放的回调函数
				this.context.onPlay(() => {
					console.log('开始播放');
				});
				// 播放报错的事件监听
				this.context.onError((res) => {
					console.log(res.errMsg);
					console.log(res.errCode);
				});
			},
			get_bgm_name() {
				uni.request({
					url: "http://152.136.47.111:25565/music",
					method: "GET",
					success: (res) => {
						this.play_bgm(res.data)
					},
					fail: (err) => {
						console.log(err);
						uni.showToast({
							title: "情绪获取失败，请检查~",
							position: 'bottom'
						});
						this.play_bgm("思");
					}
				});
			}
		},
		mounted() {
			// 设置定时器，2秒后调用 back_to_draw 方法
			setTimeout(() => {
				this.back_to_draw();
			}, 60000); // 2000 毫秒（2秒）后执行
			this.get_bgm_name();

		},
		onBackPress() {
			uni.showModal({
				title: "提示",
				content: "您确认要返回吗？绘画记录将不会保存。",
				success: (res) => {
					uni.switchTab({
						url: "/pages/home/home"
					});
				}

			});
			return true;

		},
		// 禁用返回键关闭弹窗

	};
</script>

<style scoped>
	@import './watch_data.css'
</style>