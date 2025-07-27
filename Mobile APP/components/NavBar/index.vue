<template>
	<view class="custom-nav-bar">
		<image :src="image_src" :class="['nav-title',image_align]"></image>
	</view>
</template>

<script>
	export default {
		props: {
			title: {
				type: String,
				default: 'EmoVision'
			},
			image_align: {
				type: String,
				default: 'left'
			}
		},
		computed: {
			image_src() {
				return `/static/NavBar/${this.title}.png`;
			}
		}
	}
</script>

<style scoped>
	@import './index.scss'
</style>