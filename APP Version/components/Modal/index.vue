<template>
	<view>
		<!-- 弹窗 -->
		<view v-if="showModal" class="modal-overlay" @click="closeModal">
			<view class="modal-content" @click.stop>
				<view class="modal-header">
					<text class="modal-title">{{ title }}</text>
					<button class="close-btn" @click="closeModal">❌</button>
				</view>
				<view class="modal-body">
					<text>{{ content }}</text>
				</view>
				<view class="modal-footer">
					<button class="cancel-btn" @click="cancelAction">{{ cancelText }}</button>
					<button class="confirm-btn" @click="confirmAction">{{ confirmText }}</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				showModal: false,
				title: "弹窗标题", // 默认标题
				content: "这里是弹窗内容", // 默认内容
				confirmText: "确认", // 默认确认按钮文本
				cancelText: "取消", // 默认取消按钮文本
				confirmCallback: null, // 确认回调
				cancelCallback: null // 取消回调
			};
		},
		methods: {
			// 打开弹窗
			openModal({
				title,
				content,
				confirmText,
				cancelText,
				confirmCallback,
				cancelCallback
			}) {
				this.title = title || this.title;
				this.content = content || this.content;
				this.confirmText = confirmText || this.confirmText;
				this.cancelText = cancelText || this.cancelText;
				this.confirmCallback = confirmCallback;
				this.cancelCallback = cancelCallback;
				this.showModal = true;
			},
			// 关闭弹窗
			closeModal() {
				this.showModal = false;
			},
			// 确认按钮事件
			confirmAction() {
				if (this.confirmCallback) {
					this.confirmCallback();
				}
				this.closeModal();
			},
			// 取消按钮事件
			cancelAction() {
				if (this.cancelCallback) {
					this.cancelCallback();
				}
				this.closeModal();
			}
		}
	}
</script>

<style>
	@import url("index.css");
</style>