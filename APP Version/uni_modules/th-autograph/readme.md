## **th-autograph 签名画板🚀**
### **API**
#### **属性(Props)**

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| canvasId | String | th-时间戳  | canvasId |
|actionBar  | Array | ['pencli','color','back','clear'] | 操作按钮配置：pencli(线条)  color(颜色)  back(返回)  clear(清空) |
| isDownload | Boolean | true | 是否下载签名 |
| horizontalScreen | Boolean | false  | 是否横屏 |
| fileName | String | 签名 | 下载签名文件名称 |
| delineColor | String | #000 | 线颜色 |
| delineWidth | Number | 4 | 线宽度 |

#### **事件(Events)**

| 事件名称 | 返回值 |说明  |
| --- | --- | --- |
| submit | base64地址 | 非下载签名返回base64地址 |
| dowmloadErr | String | 下载签名失败回调 |

### **快速使用**
###### 基础示例，具体说明参考上面API
```
<template>
	<view class="box">
		<th-autograph 
		:is-download="false" 
		@submit="getFile" 
		canvas-id="autograph">
		</th-autograph>
	</view>
</template>

<script>
	import thAutograph from "../../uni_modules/th-autograph/components/th-autograph/th-autograph.vue"
	export default {
		components:{
			thAutograph
		},
		methods:{
			getFile(path){
				console.log(path)
			}
		}
	}
</script>

<style>
	page{
		width: 100%;
		height: 100%;
	}
	.box{
		width: 100%;
		height: 100%;
	}
</style>

```
##### **如有问题或建议，欢迎留言或加群联系沟通哟（QQ群号：793036961）**
