<p>@Time        :    2021/4/1 0001 13:56</p>
<p>@Author      :    tb_youth</p>
<p>@FileName    :    README.md</p>
<p>@Description :    NER Project Description</p>
<p>@Blog        :    https://blog.csdn.net/tb_youth</p>

# README

------

<p>@Daily English</p>

> You can overcome anything,if and only if you love something enough.

> 只要并只有你足够热爱一件事情，你可以克服任何困难。
## About
+ 毕设题目：**中医电子病历实体识别模型研究**
+ 作者邮箱：tbyouth11@gmail.com

## How to use it?

 1. 原仓库：```get clone https://gitee.com/tbyouth/ner.git```现迁移到：https://gitee.com/tbyouth/ner-trip.git
 2. 参考`requirements.txt`配置项目所需环境（**注意**tensorflow版本：linux下和windows下的不一样）
 3. 在`data`文件夹下创建一个你的数据集文件夹，你需要把你的数据集中每一个文本处理成一对txt,ann文件，txt存储文本，ann存储标注信息...
 4. 在`NER\config\setting.py`下修改配置
 5. 在`NER\preprocess\data_prepare.py`中按步骤执行相关操作
 6. ...
 
 

## Target data set for NER
+ 瑞金医院竞赛数据集
+ 古今名家验案全析.csv
+ 中医脾胃病学核对稿20201110.csv
### Information for data set
> 共计1776条记录
1. 竞赛数据集语料为：中医药物说明书（1000条）
2. 古今名家验案全析.csv数据内容大致分布（484条）：

* * *

|id|症状|症状|证候|病因|自诉|null|null|症状...|
|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| | | | | | | | | |

* * *



3. 中医脾胃病学核对稿20201110.csv数据内容大致分布（292条）：

* * *

|id | 疾病（诊断，症状） | 第一项的别名 | 证候 | 临床表现 | 理法概要 | 治法 | 药方|
|:-----:|:----:|:----:|:---:|:----:|:---:|:---:|:---:|
| | | | | | | | |

* * *

## Target entity class for NER 
可选类别：症状，脉类，脉象，疾病，病位，病名，病因，症状，治法，方剂，方药，检查，
舌体，舌苔，舌象，器官，身体部位...

本数据集确定的NER目标实体如下：
* * *

|实体类别|类别标签|举例| 
|:---:|:---:|:---:|
方药|FY|桂枝
方剂|FJ|大承气汤
证候|ZH|中焦虚寒证
治法|ZF|清热止痢法
脉象|MX|浮紧浮缓
舌象|SX|唇舌淡红
症状|ZZ|嗳气不适

* * *

## Other

### features for entity
#### 会存在实体嵌套现象
比如：桂枝人参汤，这是一个方剂实体，嵌套了两个方药实体:桂枝，人参；
#### 解决方案
优先标注更长的，其他的可以构成扩充语料？
训练时可以作为扩充语料。
但是预测就会存在问题！！！
一个句子输入只能输出一个序列标注。
嵌套实体NER不是很好解决。
所以目前目标：识别出最长实体就好了，或者嵌套的实体识别出来了也不错。

#### 中医实体较长
比如方剂实体：桂枝去芍加麻附细辛汤；证候实体：虫毒湿热结肤证,小儿痰热蒙闭心窍证；...
#### 不连续，并列实体
治法宜益气健脾、升阳举陷为主，根据食积、痰饮、湿热、瘀血之不同，分别佐以消食、化饮、化湿、通络之法。
治法实体：益气健脾，升阳举陷，消食，化饮，化湿，通络
对其治法应“寓补于消，标本兼顾”
治法实体：寓补于消，标本兼顾

#### 表述多样性，异形同义
有些侯证“xxx证”有时被表述为“xxx”或者“证属xxx”
如：气滞血瘀证 = 气滞血瘀，中气下陷证 = 证属元气虚衰，中气下陷。（并列实体：证属元气虚衰，证属中气下陷）
瘀阻之证：瘀阻证

### 系统展示

[![gInzJU.png](https://z3.ax1x.com/2021/05/19/gInzJU.png)](https://imgtu.com/i/gInzJU)
[![gInxiT.png](https://z3.ax1x.com/2021/05/19/gInxiT.png)](https://imgtu.com/i/gInxiT)
[![gInXd0.png](https://z3.ax1x.com/2021/05/19/gInXd0.png)](https://imgtu.com/i/gInXd0)
[![gInOZq.png](https://z3.ax1x.com/2021/05/19/gInOZq.png)](https://imgtu.com/i/gInOZq)
[![gInqLn.png](https://z3.ax1x.com/2021/05/19/gInqLn.png)](https://imgtu.com/i/gInqLn)




