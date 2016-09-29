---
title: 资源列表
date: 2016-09-18 14:20:54
---

# 资源列表

<style>
ol{
        counter-reset: li; /* 创建一个计数器 */
        list-style: none; /* 清除列表默认的编码*/
        *list-style: decimal; /* 让IE6/7具有默认的编码 */
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
<li><a href="/2015/02/12/docker-intro/">docker指南</a></li>
<li><a href="docker-internal.html">docker实现原理</a></li>
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
<li><a href="../go-tips/">Go语言技巧</a></li>
<li><a href="python.html">python</a></li>
<li><a href="java.html">java</a></li>
</ol>

## 其他

<ol class="rounded-list">
<li><a href="/2015/01/27/vagrant/">vagrant使用指南</a></li>
<li><a href="pig.html">pig</a></li>
<li><a href="leveldb.html">leveldb</a></li>
<li><a href="concurrency.html">concurrency</a></li>
<li><a href="megastore.html">megastore</a></li>
<li><a href="mapreduce-a-major-step-backwards.html">MapReduce: A major step backwards（MapReduce：一个巨大的倒退）</a></li>
<li><a href="design-pattern.html">design-pattern</a></li>
<li><a href="probabilistic-data-structures-for-web-analytics-and-data-mining.html">Probabilistic Data Structures for Web Analytics and Data Mining</a></li>
<li><a href="large-scale-data-and-computation-chanllenges-and-opportunities.html">Large-Scale Data and Computation: Challenges and Opportunities</a></li>
<li><a href="gwp.html">gwp</a></li>
<li><a href="pic.html">position independent code</a></li>
<li><a href="backblaze-storage-pod.html">backblaze-storage-pod</a></li>
<li><a href="jni.html">jni</a></li>
<li><a href="screen.html">screen tips</a></li>
<li><a href="pnuts.html">pnuts</a></li>
<li><a href="data-mining.html">data-mining</a></li>
<li><a href="systems-software-research-is-irrelevant.html">Systems Software Research is Irrelevant</a></li>
<li><a href="writing-software-is-like-writing.html">Writing Software is Like &hellip; Writing</a></li>
<li><a href="opentsdb.html">opentsdb</a></li>
<li><a href="system-programming-at-twitter.html">Systems Programming at Twitter</a></li>
<li><a href="a-word-on-scalability.html">A Word on Scalability</a></li>
<li><a href="programmer-dilemma.html">Programmer’s dilemma</a></li>
<li><a href="percolator.html">percolator</a></li>
<li><a href="application-resilience-in-a-service-oriented-architecture.html">Application Resilience in a Service-oriented Architecture</a></li>
<li><a href="build-system.html">build-system</a></li>
<li><a href="folly.html">folly</a></li>
<li><a href="ace.html">ace</a></li>
<li><a href="lzf.html">lzf</a></li>
<li><a href="how-to-beat-the-cap-theorem.html">How to beat the CAP theorem</a></li>
<li><a href="linux.html">linux</a></li>
<li><a href="the-anatomy-of-the-google-architecture.html">The Anatomy Of The Google Architecture</a></li>
<li><a href="dremel.html">dremel</a></li>
<li><a href="python-copy.html">python copy</a></li>
<li><a href="the-tyranny-of-the-clock.html">The Tyranny of the Clock</a></li>
<li><a href="unveil-google-app-engine.html">探索Google App Engine背后的奥秘</a></li>
<li><a href="mapreduce-and-parellel-dbmss-friends-or-foes.html">MapReduce and Parallel DBMSs: Friends or Foes?（MapReduce和并行数据库，朋友还是敌人？）</a></li>
<li><a href="clojure.html">clojure</a></li>
<li><a href="memcached.html">memcached</a></li>
<li><a href="couchbase.html">couchbase</a></li>
<li><a href="dynamodb.html">dynamodb</a></li>
<li><a href="redis.html">redis</a></li>
<li><a href="storage-system-reading.html">storage-system-reading</a></li>
<li><a href="snappy.html">snappy</a></li>
<li><a href="building-scalable-highly-concurrent-and-fault-tolerant-systems.html">Building Scalable, Highly Concurrent &amp; Fault-Tolerant Systems: Lessons Learned</a></li>
<li><a href="building-software-systems-at-google-and-lessons-learned.html">Building Software Systems at Google and Lessons Learned</a></li>
<li><a href="data-structures-and-algorithms-for-big-databases.html">Data Structures and Algorithms for Big Databases</a></li>
<li><a href="jvm.html">jvm</a></li>
<li><a href="cpython-signal.html">cpython-signal</a></li>
<li><a href="tcmalloc.html">tcmalloc</a></li>
<li><a href="recommender-system.html">recommender-system</a></li>
<li><a href="the-secret-to-10-million-concurrent-connections.html">The Secret To 10 Million Concurrent Connections -The Kernel Is The Problem, Not The Solution</a></li>
<li><a href="gizzard.html">gizzard</a></li>
<li><a href="gperftools.html">gperftools</a></li>
<li><a href="gcc-asm.html">gcc-asm</a></li>
<li><a href="azkaban.html">azkaban</a></li>
<li><a href="design-reading.html">design-reading</a></li>
<li><a href="memory-barrier.html">memory-barrier</a></li>
<li><a href="consistency.html">storage_diary</a></li>
<li><a href="rocksdb.html">rocksdb</a></li>
<li><a href="f1.html">f1</a></li>
<li><a href="oprofile.html">oprofile</a></li>
<li><a href="aosa.html">The Architecture of Open Source Applications</a></li>
<li><a href="thrift.html">thrift</a></li>
<li><a href="dbms.html">dbms</a></li>
<li><a href="git.html">git</a></li>
<li><a href="apache-hadoop-goes-realtime-at-facebook.html">Apache Hadoop Goes Realtime at Facebook</a></li>
<li><a href="zookeeper.html">zookeeper</a></li>
<li><a href="ssd-and-distributed-data-systems.html">SSDs and Distributed Data Systems</a></li>
<li><a href="on-working-remotely.html">On Working Remotely</a></li>
<li><a href="mysql.html">mysql</a></li>
<li><a href="coroutine.html">coroutine</a></li>
<li><a href="PythonPaste.html">paste.deploy</a></li>
<li><a href="pic-code.html">pic-code</a></li>
<li><a href="case-study-gfs-evolution-on-fast-forward.html">Case Study GFS: Evolution on Fast-forward</a></li>
<li><a href="encoding.html">encoding</a></li>
<li><a href="hbase.html">hbase</a></li>
<li><a href="mapreduce.html">mapreduce</a></li>
<li><a href="lock.html">lock</a></li>
<li><a href="oozie.html">oozie</a></li>
<li><a href="muduo.html">muduo</a></li>
<li><a href="apue.html">apue</a></li>
<li><a href="unp.html">unp</a></li>
<li><a href="dapper.html">dapper</a></li>
<li><a href="nmstl.html">nmstl</a></li>
<li><a href="web-misc.html">web-misc</a></li>
<li><a href="realtime-big-data-analytics-emerging-architecture.html">Real-Time Big Data Analytics: Emerging Architecture</a></li>
<li><a href="haproxy.html">haproxy</a></li>
<li><a href="ssd-gc-and-trim.html">固态硬盘技术解析之垃圾回收和TRIM指令</a></li>
<li><a href="you-can-not-sacrifice-partition-tolerance.html">You Can’t Sacrifice Partition Tolerance</a></li>
<li><a href="bigtable.html">bigtable</a></li>
<li><a href="mapreduce-a-minor-step-forward.html">MapReduce: A Minor Step Forward</a></li>
<li><a href="maven.html">maven</a></li>
<li><a href="kylin.html">kylin</a></li>
<li><a href="mapreduce-a-flexible-data-processing-tool.html">MapReduce: A Flexible Data Processing Tool（MapRedcue: 一个灵活的数据库处理工具）</a></li>
<li><a href="swig.html">swig</a></li>
<li><a href="spark.html">spark</a></li>
<li><a href="nas_san.html">nas</a></li>
<li><a href="voldemort.html">voldemort</a></li>
<li><a href="scheme.html">scheme</a></li>
<li><a href="hive.html">hive</a></li>
<li><a href="sysperf.html">sysperf</a></li>
<li><a href="computational-advertising.html">computational-advertising</a></li>
<li><a href="chubby.html">chubby</a></li>
<li><a href="tenzing.html">tenzing</a></li>
<li><a href="the-skinny-on-raid.html">The skinny on RAID </a></li>
<li><a href="nosql-back-to-the-feature-or-yet-another-db-feature.html">NoSQL - Back to the Future or Yet Another DB Feature</a></li>
<li><a href="algorithm.html">algorithm</a></li>
<li><a href="spanner.html">spanner</a></li>
<li><a href="a-comparison-of-approaches-to-large-scale-data-analysis.html">A Comparison of Approaches to Large-Scale Data Analysis</a></li>
<li><a href="netty.html">netty</a></li>
<li><a href="apache.html">apache</a></li>
<li><a href="hadoop.html">hadoop</a></li>
<li><a href="scala.html">scala</a></li>
<li><a href="eclipse.html">eclipse</a></li>
<li><a href="streambase.html">streambase</a></li>
<li><a href="google-cluster-computing-faculty-traning-workshop.html">Google Cluster Computing Faculty Training Workshop</a></li>
<li><a href="tail-at-scale.html">The Tail at Scale</a></li>
<li><a href="encode.html">encode</a></li>
<li><a href="interview-problem.html">interview-problem</a></li>
<li><a href="cpu.html">cpu</a></li>
<li><a href="license.html">license</a></li>
<li><a href="systemtap.html">systemtap</a></li>
<li><a href="how-to-read-a-paper.html">How to Read a Paper</a></li>
<li><a href="dynamo.html">Dynamo: Amazon’s Highly Available Key-value Store</a></li>
<li><a href="ssd.html">ssd</a></li>
<li><a href="simd.html">simd</a></li>
<li><a href="prog-lang.html">prog-lang</a></li>
<li><a href="mac.html">mac</a></li>
<li><a href="mapred.html">mapred</a></li>
<li><a href="ubuntu.html">ubuntu</a></li>
<li><a href="beating-the-cap-theorem-checklist.html">Beating the CAP Theorem Checklist</a></li>
<li><a href="effective-scala.html">Effective Scala</a></li>
<li><a href="memory.html">memory</a></li>
<li><a href="mapreduce-online.html">MapReduce Online</a></li>
<li><a href="cpp.html">cpp</a></li>
<li><a href="mapreduce-versus-parellel-dbms.html">MapReduce Versus Parallel DBMS</a></li>
<li><a href="perf.html">perf</a></li>
<li><a href="topcoder.html">topcoder</a></li>
<li><a href="designs-lessons-and-advice-from-building-large-distributed-systems.html">Designs, Lessons and Advice from Building Large Distributed Systems</a></li>
<li><a href="cassandra.html">cassandra</a></li>
<li><a href="finagle.html">finagle</a></li>
<li><a href="suffering-oriented-programming.html">Suffering-oriented programming</a></li>
<li><a href="hpserver.html">hpserver</a></li>
<li><a href="mongodb.html">mongodb</a></li>
<li><a href="networking-namespace.html">net-ns</a></li>
<li><a href="libev.html">libev</a></li>
<li><a href="your-server-as-a-function.html">Your Server as a Function</a></li>
<li><a href="hdfs.html">hdfs</a></li>
<li><a href="akka.html">akka</a></li>
<li><a href="solid-state-revolution-in-depth-on-how-ssd-really-work.html">Solid-state revolution: in-depth on how SSDs really work</a></li>
<li><a href="clr-interview-problem.html">clr-interview-problem</a></li>
<li><a href="deconstructing-recommender-systems.html">Deconstructing Recommender Systems</a></li>
<li><a href="web-search-for-a-planet.html">Web Search for a Planet</a></li>
<li><a href="a-tour-inside-cloudflare-latest-generation-servers.html">A Tour Inside CloudFlare's Latest Generation Servers</a></li>
<li><a href="druid.html">druid</a></li>
<li><a href="in-stream-big-data-processing.html">In-Stream Big Data Processing</a></li>
<li><a href="zeromq.html">zeromq</a></li>
<li><a href="busting-4-modern-hardware-myths-are-memory-hdds-and-ssds-really-random-access.html">Busting 4 Modern Hardware Myths - Are Memory, HDDs, And SSDs Really Random Access?</a></li>
<li><a href="mapreduce-a-major-step-backwards-ii.html">MapReduce: A major step backwards（MapReduce：一个巨大的倒退）- FeedBack</a></li>
<li><a href="hackers-and-painters.html">黑客与画家</a></li>
<li><a href="cracking-the-coding-interview.html">Cracking The Coding Interview</a></li>
<li><a href="pregel.html">pregel</a></li>
<li><a href="lessons-learned-while-building-infrastructure-software-at-google.html">Lessons Learned While Building Infrastructure Software at Google</a></li>
</ol>