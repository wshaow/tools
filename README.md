# Tools
## 图像局部放大分析工具

### 使用方法

#### 安装

python 版本 python3

安装需要的库

```
pip install -r requirment.txt
```

#### 运行

1、将需要对比的图形放在imgs文件下

2、原始图像文件名需要包含`_ROI`，现在是只有一张原始图像

3、选择原始图像中想比较的区域

4、选好后，按空格键会显示所有图像的所选区域的放大图，第一行为对应图像的放大图，第二列为原始图像的放大图。

5、如果要退出按回车键。

#### 参数设置

有一些可以选择的参数：

```python
LINE_COLOR = (0, 255, 0)  # 获取在原图上画的线的颜色
LINE_WIDTH = 2  # 在原图上线的宽度
SCALE = 2  # 对选取区域的放大倍数
ADD_BBOX = True  # 是否对要保存的图像增加边框
BBOX_WIDTH = 4   # 增加的边框的宽度
BBOX_COLOR = (255, 255, 255)  # 默认为白色
INTER_METHOD = cv.INTER_LINEAR  # 放大图像的差值方式，默认使用线性插值INTER_LINEAR， 双三次INTER_CUBIC, INTER_LANCZOS4, INTER_LINEAR
```

#### 最终结果

在result中保存了最后一次选择的局部放大图



