## ** wn-canvas 万能画板**

### **简介**
### powered by <a href="https://github.com/Summer371">    Xiaogang </a>  @2023
###### 万能画板，支持H5和小程序，支持保存图片，支持自定义背景图片，支持自定义画笔颜色，支持自定义画笔粗细，支持自定义画笔橡皮擦，支持自定义画笔撤销，支持自定义画笔清空，支持自定义画笔保存，支持自定义画笔下载，支持自定义画笔下载失败回调

### **效果图**


### **API**
#### **属性(Props)**![img.png](img.png)

| 属性名 | 类型 | 默认值 | 说明     |
| --- | --- |-----|--------|
| saveImageType | String | 1   | 保存图片的类型 1、保存地址 2、保存到本地图片 3、既保存地址 又保存图片 |
| drawImage | String | ""  | 背景图片   |
| drawImage | String | ""  | 背景图片   |


#### **事件(Events)**

| 事件名称 | 返回值    | 说明                       |
| --- |--------|--------------------------|
| saveImage | 图片地址   | H5返回base64地址，小程序返回http链接 |
| dowmloadErr | String | 下载图片失败回调                 |
| isUnderBkg | Boolean | 背景图片是否在画板下显示，擦除将不会擦除背景图                 |

### **快速使用**
###### 基础示例，具体说明参考上面API
```
<template>
	<view class="content">
		<wnCanvas saveImageType="3" @saveImage="saveImage" :drawImage="drawImage" :isUnderBkg="true" @dowmloadErr='dowmloadErr' @dowmloadSuc="dowmloadSuc"></wnCanvas>
	</view>
</template>
<script>
	import wnCanvas from "@/uni_modules/xiaogang-canvas/components/wn-canvas.vue"
	export default {
		components: {
			wnCanvas
		},
		data() {
			return {
				drawImage:require("../../static/head.jpg")//绘制背景图片 不传则为白色背景
			}
		},
		methods: {
			saveImage(url) {
				//画板返回的图片地址
				console.log(url);
			},
			dowmloadErr(err){
				//下载图片失败时的回调
				console.log(err);
			},
			dowmloadSuc(res){
				//下载图片成功时的回调
				console.log(res);
			}
		}
	}
</script>


```
##### **如有问题或建议，欢迎留言或关注公众号「小刚科技站」联系沟通哟**
