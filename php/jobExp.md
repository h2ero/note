工作中学到的一些东西
===========================
1. `serialize()`序列化数组／对象为字符串，方便在数据库中存储。
2. `union`查询时候用`order by` 需要将两个子查询括号，`()union () order by`
3. `session_id(),session_start()`如果`session_start()`在第一个则`session_id()`无效，并且`$_SESSION`如果存有字符串，将不再能存入多维数组。
4. js加载可以直接新建一`require_js.php` 然后根据功能分组判断加载。
5. 图片后缀等相关信息判断可以通过`getimagesize()`进行判断。 
