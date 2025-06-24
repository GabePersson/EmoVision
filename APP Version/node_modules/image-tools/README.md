# image-tools
图像转换工具，可用于如下环境：uni-app、微信小程序、5+APP、浏览器（需允许跨域）

## 使用方式

### NPM

```
npm i image-tools --save
```

```js
import { pathToBase64, base64ToPath } from 'image-tools'
```

### 直接下载

```js
// 以下路径需根据项目实际情况填写
import { pathToBase64, base64ToPath } from '../../js/image-tools/index.js'
```

## API

### pathToBase64

从图像路径转换为base64，uni-app、微信小程序和5+APP使用的路径不支持网络路径，如果是网络路径需要先使用下载API下载下来。

```js
pathToBase64(path)
  .then(base64 => {
    console.log(base64)
  })
  .catch(error => {
    console.error(error)
  })
```

### base64ToPath

将图像base64保存为文件，返回文件路径。

```js
base64ToPath(base64)
  .then(path => {
    console.log(path)
  })
  .catch(error => {
    console.error(error)
  })
```

## 提示

可以利用promise来串行和并行的执行多个任务

```js
// 并行
Promise.all(paths.map(path => pathToBase64(path)))
  .then(res => {
    console.log(res)
    // [base64, base64...]
  })
  .catch(error => {
    console.error(error)
  })
// 串行
paths.reduce((promise, path) => promise.then(res => pathToBase64(path).then(base64 => (res.push(base64), res))), Promise.resolve([]))
  .then(res => {
    console.log(res)
    // [base64, base64...]
  })
  .catch(error => {
    console.error(error)
  })
```