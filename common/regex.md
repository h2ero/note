正则表达式   《精通正则表达式》
========

概念
-------
1. 正则(regex):
	+ 元字符+普通字符
2. 字符组(Character Class):
    + `[abc.?]`     .?等需要转义的字符可以以字符组方式匹配
    + 字符组都是匹配一个字符 
		>`g[.?]` 并不会匹配 g.?

3. 字符组元字符(Character-class Metacharacter):
    + `[^0-5a-z]`  匹配大小写`[Ss]qr`
    + 匹配HTML TAG `<H[1-5]>`
    + ^不包含
    + `[a|b]`和(a|b)不同,前者|只是一个字符,后者则是"或"
4. 单词分界(Word Boundaries)元字符序列(Metasequences):
    + `<\word word\>`
    + 匹配单词word开头的和word结尾的
    + \b单词分界 \bcat\b
5. 括号及反向引用(Parentheses and Backreferences):
	+ (abc)\1       \1开始引用 多个括号从左至右
   	+ php 使用引用需要转义，即 `preg_match('/(cat)\\1/',$str,$res)`
6. 环视(lookaround):
    环视和\b ^ $等一样只是匹配特定的位置。
    1. 肯定顺序环视(lookahead): 
		+ `(?=h2ero)love you`     从左至右
    2. 肯定逆序环视:
    	+ `(?<=h2ero)lover you`   从右至左

	    	>分隔123456789为123.456.789,可以是`preg_replace('/(?<=\d)(?=(\d\d\d)+$)/','.','123456789');`也可以是`preg_replace('/(?=\d)(?<=(\d\d\d)+$)/','.','123456789');`两个环视的先后顺序不重要。只要在相同位置匹配即可。

	3. 否定顺序环视:
		+ `(?!h2ero)love you`     从左至右
	4. 否定逆序环视:
		+ `(?<!h2ero)lover you`   从右至左

	
拾遗
-------
1. `^cat$`       以字符阅读 第一个c开头 第二个a 第三个t结尾 而不是单词cat
2. `^$`          匹配空行
3. `"[^"]*"`   匹配`[]`内的字符串

