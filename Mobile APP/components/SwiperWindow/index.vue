<template>
	<view class="image-carousel">
		<swiper autoplay="true" interval="3000" circular="true" indicator-dots="true" indicator-active-color="#7F5FFF"
			class="swiper-container">
			<swiper-item v-for="(image, index) in carousel_images" :key="index">
				<image :src="image.src" class="swiper-image"></image>
			</swiper-item>
		</swiper>
	</view>
</template>

<script>
	export default {
		data() {
			return {
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
		}
	}
</script>

<style>
	@import './index.scss'
</style>