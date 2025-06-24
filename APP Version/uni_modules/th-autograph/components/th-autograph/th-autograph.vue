<template>
	<view class="autograph-box" :style="{'padding-bottom': bottomHeight + 'px'}">
		<!-- 画板 -->
		<canvas class="autograph" v-show="canvasShow" :class="{'hidden': !canvasShow}" :canvas-id="canvasId"
			:id="canvasId" @touchstart="canvasStart($event)" @touchmove="canvasMove($event)" disable-scroll:true>
			<view v-if="history.length==0" :class="['default-text',horizontalScreen?'rote-text':'']">绘制区域</view>
		</canvas>
		<!-- 使用工具时的遮盖 -->
		<view v-show="!canvasShow" class="autograph" :class="{'hidden': canvasShow, 'rote-text': horizontalScreen }">配置中
		</view>

		<image class="draw_tool_btn" :style="{ left: `${tool_currentX}px`, top: `${tool_currentY}px` }"
			src="/static/draw/draw_tool_btn.png" @click="change_head_toggle_visual"
			@touchstart="startDrag($event,'tool')" @touchmove="dragging($event, 'tool')" @touchend="endDrag">
		</image>
		<!-- 确认结束绘画按钮 -->
		<image class="confirm_btn" :style="{ left: `${confirm_btn_currentX}px`, top: `${confirm_btn_currentY}px` }"
			src="/static/draw/confirm_btn.png" @touchstart="startDrag($event,'confirm')"
			@touchmove="dragging($event, 'confirm')" @touchend="endDrag" @click="confirm">
		</image>

		<!-- 上方工具栏 -->
		<view :class="['head_toggle',head_toggle_visible?'visible':'hidden']">
			<image class="head_toogle_icon" src="../../static/th-autograph/pencli.svg" @click="openAction('thLine')"
				v-if="judge('pencli')" title="画笔"></image>
			<image class="head_toogle_icon" src="../../static/th-autograph/color.svg" @click="openAction('thColor')"
				v-if="judge('color')" title="颜色"></image>
			<image class="head_toogle_icon" src="../../static/th-autograph/back.svg" @click="goBack"
				v-if="judge('back')" title="撤销"></image>
			<image class="head_toogle_icon" src="../../static/th-autograph/clear.svg" @click="clear"
				v-if="judge('clear')" title="清空"></image>

		</view>


		<!-- 左侧的工具栏 -->
		<view :class="['left_toggle',left_toggle_visible?'visible':'hidden']">
			<view class="left_toggle_title">
				<image class="left_toggle_title_img" src="/static/draw/title.png"></image>
			</view>
			<view class="left_main_container">
				<view class="left_top_tool">
					<view class="ref_img_container">
						<image class="generate_img" :src="img_path.ref" @click="put_ref_img"></image>
					</view>
					<view class="re_and_put_group">
						<image class="regenerate_btn" src="/static/draw/regenerate_btn.png" @click="generate_ref_img">
						</image>
						<image class="put_btn"
							:src="canPut?'/static/draw/can_delete.png':'/static/draw/cannot_delete.png'"
							@click="remove_ref_image">
						</image>
					</view>
					<view class="prompt_input_wrapper">
						<input class="prompt_input" v-model="prompt" placeholder="请输入" />
						<image class="voice_icon"
							:src="is_recording?'/static/draw/voice_enable.png':'/static/draw/voice.png'"
							@click="toggle_speech_recognition">
						</image>
					</view>
					<image class="start_generate_btn" src="/static/draw/staert.png" @click="generate_next_img">
					</image>
					<slider class="finetune_ref_width" :value="ref_width" @changing="slider_width_change" min=100
						max=500>
						宽度
					</slider>
					<slider class="finetune_ref_height" :value="ref_height" @changing="slider_height_change" min=100
						max=500>高度
					</slider>
				</view>
				<view class="left_bottom_tool">
					<image class="logo" src="/static/draw/logo.png"></image>
					<image class="hide_left_btn" src="/static/draw/hide_left_btn.png"
						@click="change_left_toggle_visual"></image>
				</view>
			</view>
		</view>

		<!-- 关闭/回到上一界面 -->
		<image class="close_btn" src="/static/draw/close.png" @click="close"></image>
		<image class="show_left_btn" src="/static/draw/show_left_btn.png" @click="change_left_toggle_visual">
		</image>

		<!-- 隐藏的参考图层 -->
		<image :class="[ref_layer_hidden?'hidden':'display','ref_layer']"
			:style="{ left: `${ref_currentX}px`, top: `${ref_currentY}px`,width:`${ref_width}px`,height:`${ref_height}px` }"
			@touchstart="startDrag($event,'ref')" @touchmove="dragging($event, 'ref')" @touchend="endDrag"
			:src="ref_path"></image>


		<th-color ref="thColor" @setColor="setColor" @closePop="canvasShow = true"></th-color>
		<th-line ref="thLine" @setLine="setLine" @closePop="canvasShow = true"></th-line>
	</view>
</template>
<script>
	/**
	 * @property {Array} actionBar 操作按钮配置 pencli(线条)  color(颜色)  back(返回)  clear(清空)
	 * @property {String} canvasId CanvasId
	 * @property {Boolean} isDownload 是否下载签名
	 * @property {Boolean} horizontalScreen 是否横屏
	 * @property {String} fileName 文件名称
	 * @property {String} delineColor 线颜色
	 * @property {Number} delineWidth 线宽度
	 **/
	import thColor from "./th-color.vue"
	import thLine from "./th-line.vue"
	export default {
		props: {
			//canvasId
			canvasId: {
				type: String,
				default: `th-${Date.now()}`
			},
			//配置栏
			actionBar: {
				type: Array,
				default: () => {
					return [
						'pencli',
						'color',
						'back',
						'clear'
					]
				}
			},
			//是否下载签名
			isDownload: {
				type: Boolean,
				default: false
			},
			//是否横屏
			horizontalScreen: {
				type: Boolean,
				default: false
			},
			//文件名称
			fileName: {
				type: String,
				default: '签名'
			},
			//线颜色
			delineColor: {
				type: String,
				default: '#000'
			},
			//线宽度
			delineWidth: {
				type: Number,
				default: 4
			},
			background_name: {
				type: String,
				default: '1'
			}
		},
		computed: {
			model_src() {
				return `/static/model/${this.background_name}.jpg`
			}
		},
		data() {
			return {
				context: null,
				history: [],
				lineColor: this.delineColor,
				lineWidth: this.delineWidth,
				canvasShow: true,
				bottomHeight: 0,
				canvasWidth: 0,
				canvasHeight: 0,
				toolbarVisible: true, // Initially hidden toolbar
				head_toggle_visible: true,
				left_toggle_visible: true,
				touchStartY: 0, // To track the Y position of the touch start for swipe detection
				isDragging: false, // 是否正在拖动
				startX: 0, // 初始触摸点X坐标
				startY: 0, // 初始触摸点Y坐标
				tool_currentX: 300, // 屏幕宽度减去按钮宽度和右侧间距
				tool_currentY: 200, // 屏幕高度减去按钮高度和底部间距
				confirm_btn_currentX: 290,
				confirm_btn_currentY: 600,

				offsetX: 0, // 按钮的偏移量
				offsetY: 0, // 按钮的偏移量

				prompt: "",
				// 录音用
				recorder_manager: null,
				is_recording: false,
				audio_path: "",
				ref_left: 0,
				ref_top: 0,

				// 参考图像用
				img_path: {
					"ref": "/static/draw/sample_generation.jpg",
					"next_step": ""
				},
				is_generating_next: false,
				is_generating_ref: false,
				// 参考图层
				ref_path: "/static/draw/sample_generation.jpg",
				ref_layer_hidden: true,
				ref_currentY: 200,
				ref_currentX: 200,
				ref_width: 160,
				ref_height: 160,

				// 各类情绪分析计时器
				text_analyse_timer: null,
				picture_analyse_timer: null,

				canPut: false,

				desc: "",

			};
		},

		components: {
			thColor,
			thLine
		},
		mounted() {
			// #ifdef MP-WEIXIN
			this.getIphoneBottom()
			// #endif
			this.lineColor = this.delineColor
			this.lineWidth = this.delineWidth
			const ctx = uni.createCanvasContext(this.canvasId, this);
			this.context = ctx;
			this.$nextTick(() => {
				const button = this.$refs.toggleButton;
				this.initCanvas();
			});
			this.img_path.ref = this.model_src;
			this.ref_path = this.model_src;
		},
		methods: {
			slider_width_change(e) {
				this.ref_width = e.detail.value;
			},
			slider_height_change(e) {
				this.ref_height = e.detail.value;
			},
			put_ref_img() {
				this.ref_path = this.img_path["ref"];
				this.ref_layer_hidden = false;
				this.canPut = true;

			},
			// draw_ref_image() {
			// 	this.context.drawImage(this.ref_path, this.ref_currentX, this.ref_currentY, this.ref_width, this
			// 		.ref_height);
			// 	this.context.draw(true);
			// 	this.ref_layer_hidden = true;
			// 	this.canPut = false;
			// },
			remove_ref_image() {
				this.ref_layer_hidden = true;
				this.canPut = false;
			},
			clear_data() {
				uni.request({
请修改api地址
					url: "http://xxx.xxx.xxx.xxx:25565/clear",
					method: "GET"
				});
			},
			set_timer() {
				// debug用
				this.text_analyse_timer = setInterval(this.prompt_analyse, 20000);
				this.picture_analyse_timer = setInterval(this.img_recognition, 20000);
			},
			uninstall_timer() {
				clearInterval(this.text_analyse_timer);
				clearInterval(this.picture_analyse_timer);
			},
			prompt_analyse() {
				console.log(this.prompt);
				if (this.prompt == "") {
					return;
				}
				uni.request({
请设置api地址
					url: "http://xxx.xxx.xxx.xxx:25565/process_text_info",
					method: "POST",
					data: {
						text: this.prompt
					},
					success: (res) => {
						console.log("文本情绪分析成功", res);
					},
					fail: (err) => {
						console.log("情绪分析失败", err);
						uni.showToast({
							title: "分析失败，请检查连接",
							position: "bottom"
						})
					}

				})
			},
			get_img_desc() {
				return this.desc;
			},
			async img_recognition() {
				const temp_file_path = await this.canvasToFilPath()
				uni.uploadFile({
请设置api地址
					url: "http://xxx.xxx.xxx.xxx:25564/picture_predict",
					filePath: temp_file_path,
					name: "file",
					success: (res) => {
						console.log("绘画情绪分析成功", res);
						this.desc = res.data;

					},
					fail: (err) => {
						console.log("失败", err);
						uni.showToast({
							title: "分析失败，请检查连接",
							position: "bottom"
						})
					}

				})
			},
			generate_ref_img() {
				if (this.is_generating_ref) {
					uni.showToast({
						title: "正在生成中，请稍等~",
						position: 'bottom'
					})
					return;
				}
				this.is_generating_ref = true;
				uni.request({
请设置api地址
					url: "http://xxx.xxx.xxx.xxx:25565/generate_ref_img",
					method: 'POST',
					data: {
						text: this.prompt
					},
					success: (res) => {
						console.log("成功", res);
						var return_data = res.data;
						if (return_data.image_url == "") {
							uni.showToast({
								title: "生成失败，请检查网络",
								position: "bottom"
							});
						} else {
							this.download_data(return_data.image_url, "ref");
						}
						this.is_generating_ref = false;
					},
					fail: (err) => {
						console.log("失败", err);
						uni.showToast({
							title: "生成失败，请检查连接",
							position: "bottom"
						})
						this.is_generating_ref = false;
					}
				});

			},
			async generate_next_img() {
				if (this.is_generating_next) {
					uni.showToast({
						title: "正在生成中，请稍等~",
						position: 'bottom'
					})
					return;
				}
				this.is_generating_next = true;
				const draw_path = await this.canvasToFilPath()
				uni.uploadFile({
请设置api地址
					url: 'http://xxx.xxx.xxx.xxx:25565/generate_next_img',
					method: "POST",
					filePath: draw_path,
					name: 'file',
					formData: {
						'prompt': this.prompt
					},
					success: (res) => {
						console.log("成功", res);
						var return_data = JSON.parse(res.data);
						if (return_data.image_url == "") {
							uni.showToast({
								title: "生成失败，请联系管理员",
								position: "bottom"
							});
						} else {
							this.download_data(return_data.image_url, "next_step");
						}
						this.is_generating_next = false;
					},
					fail: (err) => {
						console.log("失败", err);
						uni.showToast({
							title: "生成失败，请检查连接",
							position: "bottom"
						})
						this.is_generating_next = false;
					}

				});
			},
			toggle_speech_recognition() {
				if (this.is_recording) {
					this.stop_record();
				} else {
					this.start_record();
				}
			},
			start_record() {
				this.is_recording = true;
				this.recorder_manager = uni.getRecorderManager();
				this.recorder_manager.onStart(() => {

					console.log("开始录音")
					uni.showToast({
						title: "开始录音",
						position: "bottom",
						duration: 1000,
					})
				});

				this.recorder_manager.onStop((res) => {
					console.log('录音停止', res);
					this.audio_path = res.tempFilePath; // 获取音频文件路径
					this.start_speech_recognition(); // 上传音频文件
					uni.showToast({
						title: "录音结束",
						position: "bottom",
						duration: 1000,
					})
				});

				this.recorder_manager.onError((err) => {
					console.log("录音错误", err);
					this.is_recording = false;
				})

				this.recorder_manager.start({
					format: 'MP3', // 设置音频格式
					duration: 10000
				});


			},
			stop_record() {
				this.is_recording = false;
				this.recorder_manager.stop();
			},
			start_speech_recognition() {
				uni.uploadFile({
请设置api地址
					url: 'http://xxx.xxx.xxx.xxx:25565/voice_recognition',
					filePath: this.audio_path,
					name: 'file',
					success: (res) => {
						console.log("成功", res);
						var return_data = JSON.parse(res.data);
						this.prompt = return_data.result;
						console.log(this.prompt);
					},
					fail: (err) => {
						console.log("失败", err);
						uni.showToast({
							title: "语音识别失败，请检查连接",
							position: "bottom"
						})
					}

				})
			},
			download_data(data_url, type) {
				uni.downloadFile({
					url: data_url,
					success: (res) => {
						console.log("下载成功");
						console.log(res.tempFilePath);
						// this.img_path[type] = res.tempFilePath;
						// if (type == "next_step") {
						// 	this.drawNextBackGround();
						// }
						this.img_path["ref"] = res.tempFilePath;
					},
					fail: (err) => {
						console.log("下载失败", err);
					},
				})
			},
			close() {
				uni.redirectTo({
					url: "/pages/model_select/model_select"
				});
			},
			change_head_toggle_visual() {
				this.head_toggle_visible = !this.head_toggle_visible;
			},
			change_left_toggle_visual() {
				this.left_toggle_visible = !this.left_toggle_visible;
			},

			// 拖动开始
			startDrag(event, type) {
				this.isDragging = true; // Set dragging to true when touch starts
				const touch = event.touches[0];
				this.startX = touch.clientX;
				this.startY = touch.clientY;
				if (type == "tool") {
					this.offsetX = this.tool_currentX; // Save current button position as offset
					this.offsetY = this.tool_currentY;
				} else if (type == "confirm") {
					this.offsetX = this.confirm_btn_currentX; // Save current button position as offset
					this.offsetY = this.confirm_btn_currentY;
				} else {
					this.offsetX = this.ref_currentX; // Save current button position as offset
					this.offsetY = this.ref_currentY;
				}
			},

			// Dragging in progress
			dragging(event, type) {
				if (!this.isDragging) return;
				const touch = event.touches[0];
				const deltaX = touch.clientX - this.startX;
				const deltaY = touch.clientY - this.startY;


				if (type == "tool") {
					// 限制按钮移动范围
					const buttonWidth = 42; // 按钮宽度
					const buttonHeight = 42; // 按钮高度
					const margin = -10; // 边距
					this.tool_currentX = Math.min(
						Math.max(this.offsetX + deltaX, margin),
						this.canvasWidth - buttonWidth - margin
					);
					this.tool_currentY = Math.min(
						Math.max(this.offsetY + deltaY, margin),
						this.canvasHeight - buttonHeight - margin
					);
				} else if (type == "confirm") {
					const buttonWidth = 96; // 按钮宽度
					const buttonHeight = 42; // 按钮高度
					const margin = -20; // 边距
					const w_margin = -60;
					this.confirm_btn_currentX = Math.min(
						Math.max(this.offsetX + deltaX, w_margin),
						this.canvasWidth - buttonWidth - w_margin
					);
					this.confirm_btn_currentY = Math.min(
						Math.max(this.offsetY + deltaY, margin),
						this.canvasHeight - buttonHeight - margin
					);
				} else {
					const buttonWidth = this.ref_width; // 按钮宽度
					const buttonHeight = this.ref_height; // 按钮高度
					const margin = -50;
					this.ref_currentX = Math.min(
						Math.max(this.offsetX + deltaX, margin),
						this.canvasWidth - buttonWidth - margin
					);
					this.ref_currentY = Math.min(
						Math.max(this.offsetY + deltaY, margin),
						this.canvasHeight - buttonHeight - margin
					);
				}
			},



			// Dragging ends
			endDrag() {
				this.isDragging = false; // Set dragging to false when touch ends
			},
			// updateButtonPosition() {
			// 	this.$nextTick(() => { // Ensure DOM updates are complete
			// 		const button = this.$refs.toggleButton;
			// 	});
			// },
			confirm() {
				this.$emit('confirm');
			},


			initCanvas() {
				const query = uni.createSelectorQuery().in(this); // 在当前组件实例中查找
				query.select('.autograph-box') // 选择目标节点
					.boundingClientRect((rect) => {
						if (rect) {
							// 获取 Canvas 的宽高
							this.canvasWidth = rect.width;
							this.canvasHeight = rect.height;

							// 在宽高获取成功后调用绘制方法
							this.drawBackGround();
						} else {
							console.error('未能获取 .autograph-box 节点信息，请检查是否正确渲染');
						}
					})
					.exec(); // 执行查询
			},
			drawBackGround() {

				this.context.drawImage('/static/draw/bg.png', 0, 0, this.canvasWidth, this.canvasHeight);
				this.context.draw();
			},
			// drawNextBackGround() {
			// 	this.context.drawImage(this.img_path.next_step, 0, 0, this.canvasWidth, this.canvasHeight);
			// 	this.context.draw();
			// },
			getIphoneBottom() {
				uni.getSystemInfo({
					success: res => {
						const bottom = res.screenHeight - res.safeArea.bottom;
						this.bottomHeight = bottom > 0 ? bottom - 10 : bottom
					}
				})
			},
			//操作栏显示控制
			judge(key) {
				if (this.actionBar.includes(key)) {
					return true
				} else {
					return false;
				}
			},
			//打开选择器
			openAction(ref) {
				this.canvasShow = false
				this.$refs[ref].checkModel()
			},
			//设置颜色
			setColor(color) {
				this.lineColor = color;
			},
			//设置线条
			setLine(width) {
				this.lineWidth = width;
			},
			//切换控制栏
			checkAction() {
				this.actionShow = !this.actionShow
			},
			//保存
			async saveCanvas() {
				const tempFilePath = await this.canvasToFilPath()
				if (!this.isDownload) {
					this.$emit('submit', tempFilePath)
					return false;
				}
				return new Promise((resolve, reject) => {
					// #ifdef H5
					try {
						const a = document.createElement('a')
						a.href = tempFilePath
						a.download = this.fileName
						document.body.appendChild(a)
						a.click()
						a.remove()
						resolve()
					} catch (e) {
						reject(e)
					}
					// #endif
					// #ifndef H5
					uni.saveImageToPhotosAlbum({
						filePath: tempFilePath,
						success(resObj) {
							this.$emit('submit', tempFilePath)
							resolve(resObj)
						},
						fail(err) {
							this.$emit('dowmloadErr', err)
							reject(err)
						}
					})
					// #endif
				})
			},
			// 保存临时路径
			canvasToFilPath(conf = {}) {
				return new Promise((resolve, reject) => {
					uni.canvasToTempFilePath({
						canvasId: this.canvasId,
						success: res => {
							resolve(res.tempFilePath)
						},
						fail: err => {
							reject(err)
						}
					}, this)
				})
			},
			//撤回
			goBack() {
				this.drawBackGround();
				this.history.pop();
				this.history.forEach((item, index) => {
					let {
						color,
						width
					} = item.style
					this.context.beginPath()
					this.context.setLineCap('round')
					this.context.setStrokeStyle(color)
					this.context.setLineWidth(width)
					if (item.coordinates.length >= 2) {
						item.coordinates.forEach(it => {
							if (it.type == 'touchstart') {
								this.context.moveTo(it.x, it.y)
							} else {
								this.context.lineTo(it.x, it.y)
							}
						})
					} else {
						const point = item.coordinates[0]
						this.context.moveTo(point.x, point.y)
						this.context.lineTo(point.x + 1, point.y)
					}
					this.context.stroke()
				})
				this.context.draw(true)
			},
			//清空画布
			clear() {
				this.history = [];
				this.drawBackGround();
			},
			canvasStart(event) {
				let {
					x,
					y
				} = event.touches[0]
				this.history.push({
					style: {
						color: this.lineColor,
						width: this.lineWidth
					},
					coordinates: [{
						type: event.type,
						x: x,
						y: y
					}]
				})
				this.drawGraphics()
			},
			canvasMove(e) {
				// e.preventDefault()
				let {
					x,
					y
				} = e.touches[0]
				this.history[this.history.length - 1].coordinates.push({
					type: e.type,
					x: x,
					y: y
				})
				this.drawGraphics()
			},
			//绘制
			drawGraphics() {
				let historyLen = this.history.length
				if (!historyLen) return
				let currentData = this.history[historyLen - 1]
				let coordinates = currentData.coordinates
				if (!coordinates.length) return
				let startPoint, endPoint;
				if (coordinates.length < 2) {
					startPoint = coordinates[coordinates.length - 1]
					endPoint = {
						x: startPoint.x + 1,
						y: startPoint.y
					}
				} else {
					startPoint = coordinates[coordinates.length - 2]
					endPoint = coordinates[coordinates.length - 1]
				}
				let style = currentData.style
				this.context.beginPath()
				this.context.setLineCap('round')
				this.context.setStrokeStyle(style.color)
				this.context.setLineWidth(style.width)
				this.context.moveTo(startPoint.x, startPoint.y)
				this.context.lineTo(endPoint.x, endPoint.y)
				this.context.stroke()
				this.context.draw(true)
			}
		}
	}
</script>

<style lang="scss" scoped>
	.floating-toolbar {
		position: fixed;
		top: 0px;
		left: 20px;
		z-index: 999;
		display: flex;
		flex-direction: column;
		align-items: center;
	}




	.toolbar-content {
		display: flex;
		align-items: center;
		background-color: rgba(0, 0, 0, 0.7);
		border-radius: 30px;
		padding: 10px;
		box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
	}

	.toolbar-icon {
		width: 40px;
		height: 40px;
		margin: 0 10px;
		cursor: pointer;
		transition: transform 0.2s ease;
	}

	.toolbar-icon:hover {
		transform: scale(1.1);
	}

	.toolbar-submit {
		padding: 8px 20px;
		background-color: #5c6bc0;
		color: white;
		border-radius: 20px;
		font-size: 16px;
		cursor: pointer;
		margin-left: 15px;
		transition: background-color 0.3s ease;
	}

	.toolbar-submit:hover {
		background-color: #3f51b5;
	}


	.autograph {
		width: 100%;
		height: 100%;
		box-sizing: border-box;
		border: 1px dashed #ccc;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 38upx;
		color: #C0C0C0;
	}

	.config {
		width: 100%;
		height: 92%;
		background-color: red;
	}

	.horizontalScreen {
		left: -150upx !important;
		bottom: 0 !important;
		right: auto !important;
		transform: rotate(90deg);
		transform-origin: bottom right;
	}

	.rote-text {
		transform: rotate(90deg);
	}

	.rote-action {
		transform: rotate(180deg);
		padding-top: 0 !important;

		.th-submit {
			transform: rotate(-90deg);
			width: 120upx !important;
			height: 100% !important;
		}
	}

	.action-box {
		height: 8%;
		z-index: 50;
		display: flex;
		flex-direction: row;
		align-items: flex-end;
		justify-content: flex-end;
		box-sizing: border-box;
		padding-top: 20upx;
	}

	.th-submit {
		width: 150upx;
		height: 100%;
		background-color: #5667F5;
		border-radius: 50upx 0 0 0;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #FFFFFF;
		font-size: 30upx;
		transition: all 0.3s;
	}

	.action-bar {
		margin-right: 35upx;
		align-items: center;
		display: flex;
		height: 100%;
		align-items: center;

		image {
			width: 35upx;
			height: 35upx;
		}

		>image {
			transition: all 0.3s;
		}

		>view {
			display: flex;
			flex-direction: row;
			align-items: center;

			image {
				width: 40upx;
				height: 40upx;
				margin-right: 60upx;
			}
		}
	}

	.autograph-box {
		width: 100%;
		height: 100%;
		position: relative;
		box-sizing: border-box;

		.default-text {
			width: 100%;
			height: 100%;
			position: absolute;
			top: 0;
			left: 0;
			display: flex;
			align-items: center;
			z-index: -1;
			justify-content: center;
			font-size: 38upx;
			color: #C0C0C0;
			letter-spacing: 5upx;
		}
	}

	.toggle-button {
		position: fixed;
		/* 使其固定在屏幕上 */
		bottom: 20px;
		/* 默认位置，可以根据需要设置 */
		right: 20px;
		/* 默认位置 */
		width: 50px;
		height: 50px;
		background-color: #5c6bc0;
		border-radius: 50%;
		display: flex;
		justify-content: center;
		align-items: center;
		box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
		cursor: pointer;
		z-index: 9999;
		transition: background-color 0.3s ease;
	}

	.toggle-icon {
		display: block;
		width: 24px;
		/* 设置图标的宽度 */
		height: 24px;
		/* 设置图标的高度 */
		object-fit: contain;
		/* 确保图标适应容器 */
	}

	.toggle-button:hover {
		transform: scale(1.1);

	}



	.vertical-toolbar {
		position: fixed;
		top: 20%;
		/* 工具栏的位置 */
		left: 10px;
		/* 紧贴屏幕左侧 */
		display: flex;
		flex-direction: column;
		align-items: center;
		background-color: rgba(0, 0, 0, 0.7);
		border-radius: 10px;
		padding: 10px 0;
		box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
		z-index: 1000;
		transition: transform 0.3s ease;
	}

	.toolbar-icon-wrapper {
		margin: 10px 0;
	}

	.toolbar-submit-wrapper {
		margin-top: 20px;
		display: flex;
		justify-content: center;
	}

	.vertical-toolbar .toolbar-icon {
		width: 40px;
		height: 40px;
		cursor: pointer;
		transition: transform 0.2s ease;
	}

	.vertical-toolbar .toolbar-icon:hover {
		transform: scale(1.1);
	}

	.vertical-toolbar .toolbar-submit {
		padding: 8px 20px;
		background-color: #5c6bc0;
		color: white;
		border-radius: 20px;
		font-size: 16px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	.vertical-toolbar .toolbar-submit:hover {
		background-color: #3f51b5;
	}

	.vertical-toolbar.visible {
		display: flex;
	}

	.vertical-toolbar.hidden {
		display: none;
	}

	@import url("index.css");
</style>