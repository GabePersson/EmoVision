<template>
	<view class="th-line" v-if="lineShow" @click="checkModel">
		<view :class="[lineShow?'open-line':'close-line']" @click.stop="()=>{}">
			<view class="line-head">线条选择器</view>
			<view class="line-box">
				<view v-for="(item,index) in lineData" :key="item"
				 @click="checkline(item)"
				 :style="{'height':item+'px'}"></view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				lineShow:false,
				lineData:[4,8,12,16,18]
			}
		},
		methods:{
			checkModel() {
				this.lineShow = !this.lineShow;
				if(!this.lineShow) {
					this.$emit('closePop')
				}
			},
			checkline(item) {
				this.lineShow = false;
				this.$emit('setLine',item)
				this.$emit('closePop')
			}
		}
	}
</script>

<style scoped lang="scss">
.th-line{
	width: 100%;
	height: 100%;
	background-color: rgba(0,0,0,0.5);
	position: fixed;
	bottom: 0;
	left: 0;
	z-index: 100;
	display: flex;
	align-items: flex-end;
	>view{
		width: 100%;
		height: 500upx;
		background: #FFFFFF;
		box-shadow: 0 0 10upx #999999;
		border-radius: 60upx 60upx 0 0;
		.line-head{
			text-align: center;
			font-size: 30upx;
			height: 100upx;
			display: flex;
			align-items: center;
			justify-content: center;
			margin-bottom: 20upx;
		}
		.line-box{
			box-sizing: border-box;
			padding: 0 70upx;
			>view{
				margin-bottom:56upx;
				width: 100%;
				background-color: #000;
			}
		}
	}
}
.open-line{
	animation:fadeInUp 0.4s ;
}
.close-line{
	animation:fadeInDown 0.5s ;
}
@keyframes fadeInUp {
	0% {
		opacity: 0;
		-webkit-transform: translate3d(0, 100%, 0);
		transform: translate3d(0, 100%, 0)
	}

	to {
		opacity: 1;
		-webkit-transform: translateZ(0);
		transform: translateZ(0)
	}
}
@keyframes fadeInDown {
	0% {
		opacity: 0;
		-webkit-transform: translate3d(0, -100%, 0);
		transform: translate3d(0, -100%, 0)
	}

	to {
		opacity: 1;
		-webkit-transform: translateZ(0);
		transform: translateZ(0)
	}
}
</style>
