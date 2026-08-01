

# Compiling-Principle-Work

## Authored by Aczy156 (Software 1805 Chen Ranfei)

## Structure
### data
* Grammer_for_ll1_and_RD.txt, contains the test grammars used for Experiment 2 (Predictive Parsing) and Experiment 3 (Recursive Descent Parsing).
* Grammer_for_OF.txt, contains the test grammars used for Experiment 4 (Operator Precedence Parsing).
### MultiAnalysis
* Top-Down
    - [Experiment 2] LL1_analysis.py covers the complete process of LL(1) parsing.
    - [Experiment 3] RecursiveDescent_analysis.py covers the complete process of recursive descent parsing.
* Bottom-Up
    - [Experiment 4] OperatorFirst_analysis.py covers the complete analysis process for operator precedence grammars.
    - - [ ] LR(1) grammar, to be completed
    

### tools
[Used repeatedly across various grammars in MultiAnalysis, so they were extracted as submodules and placed here for modular management.]
* Draw_Grammer.py, uses Python's prettytable library specifically for grammar visualization.
* Eliminate_Left_Recursion.py, uses the left-recursion elimination algorithm to specifically handle left recursion issues for top-down grammars (e.g., predictive parsing in Experiment 2 and recursive descent parsing in Experiment 3).
* Extract_Common_Factors.py, uses the Longest Common Prefix (LCP) algorithm to extract and eliminate common factors.
