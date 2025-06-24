<template>
	<view class="box">
		<th-autograph :isDownload=false :background_name=draw_name @confirm="next" canvas-id="autograph" ref="child">
		</th-autograph>
	</view>
</template>

<script>
	import thAutograph from "../../uni_modules/th-autograph/components/th-autograph/th-autograph.vue"
	import {
		pathToBase64,
		base64ToPath
	} from 'image-tools'
	export default {
		components: {
			thAutograph
		},
		data() {
			return {
				stages: '1',
				draw_name: '1',
				zh2en: {
					"纸飞机": "1",
					"山间小城": "2",
					"狐狸": "3",
					"小狗": "4",
					"猫咪": "5",
					"小卖部": "6",
					"小狗": "7",
					"鲁迅先生": "8",
					"铃兰": "9",
					"猫猫队": "10",
					"气球猫": "11",
					"彩色小猫": "12",
					"摘星星的小男孩": "13",
					"风车": "14",
					"星星与月亮": "15",
					"花屋": "16",
					"童话城堡": "17",
					"雪中小屋": "18",
					"摘星星的女孩": "19"
				}
			}
		},
		onShow() {
			uni.hideTabBar();
			// 动态切换为横屏
			this.$nextTick(() => {
				this.$refs.child.set_timer();
			});
		},
		beforeDestroy() {
			this.$refs.child.uninstall_timer();
		},
		onHide() {
			this.$refs.child.uninstall_timer();
		},
		methods: {
			async next() {
				if (this.stages == '1') {
					uni.showModal({
						title: '提示',
						content: '确定要进入下一阶段吗？',
						success: (res) => {
							if (res.confirm) {
								uni.request({
请设置你的api地址
									url: "http://xxx.xxx.xxx.xxx:25565/enterNextStage",
									method: "POST"
								});
								console.log("准备进入下一阶段", this.draw_name);
								uni.redirectTo({
									url: '/pages/watch_data/watch_data?draw_name=' + this
										.draw_name
								})
							} else if (res.cancel) {}
						}
					});
				} else {
					const res = await uni.request({
请设置api地址
						url: "http://xxx.xxx.xxx.xxx:25565/most_emo",
						method: "GET"
					});
					const draw_path = await this.$refs.child.canvasToFilPath();
					const data = await pathToBase64(draw_path);
					var the_name = null;
					if (res[1].statusCode == 200) {
						the_name = res[1].data;
					} else {
						the_name = "思";
					}
					console.log(res);
					uni.showModal({
						title: '提示',
						content: '确定要结束绘画吗？',
						success: res => {
							if (res.confirm) {
								uni.request({
请设置api地址
									url: "http://xxx.xxx.xxx.xxx:25565/stopNextStage",
									method: "POST"
								});

								let history_list = JSON.parse(uni.getStorageSync("history_list"));
								history_list.unshift({
									name: the_name,
									time: new Date().toISOString().slice(0, 10),
									content: data,
									description: this.$refs.child.get_img_desc(),
									checked: false
								});
								uni.setStorageSync("history_list", JSON.stringify(history_list));
								this.$refs.child.clear_data();
								uni.reLaunch({
									url: '/pages/home/home'
								})
							} else if (res.cancel) {}
						}
					});

				}
			}
		},
		onLoad(options) {
			this.stages = options.stage;
			console.log(options);
			if (options.draw_name != "") {
				this.draw_name = this.zh2en[options.draw_name];
			}

			uni.hideNavigationBarLoading();
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

			})
			return true;

		},
	}
</script>

<style>
	@import './new_draw.css'
</style>