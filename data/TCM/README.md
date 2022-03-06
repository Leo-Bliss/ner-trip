# 文件夹说明

```
│  README.md
│  tree.txt
│  
├─extend : 根据词表匹配未标记的嵌套实体（嵌套实体只标注最长的），只有实体类别和实体位置
│      0.csv
│      ...
├─original : 词表匹配的标注结果
│      0.ann : 标注结果
│      0.txt : 对应的文本
│      ...
├─pkls
│      all_mark_dict.pkl
│      FJ.pkl : 方剂词表（处理出的词表信息源在raw_data和raw_data\extend中）
│      FY.pkl : 方药词表
│      MX.pkl : 脉象词表
│      SX.pkl : 舌象词表
│      ZF.pkl : 治法词表
│      ZH.pkl : 证候词表
│      ZZ.pkl : 症状词表
│      
├─process
│  ├─dev : 验证集,目前已经和test合并,即只有测试集和训练集
│  │      101.csv
│  │      91.csv
│  │      
│  ├─pkls
│  │      dev.pkl : 用于跑模型的验证集
│  │      entities_count.pkl : 该文件夹下的数据实体统计结果
│  │      fetures_dict.pkl : 处理出的包含各种特征的数据
│  │      lowfreq_words.pkl : 去除的低频词
│  │      test.pkl  : 用于跑模型的测试集
│  │      train.pkl : 用于跑模型的训练集
│  │      
│  ├─test : 测试集
│  │      106.csv
│  │      ...
│  └─train : 训练集
│          0.csv
│          ...
├─processor : 数据处理的过程中写的代码
│      count.py
│      count_test.py
│      csv_ann.py
│      mark.py
│      process_excel.py
│      rebuild_data.py
│      res_plot.py
│      tmp.txt
│      
├─process_csv : 数据处理过程中时没有之间生成ann文件，而是先保存成了csv
│      0.csv   : 和ann文件对应
│      
└─raw_data : 老师给的原始材料
    │  【aim】中医脾胃病学核对稿20201110.csv
    │  【aim】古今名家验案全析.csv
    │  中医术语同义词一行.csv
    │  中医治法-证候-疾病术语.csv
    │  中医脾胃病学核对稿20201110.txt
    │  方剂（id_名称_别名）.csv
    │  方药（id_名称_别名）.csv
    │  治法(id_名称).csv
    │  脾胃病古今名家验案全析上下位词.csv
    │  证候(id_名称).csv
    │  
    └─extend : 其他途径获取到的扩展材料
            发热和咳嗽疾病的转好电子病历.xlsx
            方剂.csv
            方药.csv
            症状.csv
            脉象.csv
            舌象.csv
            证侯.csv
```