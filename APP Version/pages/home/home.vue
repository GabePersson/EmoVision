<template>
	<view class="container">
		<NavBar></NavBar>
		<view class="main-container">
			<!-- 搜索框 -->
			<view class="search-container">
				<SearchBar @input='search_history' :v-model="input_value"></searchbar>
			</view>


			<!-- 滑窗 -->
			<SwiperWindow></SwiperWindow>

			<!-- 历史记录 -->
			<view class="history-list">
				<image src='@/static/home/history_title.png' class="history-title"></image>
				<view class="history-item" v-for="(item, index) in search_list" :key="index">
					<image class="history-icon" :src=item.content></image>
					<view class="history-info">
						<text class="history-name">{{ item.name }}</text>
						<text class="history-time">{{ item.time }}</text>
					</view>
					<view :class="[haveChecked?'display':'hidden','controller_container']">
						<view class="top_container">
							<image class="top_icon" src="/static/home/top.png" @click="top"></image>
						</view>
						<view class="remove_container">
							<image class="remove_icon" src="/static/home/remove.png" @click="remove"></image>
						</view>
					</view>
					<image class=" checkbox"
						:src="item.checked ? '/static/home/checkbox_checked.png' : '/static/home/checkbox_unchecked.png'"
						@click="toggle_check(index)"></image>
					<!-- 					<view class="button_groups">
						<view class="top_edge">
							<image src="@/static/home/top.png" class="top_icon"></image>
						</view>
						<view class="remove_edge">
							<image src="@/static/home/remove.png" class="remove_icon"></image>
						</view>
					</view> -->
				</view>
				<text class="more-history" @click="enter_history_page">更多历史 ➔</text>
			</view>
		</view>
		<TabBar currentPath='/pages/index/home'></TabBar>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				input_value: "",
				haveChecked: false,
				checkCnt: 0,
				data_list: [{
						name: '1111',
						time: '2024/11/14',
						path: '../../static/c1.png',
						description: '111',
						checked: false
					},
					{
						name: '1',
						time: '2024/11/14',
						path: '../../static/c2.png',
						description: '111222',
						checked: false
					},
					{
						name: '1',
						time: '2024/11/14',
						path: '../../static/c2.png',
						description: '111222',
						checked: false
					},
					{
						name: '1',
						time: '2024/11/14',
						path: '../../static/c2.png',
						description: '111222',
						checked: false
					},
					{
						name: '1',
						time: '2024/11/14',
						path: '../../static/c2.png',
						description: '111222',
						checked: false
					}
				],
				search_list: [],
				max_search_items: 3,

				// 滑窗
				carousel_images: [{
						src: '/static/SliderWindow/1.png'
					},
					{
						src: '/static/SliderWindow/2.png'
					},
					{
						src: '/static/SliderWindow/3.png'
					},
					{
						src: '/static/SliderWindow/4.png'
					},
					{
						src: '/static/SliderWindow/5.png'
					}
				]
			}

		},
		onLoad() {
			uni.hideTabBar();

			var history_list = uni.getStorageSync('history_list');

			if (!history_list) {
				uni.setStorageSync('history_list', JSON.stringify([]));
				console.log("本地没有存储，正在创建存储");
			}

			this.data_list = JSON.parse(history_list);

			this.search_list = this.data_list.slice(0, this.max_search_items);

		},
		methods: {
			enter_history_page() {
				uni.navigateTo({
					url: '/pages/history/history'
				})
			},
			search_history(key) {
				this.search_list = [];
				for (var i = 0; i < Math.min(this.max_search_items, this.data_list.length); i++) {
					var item = this.data_list[i];
					var name = item.name;
					var time = item.time;
					if (name.includes(key) || time.includes(key)) {
						this.search_list.push(item)
					}
				}
			},
			toggle_check(index) {
				this.search_list[index].checked = !this.search_list[index].checked;
				if (this.search_list[index].checked) {
					this.checkCnt += 1;
				} else {
					this.checkCnt -= 1;
				}
				if (this.checkCnt != 0) {
					this.haveChecked = true;
				} else {
					this.haveChecked = false;
				}
			},
			refresh_storage() {
				uni.setStorageSync('history_list', JSON.stringify(this.data_list));
			},
			remove() {
				this.data_list = this.data_list.filter(item => item.checked != true);
				this.search_history(this.input_value);
				this.refresh_storage();
			},
			top() {
				if (this.checkCnt != 1) {
					uni.showToast({
						title: "只能置顶一个元素哟~",
						position: 'bottom'
					});
					return;
				}
				var item_index = this.data_list.findIndex(item => item.checked == true);
				var item = this.data_list[item_index];
				this.data_list.splice(item_index, 1);
				this.data_list.unshift(item);
				this.refresh_storage();
				this.search_history(this.input_value);

			}
		}
	}
</script>

<style scoped>
	@import './home.css'
</style>