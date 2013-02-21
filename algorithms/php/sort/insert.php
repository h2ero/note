<?php

/* ------------------------------------------
    Properties:
    Stable
    O(1) extra space
    O(n^2) comparisons and swaps
    Adaptive: O(n) time when nearly sorted
    Very low overhead

    -----------------------------------------
    Although it is one of the elementary sorting algorithms with O(n2) worst-case time, insertion sort is the algorithm of choice either when the data is nearly sorted (because it is adaptive) or when the problem size is small (because it has low overhead).

    For these reasons, and because it is also stable, insertion sort is often used as the recursive base case (when the problem size is small) for higher overhead divide-and-conquer sorting algorithms, such as merge sort or quick sort. 
  --------------------------------------------*/

$arr = array(1, 2, 0, 33, 5, 6);

var_dump($arr);

$count = count($arr);

for ($i = 1; $i < $count;$i ++ )
{
    for ($k = $i; $k > 0, $arr[$k] < $arr[$k - 1]; $k-- ) 
    {
        $temp      = $arr[$k];
        $arr[$k]   = $arr[$k-1];
        $arr[$k-1] = $temp;
    }
}
var_dump($arr);
