<template>
	<view class="container">
		<NavBar></NavBar>
		<view class="avatar_container">
			<image :src="avatar_path" class="avatar"></image>
		</view>
		<view class="info_container">
			<view class="username">{{username}}</view>
			<view class="id">ID:{{id}}</view>
		</view>
		<image class="setting" @click="other_button" src="/static/about/setting.png"></image>
		<image class="scan" @click="other_button" src="/static/about/Scan.png"> </image>
		<view class="main-container">
			<view class="page-item" v-for="(item, index) in about" :key="index" @click=item.click>
				<image class="page-icon" :src=item.icon></image>
				<view class="page-info">
					<text class="page-name">{{ item.txt }}</text>
				</view>
			</view>





			<TabBar selectedTab='/pages/about/about'></TabBar>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				username: "用户名",
				id: "1234567",
				about: [{
						"icon": "/static/about/account.png",
						"txt": "账户",
						"click": () => this.other_button()
					},
					{
						"icon": "/static/about/history.png",
						"txt": "情绪历史",
						"click": () => this.enter_history_page()
					},
					{
						"icon": "/static/about/Love.png",
						"txt": "喜欢",
						"click": () => this.other_button()
					},
					{
						"icon": "/static/about/about.png",
						"txt": "关于",
						"click": () => this.other_button()
					}
				]
			}
		},
		methods: {
			enter_history_page() {
				uni.navigateTo({
					url: '/pages/history/history'
				})
			},
			other_button() {
				uni.showToast({
					title: "还在修改中~",
				})
			}
		},
		onLoad() {
			uni.hideTabBar()
		}
	}
	// import CustomTabBar from '@/components/CustomTabBar.vue'
	// export default {
	// 	components: {
	// 		CustomTabBar
	// 	}
	// }
</script>

<style>
	@import url("./about.css");
</style>