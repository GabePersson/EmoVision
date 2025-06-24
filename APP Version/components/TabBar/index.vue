<template>
	<view class="tab-bar">
		<view v-for="(item, index) in tabBars" :key="index"
			:class="{ 'tab-item': true, 'selected': selectedTab === item.pagePath }" @click="switchTab(item.pagePath)">
			<image :src="selectedTab === item.pagePath ? item.selectedIconPath : item.iconPath"
				:class="['tab-icon',item.pagePath=='/pages/model_select/model_select'?'new':'other']" />
		</view>
	</view>
</template>

<script>
	export default {
		props: {
			selectedTab: {
				type: String,
				default: '/pages/home/home'
			}
		},
		data() {
			const color = '#FFFFFF66';
			const selectedColor = '#FFF';
			return {
				isHidden: false, // 初始状态为隐藏
				tabBars: [{
						name: '首页',
						iconPath: '../../static/TabBar/home_unactivate.png',
						selectedIconPath: '../../static/TabBar/home_activate.png',
						pagePath: '/pages/home/home',
						color,
						selectedColor,
					},
					{
						name: '新建',
						iconPath: '../../static/TabBar/New.png',
						selectedIconPath: '../../static/TabBar/New.png',
						pagePath: '/pages/model_select/model_select',
						color,
						selectedColor,
					},
					{
						name: '关于',
						iconPath: '../../static/TabBar/me_unactivate.png',
						selectedIconPath: '../../static/TabBar/me_activate.png',
						pagePath: '/pages/about/about',
						color,
						selectedColor,
					}
				]
			};
		},
		methods: {
			switchTab(url) {
				if (url === '/pages/model_select/model_select') {
					uni.redirectTo({
						url: url
					});
				} else if (this.selectedTab !== url) {
					uni.switchTab({
						url: url
					});
				}
			}
		}
	};
</script>


<style scoped>
	@import './index.scss'
</style>