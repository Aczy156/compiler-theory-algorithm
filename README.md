# Compiling-Principle-Work

## Authored by Aczy156(软件1805陈冉飞)

## Structure
### data
* Grammer_for_ll1_and_RD.txt，是存放用于实验二预测分析法和实验三递归下降分析文法的测试文法
* Grammer_for_OF.txt，是存放用于实验四算符优先文法的测试文法。
### MultiAnalysis
* 自上而下
    - [实验二]LL1_analysis.py是LL1分析法的整体过程。
    - [实验三]RecursiveDescent_analysis.py是递归下降分析的整体过程。
* 自下而上
    - [实验四]OperatorFirst_analysis.py是算符优先文法的整体分析过程。
    - - [ ] LR(1)文法，待完成
    

### tools
[在MultiAnalysis中的各种文法中多次使用，所以提取出来子模块，放进工具中来模块化管理]
* Draw_Grammer.py，利用python中prettytable来专门做文法的可视化。
* Eliminate_Left_Recursion.py，利用消除左递归算法来专门处理对于自上而下的文法(例如实验二中的预测分析文法和实验三的递归下降文法)的左递归的问题。
* Extract_Common_Factors.py，利用LCP(最长公共前缀)来提取公因子并消除。