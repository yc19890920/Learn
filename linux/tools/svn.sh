#!/usr/bin/env bash
# /usr/local/pyenv/versions/edm_web/bin/python mosaico_to_otheruser.py -t 1234 -u 2369

DIR="/home/python/Linux-WebVue"
PATCH_DIR="/home/python/patch/src_webvue"

while true; do
  case "$1" in
       -v|--version)
          version="$2"
          echo "version: $version"
          shift
          ;;
      -t|--type)
          type="$2"
          echo "type:   $type"
          shift
          ;;
      -m|--comment)
          comment="$2"
          echo "comment: $comment"
          shift
          ;;
      -h|--help)
          usage
          # 打印usage之后直接用exit退出程序
          exit
          ;;
      --)
        shift
        break
        ;;
      *)
        # echo "$1 is not option"
        break
  esac
  shift
done

set -- $(getopt -o v:t:m --long version:,type:,comment:,help -- "$@")

usage(){
  echo "
Usage:
  -v, --version  提交的版本，比如 2.2.7  对应svn就是2.2.7， 对应vue就是 release-2.2.7
  -t, --type    py or vue；更新svn py文件， 或者 svn vue以及py文件
  -m, --comment    提交git以及svn的说明
  -h, --help    display this help and exit

  example1: ./svn_update.sh -v 2.2.7 -t py -m bug说明
  example2: ./svn_update.sh --version 2.2.7 --type vue --comment bug说明
"
}

check_params(){
    if [ ! $version ]; then
        usage
        exit 1 ;
    fi

    if [ ! $version ]; then
        usage
    else
        cd $DIR
        ss=`git branch -a | grep -E "release-$version"`
        if [[ -z $ss ]]; then
            echo "没有此git版本：release-$version ..............."
            # usage
            exit 1;
        fi
    fi

    if [ ! $type ]; then
        usage
        exit 1 ;
    fi

    if [ $type = "py" ]; then
        echo "==============================py"
    elif [ $type = "vue" ]; then
        echo "==============================vue"
    else
        echo "==============================error type"
    fi

    if [ ! $comment ]; then
        usage
        exit 1 ;
    fi
}

update_vue(){
    ##############################################################
    # 更新vue
    cd $DIR
    echo "更新git"
    git pull origin release-${version}

    echo "删除dist目录"
    rm -rf $DIR/appfront/dist/

    echo "打包vue项目"
    cd $DIR/appfront
    cnpm run build

    git add -f dist/
}

update_py(){
    ##############################################################
    # 提取文件
    cd $DIR
    echo "更新git"
    git pull origin release-${version}

    rm -rf $DIR/tmp

    # 在源代码根目录，使用git status命令获取已修改文件的列表
    git status | grep -E "修改：|新文件：" | awk '{print $2}' > $DIR/update.txt
    git status | grep -E "重命名：" | awk '{print $4}' >> $DIR/update.txt

    # # 更新成svn需要的update.txt格式
    git status | grep -E "修改：|新文件：" | awk '{print $2" = $WEBVUE_PATH/"$2}' > $DIR/update2.txt
    git status | grep -E "重命名：" | awk '{print $4" = $WEBVUE_PATH/"$4}' >> $DIR/update2.txt

    # 字符串是否为空
    # -z	检测字符串长度是否为0，为0返回 true。	[ -z $a ] 返回 false。
    # -n	检测字符串长度是否为0，不为0返回 true。	[ -n "$a" ] 返回 true。
    ss=`git status | grep -E "修改：|新文件：|重命名："`
    if [[ -z $ss ]]; then
        # echo $?
        echo "没有需要更新提交的文件..............."
        cd $DIR
        git checkout master
        exit 1;
    fi

    cat $DIR/update.txt

    # 在当前目录下，创建tmp目录
    mkdir -p $DIR/tmp
    #cp $DIR/update.txt $DIR/tmp

    # 将已修改文件列表逐一复制到当前目录下的temp目录
    xargs -a $DIR/update.txt cp --parents -t $DIR/tmp

    # 更新成svn需要的update.txt格式
    echo 'y' | mv $DIR/update2.txt $DIR/alter.txt


    # /home/python/pyenv/versions/Linux-Opration/bin/python $DIR/build-update.py $DIR/update.txt > $DIR/tmp/update.txt
    ##############################################################
     echo "提交git；commit $comment"
     git commit -am "$comment"
     git push origin release-$version

     echo "提交svn；commit $comment"

     cd $PATCH_DIR
     version_dir=$PATCH_DIR/${version}
     if [[ ! -e ${version_dir} ]]; then
        mkdir -p ${version_dir}
        touch ${version_dir}/update.txt
     fi

     # echo "cat $DIR/alter.txt >> ${version_dir}/update.txt"
     echo "# $comment\n" >> ${version_dir}/update.txt
     cat $DIR/alter.txt >> ${version_dir}/update.txt
     echo "\n">> ${version_dir}/update.txt

     cp -rf  $DIR/tmp/*  /${version_dir}/

     echo "============提交svn文件"
     echo "手动输入svn密码： 123456"
     echo "手动输入svn密码： 123456"
     echo "手动输入svn密码： 123456"
     echo "手动输入svn密码： 123456"
     echo "手动输入svn密码： 123456"
     echo "手动输入svn密码： 123456"
     cd $PATCH_DIR
     svn add ${version}
     # svn commit -m "$comment"
     # echo "123456" | svn commit -m "$comment"

     echo "$version_dir"
     cd $version_dir

     svn status | awk '{$1=""; print $0}' | xargs -i svn add "{}"

     svn commit -m "$comment"
     # echo "123456" | svn commit -m "$comment"

     cd $DIR
     git checkout master
}

update_all(){
    update_vue;
    update_py;
}

update_git(){
    cd $DIR
    git checkout release-${version}
    git pull origin release-${version}
}

check_params;

case $type in
    "vue")
        update_git;
        update_all;
        ;;
    "py")
        update_git;
        update_py;
        ;;
    *)
        echo "==============================22222222222222"
        usage
        ;;
esac