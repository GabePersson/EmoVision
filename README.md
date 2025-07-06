# <center> **EmoVision：基于多模态情绪调节的艺术疗愈平台** </center>

<center>
    <img style="border-radius: 0.3125em;
    width: 90%;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
    src="https://ai-studio-static-online.cdn.bcebos.com/d756520c1d284eccbc4a68275cdcae8b5b0d3ddad606445aafb1617d94d23295">
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;    
    display: inline-block;
    color: #999;
    padding: 2px;">图1 EmoVision软件标识</div>
</center>

## <center> **项目概述**  </center>

在现代社会，情感健康问题日益凸显，心理压力和情绪波动成为影响人们生活和工作效率的重要因素。根据世界卫生组织数据，全球约有3亿人患有抑郁症，超过2.6亿人患有焦虑症。而COVID-19疫情加剧了这一问题，全球焦虑和抑郁症的患病率增加了25%。同时，由于心理健康意识的不足或专业帮助的难以获取，许多人难以有效应对这些问题。艺术疗愈作为一种非侵入性的心理健康干预方式，近年来逐渐受到关注，但传统的艺术疗愈方式依赖专家指导和面对面互动，存在普及和大规模应用的挑战。 
    
而当前市场上的疗愈软件一般只具有音乐播放、内容推荐等功能，交互性较弱，不能很好地切中用户的核心需求。
因此，为了改善这一现象，本项目旨在通过技术手段，将艺术疗愈数字化、智能化，打造一种普及率更高、更加个性化的情绪疗愈工具。结合多模态大模型的发展，如语音识别、艺术图像生成和面部表情情感分析，为情感识别和调节提供技术基础，实现艺术疗愈的创新应用。

<center>
    <img style="border-radius: 0.3125em;
    width: 90%;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
    src="https://ai-studio-static-online.cdn.bcebos.com/a69a6e1aa6de445eae6dee0707d220c695cf4a78a9a646a8ab2a55d4c71378d6">
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;    
    display: inline-block;
    color: #999;
    padding: 2px;">图2 EmoVision软件整体架构</div>
</center>

EmoVision的系统整体架构如图2所示，主要包括评估、疗愈、检验模块。评估模块中包括基于Vosk本地模型的语音识别功能，基于Paddle的AI作图大模型图像生成功能，基于本地部署模型与Paddle内容理解大模型等等。当用户在使用客户端的时候，我们的软件将会综合用户的文本输入，绘画以及面部等信息，通过我们的多模态数据处理系统识别为特定的情绪占比，并上传至云端。同时，我们的程序在生成了初步的用户画像后，将会自动从我们只做的双插帧音乐数据库中匹配到合适的音乐并进行播放，以便对用户进行疗愈。同时，云端提供了一系列的API系统可供外界进行调用处理。此外，系统还结合了百度的SugarBI数据可视化平台，将情绪进一步直观化，以便用户进行使用。相比于其他的疗愈项目，我们项目的创新点在于：

- **多模态情感识别**：通过语音转文字、文字生成图像、面部表情识别等技术，综合分析用户的情感状态，提高识别的准确性和全面性。  
- **自然与人性化的设计**：提供语音/文字生成画作的替代方案，满足不具备绘画能力的用户需求，通过深度学习模型分析画作中的情感元素。  
- **个性化音乐推荐**：微调音乐插帧模型，构建双情感疗愈音乐数据集，实现用户情感的个性化音乐疗愈。  
- **情感变化的可视化反馈**：通过漂亮的界面直观地展示用户的情感变化过程，有助于自我反思与理解情感。  

系统的主要功能基本可实现本地化部署，在部署后，用户可随时随地使用我们的应用进行疗愈。

**项目界面功能展示：**

<iframe src="//player.bilibili.com/player.html?isOutside=true&aid=113283184990802&bvid=BV1LV25YWE7y&cid=26230326619&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 相关链接
#### **EmoVision项目介绍:【C4AI-2024】EmoVision：基于多模态情绪调节的艺术疗愈平台（https://aistudio.baidu.com/projectdetail/8376625 ）**
#### **EmoVision上线项目：EmoVision-Streamlit（https://aistudio.baidu.com/projectdetail/8374348 ）**
#### **EmoVision上线项目：EmoVision-PyQt（https://aistudio.baidu.com/projectdetail/8376569 ）**
#### **EmoVision上线项目：EmoVision-uniapp（https://aistudio.baidu.com/projectdetail/8661704 ）**
#### **GitHub仓库地址：EmoVision-Streamlit（https://github.com/GabePersson/EmoVision-Streamlit ）**
#### **GitHub仓库地址：EmoVision-PyQt（https://github.com/GabePersson/EmoVision-PyQt ）**
#### **GitHub仓库地址：EmoVision-uniapp（https://github.com/GabePersson/EmoVision-uniapp ）**

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=GabePersson/EmoVision&type=Date)](https://www.star-history.com/#GabePersson/EmoVision&Date)

## Acknowledgement
[ProcessPainter]https://github/com/nicolaus-huang/ProcessPainter

Thanks for above author's contribution.
