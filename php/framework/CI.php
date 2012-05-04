<?php
/*
 * 
 * 
 * CI删除缓存
 * 
 * 
 * 
 */
$uri = $this->config->item('base_url').
$this->config->item('index_page').
$this->uri->uri_string();

//得出cache文件的文件名
$cacheName = md5($uri);

$this->_deleteCache($cache_name);

//删除cache文件函数
function _deleteCache($cache_name)
{
	$path = $this->config->item('cache_path');
	$cache_path = ($path == '') ? BASEPATH.'cache/' : $path;
	$cache_path .= $cache_name;
	if(file_exists($cache_path)){
		touch($cache_path);
		unlink($cache_path);
	}else{
		return false;
	}
	echo $cache_path;
}