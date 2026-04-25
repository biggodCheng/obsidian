# 撕拉片网站
## 飞书模板：
https://my.feishu.cn/docx/BhQedH8JVoAaJ9xRodCcRWbunCc?previous_navigation_time=1777107959304

**StarPolaroid – MVP Product Requirements Document**

**1. 基本信息**

|   |   |
|---|---|
|项|内容|
|**网站名**|**StarPolaroid**|
|**Slogan**|_Turn any selfie into a celebrity‑style Polaroid in 30 seconds_|
|**一句话说明解决的问题**|用 1/100 的价格、30 秒钟时间，让普通用户获得“明星同款”撕拉片照片，可下载/分享|
|**idea来源**|**背景：**刷小红薯的时候发现最近很多明星网红开始show自己的撕拉片，普通人也开始去海马体拍同款，或者自己在家复刻。https://www.xiaohongshu.com/explore/68450136000000002202f828?app_platform=ios&app_version=8.90&share_from_user_hidden=true&xsec_source=app_share&type=video&xsec_token=CBJNR8TxuFhoFIxSAmNYAB0qUyAoqgGM9wPX1u92FKvMM=&author_share=1&xhsshare=WeixinSession&shareRedId=ODs3MEk2Sks2NzUyOTgwNjY7OTc1Oko9&apptime=1751703198&share_id=ed68b63a8aec44b9a9188ae4004fc4e1  <br>  <br>**痛点**：1、拍一张400块；2、一次性出结果，拍不好就废了；<br><br>**解决方案的亮点：**更便宜、更能出片（直接上传自己喜欢的照片）|

**2. 目标用户**

|   |   |
|---|---|
|**维度**|描述|
|**年龄**|18–35 岁女性为主|
|**兴趣**|自拍、时尚潮流、追星、TikTok/小红书活跃|
|**动机**|获得明星棚拍质感照片，用于头像/社媒/打印|

**3. 竞品 & 机会点**

|   |   |   |   |
|---|---|---|---|
|竞品|模式|痛点|机会|
|VSCO / Tezza|滤镜 App|仅调色，无法直接去背景，难复现明星影棚风撕拉片|**我们一键生成 + 白框成品**|
|PhotoRoom|抠图换背景|无特定风格|**垂直明星同款**|
|线下拍立得棚拍|¥400/张|价格高、需预约|**线上 \$2.99 即时获得**|

**海外切入词**：celebrity polaroid generator / AI polaroid maker

**4. 价值主张**

1. **极速**：30 s 生成；免费预览。

2. **低价**：HD 下载 \$2.99 (< 线下 \$50)。

3. **专业**：正方画幅、白框、明星棚拍灯光。

4. **零门槛**：无需注册即可体验。

**5. 功能列表（MVP）**

|   |   |
|---|---|
|**模块**|**说明**|
|上传|JPG/PNG ≤10 MB，裁 4:5 或 1:1|
|AI 生成|Replicate/Fooocus 输出 1600×1600 无框|
|前端后处理（待确定）|Canvas 加 10 % 白框(底 13 %)、纸纹、颗粒|
|预览 & 水印|800 px 预览 + 斜水印|
|付费下载|Stripe Checkout \$2.99 HD 无水印|
|Gallery|Cover‑flow 滚动，hover 前后对比|
|SEO 页|/about /faq /terms /privacy|

**网站风格**：文艺、小清新、复古

**6. 收费策略**

|   |   |   |
|---|---|---|
|阶段|价格|说明|
|MVP|\$2.99/张|免费预览|
|迭代1|订阅 $19.99/月|不限次数|

**7. 运营 / 营销**

按着解决方案的亮点进行生成内容

• SEO 关键词表：celebrity polaroid generator, AI polaroid photo, vintage instant film…

• UGC Gallery opt‑in 送 1 credit。

• TikTok 美妆博主联动 20 人。

• Referral：邀请即送 1 credit。

• Ins/小红书 发一些网站生成的图片

**8. 技术方案（待确定）**

|   |   |   |
|---|---|---|
|层|栈|说明|
|前端|Next.js + Tailwind|单页功能 + SEO|
|文件|Cloudinary unsigned|直传浏览器|
|AI|Replicate Fooocus|1600 px PNG|
|后端|Node/Express (tRPC)|签名/生成/轮询|
|支付|Stripe Checkout|webhook 发 HD|
|CDN|Cloudflare R2 + Edge|Canvas 白框|

**9. 原型草图（结构）**

![](file:///C:\Users\87044\AppData\Local\Temp\ksohtml9692\wps1.jpg) 

想要的效果：

|   |   |
|---|---|
|![](file:///C:\Users\87044\AppData\Local\Temp\ksohtml9692\wps2.jpg) <br><br>_用户上传的照片_|![](file:///C:\Users\87044\AppData\Local\Temp\ksohtml9692\wps3.jpg) <br><br>_生成的类似风格的照片_|

|   |
|---|
|Plain Text  <br>[ HERO ]  <br> logo · slogan  <br> Upload Photo [btn]  <br> small: Previews free – HD $2.99  <br>  <br>[ Dropzone 480×600 ]  <br>  <br>[ Progress ]  <br>[ Preview 360×450 ]  Download HD – $2.99  /  Regenerate  <br>  <br>[ Gallery cover‑flow ]  <br>  <br>[ Footer ] About \| Contact \| Terms \| Privacy|

**10. 里程碑**

|   |   |
|---|---|
|周次|任务|
|W1|设计稿\&API 规范|
|W2|前端页面 + 上传|
|W3|AI 接口 + Stripe|
|W4|Gallery + SEO|
|W5|上线 & 首轮营销|

|   |
|---|
|**StarPolaroid – Upload • Preview • Get Your Celebrity Polaroid**|