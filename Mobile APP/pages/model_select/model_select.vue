<template>
	<view class="container">
		<!-- 顶部导航栏 -->
		<NavBar title="model" image_align="center"></NavBar>

		<!-- 主体内容 -->
		<view class="main-container">
			<view class="search-container">
				<SearchBar @input='search_history'></searchbar>
			</view>

			<view class="grid-container">
				<view class="template-card" v-for="template in search_list" :key="template.name"
					@click="selectTemplate(template.name)">
					<view class="template-wrapper">
						<image :src="template.img" class="template-image"></image>
					</view>
					<view class="template-name">{{template.name}}</view>
					<view class="show-full-image" @click.stop="showFullImage(template.img)">🔍</view>

				</view>
			</view>
		</view>
		<!-- 底部确认栏 -->
		<view class="footer">
			<view class="selected_wrapper">
				<view class="selected">已选：{{ selectedTemplate || "无" }}</view>
			</view>

			<image src='/static/model_select/confirm_btn.png' class="confirm" @click="confirmSelection"></image>
		</view>

		<!-- 弹窗 -->
		<view v-if="showModal" class="modal-overlay" @click="closeModal">
			<view class="modal-content" @click.stop>
				<image :src="fullImage" alt="Full Size Template"></image>
				<view class="close-btn" @click="closeModal">❌</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				templates: [{
						name: '纸飞机',
						img: '/static/model/1.jpg'
					}, {
						name: '山间小城',
						img: '/static/model/2.jpg'
					},
					{
						name: '狐狸',
						img: '/static/model/3.jpg'
					},
					{
						name: '小狗',
						img: '/static/model/4.jpg'
					}, {
						name: '猫咪',
						img: '/static/model/5.jpg'
					}, {
						name: '小卖部',
						img: '/static/model/6.jpg'
					},
					{
						name: '小狗',
						img: '/static/model/7.jpg'
					},
					{
						name: '鲁迅先生',
						img: '/static/model/8.jpg'
					}, {
						name: '铃兰',
						img: '/static/model/9.jpg'
					}, {
						name: '猫猫队',
						img: '/static/model/10.jpg'
					},
					{
						name: '气球猫',
						img: '/static/model/11.jpg'
					},
					{
						name: '彩色小猫',
						img: '/static/model/12.jpg'
					}, {
						name: '摘星星的小男孩',
						img: '/static/model/13.jpg'
					}, {
						name: '风车',
						img: '/static/model/14.jpg'
					},
					{
						name: '星星与月亮',
						img: '/static/model/15.jpg'
					},
					{
						name: '花屋',
						img: '/static/model/16.jpg'
					}, {
						name: '童话城堡',
						img: '/static/model/17.jpg'
					}, {
						name: '雪中小屋',
						img: '/static/model/18.jpg'
					},
					{
						name: '摘星星的女孩',
						img: '/static/model/19.jpg'
					}
				],
				search_list: [],
				selectedTemplate: '',
				showModal: false,
				fullImage: ''
			};
		},
		onShow() {
			this.search_list = this.templates;
		},
		computed: {
			selectedText() {
				return this.selectedTemplate ? `已选择${this.selectedTemplate}模版` : '未选择';
			}
		},
		methods: {
			selectTemplate(templateName) {
				this.selectedTemplate = this.selectedTemplate === templateName ? '' : templateName;
			},
			search_history(key) {
				this.search_list = [];
				for (var i = 0; i < this.templates.length; i++) {
					var item = this.templates[i];
					var name = item.name;
					var img = item.img;
					if (name.includes(key)) {
						this.search_list.push(item)
					}
				}
			},
			confirmSelection() {
				uni.redirectTo({
					url: '/pages/new_draw/new_draw?stage=1&draw_name=' + this.selectedTemplate
				})
			},
			showFullImage(imageSrc) {
				this.fullImage = imageSrc;
				this.showModal = true;
			},
			closeModal() {
				this.showModal = false;
				this.fullImage = '';
			}
		},
		onBackPress() {
			uni.switchTab({
				url: "/pages/home/home"
			});
			return true;
		},
		onLoad() {
			uni.hideNavigationBarLoading();
		}
	};
</script>

<style scoped>
	@import './model_select.css'
</style>