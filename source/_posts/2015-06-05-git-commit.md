---
layout: post
title: "git commit修改前一次提交的方法"
description: ""
category: Linux
tags: []
---

方法一：用–amend选项

```
#修改需要修改的地方。
git add .
git commit –amend
```

注：这种方式可以比较方便的保持原有的Change-Id，推荐使用。

方法二：先reset，再修改

这是可以完全控制上一次提交内容的方法。但在与Gerrit配合使用时，需特别注意保持同一个commit的多次提交的Change-Id是不变的。为了保持提交到Gerrit的Change不变，需要复制对应的Change-Id到commit msg的最后，可以到Gerrit上对应的Change去复制.

```
git reset HEAD^
#重新修改
git add .
git commit -m “MSG”
```

方法三：只是修改作者

如果email不对，会无法提交到Gerrit，所以这个命令也可能用到。

```
git commit --amend --author="AUTHOR <EMAIL>"
```

注：如果该email地址从未有过成功的提交，这个修改会不成功。在别的分支做一次成功提交之后，就可以修改了。

方法四：使用rebase

```
1. // 查看修改

git rebase -i master~1 //最后一次
git rebase -i master~5 //最后五次

2. // 显示结果如下，修改 pick 为 edit ，并 :wq 保存退出

pick 92b495b 2009-08-08: ×××××××

# Rebase 9ef2b1f..92b495b onto 9ef2b1f
#
# Commands:
#  pick = use commit
#  edit = use commit, but stop for amending //改上面的 pick 为 edit
#  squash = use commit, but meld into previous commit
#
# If you remove a line here THAT COMMIT WILL BE LOST.
# However, if you remove everything, the rebase will be aborted.
#


3. 命令行显示：

Rebasing (1/1)
You can amend the commit now, with

git commit --amend


4. 使用 git commit --amend 进行修改，完成后 :wq 退出

5. 使用 git rebase --continue 完成操作
```

转自http://blog.csdn.net/tangkegagalikaiwu/article/details/8542827
