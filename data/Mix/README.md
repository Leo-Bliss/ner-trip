
# 数据集说明

+ TCM: 0-775
+ Contest: 776-1775


```
total number of entity class: 7
{'ZH': 22899, 
'SX': 2376, 
'ZZ': 15312, 
'FY': 22345, 
'FJ': 2402,
 'MX': 1417, 
 'ZF': 2792}
```

+ process_csv: 词表匹配的目标实体,这里只有Contest中部分,TCM中未复制过来
+ original : ann由txt根据process_csv做的标注
+ extend: 未标注的嵌套实体
+ inputs: 输入算法要用的数据