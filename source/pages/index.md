---
title: 读书笔记
date: 2016-09-18 14:20:54
---

*一些读书笔记和非常有趣的文章*

<style>
ol{
        counter-reset: li; 
        list-style: none; 
        *list-style: decimal; 
        font: 20px 'trebuchet MS', 'lucida sans';
        padding: 1;
        margin-bottom: 1em;
        text-shadow: 0 1px 0 rgba(255,255,255,.5);
        margin: 0 0 0 1em;
}

.rounded-list a{
    position: relative;
    display: block;
    padding: .4em .4em .4em 2em;
    *padding: .2em;
    margin: .2em 0;
    background: #ddd;
    color: #444;
    text-decoration: none;
    border-radius: .3em;
    transition: all .3s ease-out; 
}

.rounded-list a:hover{
    background: #eee;
}

.rounded-list a:hover:before{
    transform: rotate(360deg); 
}

.rounded-list a:before{
    content: counter(li);
    counter-increment: li;
    position: absolute; 
    left: -1.3em;
    top: 50%;
    margin-top: -1.3em;
    background: #87ceeb;
    height: 2em;
    width: 2em;
    line-height: 2em;
    border: .3em solid #fff;
    text-align: center;
    font-weight: bold;
    border-radius: 2em;
    transition: all .3s ease-out;
}

.circle-list li{
    padding: 2.5em;
    border-bottom: 1px dashed #ccc;
}

.circle-list h2{
    position: relative;
    margin: 0;
}

.circle-list p{
    margin: 0;
}

.circle-list h2:before{
    content: counter(li);
    counter-increment: li;
    position: absolute;    
    z-index: -1;
    left: -1.3em;
    top: -.8em;
    background: #f5f5f5;
    height: 1.5em;
    width: 1.5em;
    border: .1em solid rgba(0,0,0,.05);
    text-align: center;
    font: italic bold 1em/1.5em Georgia, Serif;
    color: #ccc;
    border-radius: 1.5em;
    transition: all .2s ease-out;    
}

.circle-list li:hover h2:before{
    background-color: #ffd797;
    border-color: rgba(0,0,0,.08);
    border-width: .2em;
    color: #444;
    transform: scale(1.5);
}

            /*rectangle list*/
        .rectangle-list a {
            position: relative;
            display: block;
            padding: 0.4em 0.4em 0.4em 0.8em;
            *padding: 0.4em;
            margin: 0.5em 0 0.5em 2em;
            background: #ddd;
            color: #444;
            text-decoration: none;
            /*transition动画效果*/
            -webkit-transition: all 0.3s ease-out;
            -moz-transition: all 0.3s ease-out;
            -ms-transition: all 0.3s ease-out;
            -o-transition: all 0.3s ease-out;
            transition: all 0.3s ease-out;
        }
        .rectangle-list a:hover {
            background: #eee;
        }
        
        .rectangle-list a::before {
            
            content: counter(li);
            counter-increment: li;
            
            position: absolute;
            left: -2.5em;
            top: 50%;
            margin-top: -1em;
            background: #fa8072;
            width: 2em;
            height: 2em;
            line-height: 2em;
            text-align: center;
            -webkit-transition: all 0.3s ease-out;
            -moz-transition: all 0.3s ease-out;
            -o-transition: all 0.3s ease-out;
            -ms-transition: all 0.3s ease-out;
            transition: all 0.3s ease-out;
        }
        .rectangle-list a::after {
            position: absolute;
            content:"";
            border: 0.5em solid transparent;
            left: -1em;
            top: 50%;
            margin-top: -0.5em;
            -webkit-transition: all 0.3s ease-out;
            -moz-transition: all 0.3s ease-out;
            -o-transition: all 0.3s ease-out;
            -ms-transition: all 0.3s ease-out;
            transition: all 0.3s ease-out;
        }
        .rectangle-list a:hover::after {
            left: -0.5em;
            border-left-color: #fa8072;
        }
</style>

## 容器的世界


<ol class="rounded-list">
<li><a href="/kubernetes/">Kubernetes指南</a></li>
<li><a href="/kubernetes-dev.html">Kubernetes开发环境指南</a></li>
<li><a href="/container/docker/">docker指南</a></li>
<li><a href="/container/cri-o.html">CRI-O</a></li>
<li><a href="/2016/02/26/Notes-about-serverless/">Serverless</a></li>
<li><a href="docker-internal.html">docker实现原理</a></li>
<li><a href="http://calcotestudios.com/ccco">容器编排系统对比</a></li>
<li><a href="https://leecalcote.github.io/ccco/overlay-underlay-betting-on-container-networking.html">容器网络方案对比</a></li>
<li><a href="http://dockerconrecap-leecalcote.rhcloud.com/#/">Docker 1.12</a></li>
<li><a href="/container/selinux/">SELinux</a></li>
</ol>

## 虚拟化

<ol class="rounded-list">
<li><a href="/virtualization/GPU/">GPU虚拟化</a></li>
<li><a href="/virtualization/SR-IOV/">SR-IOV</a></li>
<li><a href="http://awilliam.github.io/presentations/KVM-Forum-2016/">VFIO</a></li>
</ol>

## 分布式系统

<ol class="rounded-list">
<li><a href="gfs.html">gfs</a></li>
<li><a href="impala.html">impala</a></li>
<li><a href="kafka.html">kafka</a></li>
<li><a href="distributed-algorithms-in-nosql-databases.html">Distributed Algorithms in NoSQL Databases</a></li>
<li><a href="distributed-system-reading.html">分布式系统资源链接</a></li>
</ol>

## 编程语言

<ol class="rounded-list">
<li><a href="gdb.html">gdb</a></li>
<li><a href="/programing/go.html">Go语言技巧</a></li>
<li><a href="python.html">python</a></li>
<li><a href="java.html">java</a></li>
</ol>

## 其他

<ol class="rounded-list">
<li><a href="/2015/01/27/vagrant/">vagrant使用指南</a></li>
<li><a href="mapreduce-a-major-step-backwards.html">MapReduce: A major step backwards（MapReduce：一个巨大的倒退）</a></li>
<li><a href="design-pattern.html">design-pattern</a></li>
</ol>

