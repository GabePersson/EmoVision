<template>
	<view class="search-container">
		<input class="search-input" :placeholder="placeholder" :v-model="inputValue" @input="handle_input" />
		<image class="search-icon" :src="iconSrc" />
	</view>
</template>

<script>
	export default {
		props: {
			value: {
				type: String,
				default: ''
			},
			placeholder: {
				type: String,
				default: '搜索'
			},
			iconSrc: {
				type: String,
				default: '/static/SearchBar/search.png'
			}
		},
		data() {
			return {
				inputValue: this.value
			};
		},
		watch: {
			value(newVal) {
				this.inputValue = newVal;
			}
		},
		methods: {
			handle_input(event) {
				this.$emit('input', event.target.value);
			}
		}
	};
</script>
<style scoped>
	@import "./index.scss";
</style>