<?php

$arr = array(1, 2, 0, 33, 5, 6);

var_dump($arr);

$count = count($arr);

for ($i = 1; $i < $count;$i ++ )
{
    for ($k = $i;  $k>0, $arr[$k] < $arr[$k - 1];  $k -- ) 
    {
        $swap    = $arr[$k];
        $arr[$k] = $arr[$k-1];
        $arr[$k-1] = $swap;
    }
}

var_dump($arr);
