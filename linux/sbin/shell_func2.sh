#!/usr/bin/env bash

echo $(uname);
num=1000;

uname()
{
    echo "test!";
    ((num++));
    return 100;
}
testvar()
{
    local num=10;
    ((num++));
    echo $num;
}

uname;
echo $?
echo $num;
testvar;
echo $num;
