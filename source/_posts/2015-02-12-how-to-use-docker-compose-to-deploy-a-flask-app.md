---
layout: post
title: "How to use docker compose to deploy a flask app"
description: ""
category: Docker
tags: [Docker]
---

The flask app is very simple, you have an index page where your can write and read comments.

## To start

So what we need ?

In my case a [Digital Ocean](https://www.digitalocean.com/?refcode=16e2312f412e "Digital Ocean") droplet (I'm using Fedora 21).

So, first of all we connect to our vm with ssh.

<pre class="code literal-block">
<span class="nv">$ </span>ssh root@yourvmip
</pre>

Now that we are inside we need to install git, Docker and docker-compose.

<pre class="code literal-block">
<span class="nv">$ </span>yum -y install git docker python-pip
<span class="nv">$ </span>pip install docker-compose<span class="o">==</span>1.1.0-rc2
<span class="nv">$ </span>systemctl start docker
<span class="nv">$ </span>systemctl <span class="nb">enable </span>docker
</pre>

That's all we need to play with Docker.

This is our directory tree of our project, quietly standard as you can see.

<pre class="code literal-block">
yourappdir/
    - nginx/
        - static/
            - put your static file here
        - sites-enabled/
            - app
        - Dockerfile
    - templates/
        - index.html
    - .gitignore
    - app.py
    - build.yml
    - Dockerfile
    - README
    - requirements.txt
</pre>

So let's start to analyze every part, app, nginx, Dockerfiles and build.yml.

The remaining files, .gitignore, README and requirements.txt are pretty standard and I think there's not to much to say.

[Here](https://github.com/barrachri/flask_docker "flask_docker Repository") you can find the repo of this project.

## App

If you don't know [Flask](http://flask.pocoo.org/ "Flask") it's the right time to spend some hours to learn it, simple and powerful !

That's our app, we have some imports, one line config, our models and views.

<pre class="code literal-block">
<span class="c">\## yourdirapp/app.py ##</span><span class="c">\## import ##</span>
<span class="kn">import</span> <span class="nn">datetime</span>
<span class="kn">from</span> <span class="nn">flask</span><span class="kn">import</span> <span class="n">Flask</span><span class="p">,</span> <span class="n">request</span><span class="p">,</span> <span class="n">render_template</span><span class="p">,</span> <span class="n">g</span>
<span class="kn">from</span> <span class="nn">peewee</span> <span class="kn">import</span> <span class="n">PostgresqlDatabase</span><span class="p">,</span><span class="n">Model</span><span class="p">,</span><span class="n">CharField</span><span class="p">,</span> <span class="n">TextField</span><span class="p">,</span> <span class="n">DateTimeField</span><span class="p">,</span> <span class="n">OperationalError</span><span class="p">,</span> <span class="n">ProgrammingError</span>

<span class="c">\## config ##</span>
<span class="n">DEBUG</span> <span class="o">=</span> <span class="bp">False</span>

<span class="c">\## models ##</span>
<span class="n">user</span> <span class="o">=</span> <span class="s">'postgres'</span>
<span class="n">host</span> <span class="o">=</span> <span class="s">'postgres'</span>
<span class="n">database</span> <span class="o">=</span> <span class="s">'postgres'</span>
<span class="n">psql_db</span> <span class="o">=</span> <span class="n">PostgresqlDatabase</span><span class="p">(</span><span class="n">database</span><span class="p">,</span> <span class="n">user</span><span class="o">=</span><span class="n">user</span><span class="p">,</span> <span class="n">host</span><span class="o">=</span><span class="n">host</span><span class="p">)</span>

<span class="k">class</span> <span class="nc">Comment</span><span class="p">(</span><span class="n">Model</span><span class="p">):</span>
    <span class="n">title</span> <span class="o">=</span> <span class="n">CharField</span><span class="p">()</span>
    <span class="n">body</span> <span class="o">=</span> <span class="n">TextField</span><span class="p">()</span>
    <span class="n">date</span> <span class="o">=</span> <span class="n">DateTimeField</span><span class="p">()</span>
    <span class="n">author</span> <span class="o">=</span> <span class="n">CharField</span><span class="p">()</span>
    <span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
        <span class="n">database</span> <span class="o">=</span> <span class="n">psql_db</span>

<span class="k">try</span><span class="p">:</span>
    <span class="n">Comment</span><span class="o">.</span><span class="n">create_table</span><span class="p">()</span>
<span class="k">except</span> <span class="p">(</span><span class="n">OperationalError</span><span class="p">,</span> <span class="n">ProgrammingError</span><span class="p">):</span>
    <span class="k">print</span><span class="p">(</span><span class="s">"Comment table already exists!"</span><span class="p">)</span>

<span class="c">\## views ##</span>
<span class="n">app</span> <span class="o">=</span> <span class="n">Flask</span><span class="p">(</span><span class="n">__name__</span><span class="p">)</span>
<span class="n">app</span><span class="o">.</span><span class="n">config</span><span class="o">.</span><span class="n">from_object</span><span class="p">(</span><span class="n">__name__</span><span class="p">)</span>

<span class="nd">@app.before_request</span>
<span class="k">def</span> <span class="nf">before_request</span><span class="p">():</span>
    <span class="n">g</span><span class="o">.</span><span class="n">db</span> <span class="o">=</span> <span class="n">psql_db</span>
    <span class="n">g</span><span class="o">.</span><span class="n">db</span><span class="o">.</span><span class="n">connect</span><span class="p">()</span>

<span class="nd">@app.after_request</span>
<span class="k">def</span> <span class="nf">after_request</span><span class="p">(</span><span class="n">response</span><span class="p">):</span>
    <span class="n">g</span><span class="o">.</span><span class="n">db</span><span class="o">.</span><span class="n">close</span><span class="p">()</span>
    <span class="k">return</span> <span class="n">response</span>

<span class="nd">@app.route</span><span class="p">(</span><span class="s">'/'</span><span class="p">,</span> <span class="n">methods</span><span class="o">=</span><span class="p">[</span><span class="s">'GET'</span><span class="p">,</span><span class="s">'POST'</span><span class="p">])</span>
<span class="k">def</span> <span class="nf">index</span><span class="p">():</span>
    <span class="k">if</span> <span class="n">request</span><span class="o">.</span><span class="n">method</span> <span class="o">==</span> <span class="s">'POST'</span><span class="p">:</span>
        <span class="n">title</span> <span class="o">=</span> <span class="n">request</span><span class="o">.</span><span class="n">form</span><span class="p">[</span><span class="s">'title'</span><span class="p">]</span>
        <span class="n">author</span> <span class="o">=</span> <span class="n">request</span><span class="o">.</span><span class="n">form</span><span class="p">[</span><span class="s">'author'</span><span class="p">]</span>
        <span class="n">body</span> <span class="o">=</span> <span class="n">request</span><span class="o">.</span><span class="n">form</span><span class="p">[</span><span class="s">'text'</span><span class="p">]</span>
        <span class="n">comment</span> <span class="o">=</span> <span class="n">Comment</span><span class="o">.</span><span class="n">create</span><span class="p">(</span>
            <span class="n">title</span><span class="o">=</span><span class="n">title</span><span class="p">,</span>
            <span class="n">body</span><span class="o">=</span><span class="n">body</span><span class="p">,</span>
            <span class="n">author</span><span class="o">=</span><span class="n">author</span><span class="p">,</span>
            <span class="n">date</span><span class="o">=</span><span class="n">datetime</span><span class="o">.</span><span class="n">datetime</span><span class="o">.</span><span class="n">now</span><span class="p">())</span>
        <span class="n">comment</span><span class="o">.</span><span class="n">save</span><span class="p">()</span>
    <span class="n">comments</span> <span class="o">=</span> <span class="n">Comment</span><span class="o">.</span><span class="n">select</span><span class="p">()</span><span class="o">.</span><span class="n">order_by</span><span class="p">(</span><span class="n">Comment</span><span class="o">.</span><span class="n">date</span><span class="o">.</span><span class="n">desc</span><span class="p">())</span>
    <span class="k">return</span> <span class="n">render_template</span><span class="p">(</span><span class="s">'index.html'</span><span class="p">,</span> <span class="n">comments</span><span class="o">=</span><span class="n">comments</span><span class="p">)</span>

<span class="k">if</span> <span class="n">__name__</span> <span class="o">==</span> <span class="s">'__main__'</span><span class="p">:</span>
    <span class="n">app</span><span class="o">.</span><span class="n">run</span><span class="p">()</span>
</pre>

Simple right ?

We use [Peewee](http://docs.peewee-orm.com/en/latest/ "Peewee") as ORM.

And here is the index.html template, based on jinja2

```
<html class="no-js" lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Flask app</title>
    <link rel="stylesheet" href="/static/css/foundation.css" />
    <script src="/static/js/vendor/modernizr.js"></script>
  </head>
  <body>
    <div class="row">
      <div class="large-12 columns">
        <h1>Welcome to Flask</h1>
      </div>
    </div>
    <div class="row">
      <div class="large-8 medium-8 columns">
        <!-- Grid Example -->
        <h5>Write something !</h5>
        <form action="." method="POST">
                  <div class="row">
                    <div class="large-12 columns">
                      <label>Title</label>
                      <input name="title" type="text" placeholder="Insert comment title" />
                    </div>
                  </div>
                  <div class="row">
                    <div class="large-4 medium-4 columns">
                      <label>Author</label>
                      <input name="author" type="text" placeholder="Your name" />
                    </div>
                  </div>
                  <div class="row">
                    <div class="large-12 columns">
                      <label>Message</label>
                      <textarea name="text" placeholder="Comment body"></textarea>
                    </div>
                  </div>
                  <input type="submit" class="button" value="Submit">
                </form>
      </div>
    </div>
    <div class="row">
    <div class="large-8 medium-8 columns">
    {% for comment in comments %}
       <hr />
        <h3>{{comment.id}} - {{comment.title}}</h3>
        <h5>{{comment.author}} - {{comment.date}}</h5>
        <!-- Grid Example -->
        <div class="row">
          <div class="large-12 columns">
            <div class="callout panel">
              <p>{{comment.body}}</p>
            </div>
          </div>
        </div>
 {% endfor %}
    </div>
    </div>
    <script src="/static/js/vendor/jquery.js"></script>
    <script src="/static/js/foundation.min.js"></script>
    <script>
      $(document).foundation();
    </script>
  </body>
</html>
```

With flask we are done.

## Nginx

We use nginx as proxy, to redirect some request to our python app and to serve our static files.

That's our sites-enabled conf

<pre class="code literal-block">
<span class="c1">\# yourappdir/nginx/sites-enabled/app</span>
<span class="k">server</span><span class="p">{</span>
    <span class="kn">listen</span><span class="mi">80</span><span class="p">;</span>
    <span class="kn">server_name</span> <span class="s">yourwebsite.com</span><span class="p">;</span>
    <span class="kn">charset</span>     <span class="s">utf-8</span><span class="p">;</span>
    <span class="kn">location</span> <span class="s">/static</span> <span class="p">{</span>
        <span class="kn">alias</span> <span class="s">/www/static</span><span class="p">;</span> <span class="c1">\# your project's static files</span>
        <span class="p">}</span>
    <span class="kn">location</span> <span class="s">/</span> <span class="p">{</span>
        <span class="kn">proxy_pass</span> <span class="s">http://python:8000</span><span class="p">;</span>
        <span class="kn">proxy_set_header</span> <span class="s">Host</span> <span class="nv">$host</span><span class="p">;</span>
        <span class="kn">proxy_set_header</span> <span class="s">X-Real-IP</span> <span class="nv">$remote_addr</span><span class="p">;</span>
        <span class="kn">proxy_set_header</span> <span class="s">X-Forwarded-For</span> <span class="nv">$proxy_add_x_forwarded_for</span><span class="p">;</span>
        <span class="p">}</span>
    <span class="p">}</span>
</pre>

The only thing that can looks strange is "proxy_pass http://python:8000", when we link a container to another container Docker insert a new line inside linked container
/etc/hosts, something like "172.0.0.x python".

This is how our nginx container know our python app ip.

## Docker and docker-compose file

And now it's the time to talk about Docker and docker-compose.

This is our one line Dockerfile used to build python app container.

We use the power of [ON BUILD](https://docs.docker.com/reference/builder/#onbuild "ON BUILD") to install all requirements and copy the current directory inside the container /usr/src/app

<pre class="code literal-block">
# yourappdir/Dockerfile
FROM python:3.4.2-onbuild
</pre>

This is Dockerfile for nginx container

<pre class="code literal-block">
# yourappdir/nginx/Dockerfile
FROM tutum/nginx
RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled
ADD static/ /www/static
</pre>

For postgres we use the official image available on Docker registry.

Now it's the time for docker-compose.

I think that docker-compose it's a great tool that Docker didn't have.

Basically we have a [CLI](https://github.com/docker/fig/blob/master/docs/cli.md "CLI") and a [yml file](https://github.com/docker/fig/blob/master/docs/yml.md "yml file") that describes which containers you want to create and some options.

If you have some experience with Docker you'll see something familiar in some parameters.

In our case we create 3 containers, python, nginx and postgres

The first line (python, nginx and postgres) are just alias for the containers

<pre class="code literal-block">
<span class="c1">\######################</span><span class="c1">\## PYTHON CONTAINER ##</span>
<span class="c1">\######################</span>
<span class="l-Scalar-Plain">python</span><span class="p-Indicator">:</span>
    <span class="l-Scalar-Plain">restart</span><span class="p-Indicator">:</span> <span class="l-Scalar-Plain">always</span>
    <span class="l-Scalar-Plain">build</span><span class="p-Indicator">:</span> <span class="l-Scalar-Plain">.</span>
    <span class="l-Scalar-Plain">expose</span><span class="p-Indicator">:</span>
        <span class="p-Indicator">-</span> <span class="s">"8000"</span>
    <span class="l-Scalar-Plain">links</span><span class="p-Indicator">:</span>
        <span class="p-Indicator">-</span> <span class="l-Scalar-Plain">postgres:postgres</span>
    <span class="l-Scalar-Plain">volumes</span><span class="p-Indicator">:</span>
        <span class="p-Indicator">-</span> <span class="l-Scalar-Plain">/usr/src/app</span>
    <span class="l-Scalar-Plain">command</span><span class="p-Indicator">:</span> <span class="l-Scalar-Plain">/usr/local/bin/gunicorn -w 2 -b :8000 app:app</span>

<span class="c1">\#####################</span>
<span class="c1">\## NGINX CONTAINER ##</span>
<span class="c1">\#####################</span>
<span class="l-Scalar-Plain">nginx</span><span class="p-Indicator">:</span>
    <span class="l-Scalar-Plain">restart</span><span class="p-Indicator">:</span> <span class="l-Scalar-Plain">always</span>
    <span class="l-Scalar-Plain">build</span><span class="p-Indicator">:</span> <span class="l-Scalar-Plain">./nginx/</span>
    <span class="l-Scalar-Plain">ports</span><span class="p-Indicator">:</span>
        <span class="p-Indicator">-</span> <span class="s">"80:80"</span>
    <span class="l-Scalar-Plain">volumes</span><span class="p-Indicator">:</span>
        <span class="p-Indicator">-</span> <span class="l-Scalar-Plain">/www/static</span>
    <span class="l-Scalar-Plain">links</span><span class="p-Indicator">:</span>
        <span class="p-Indicator">-</span> <span class="l-Scalar-Plain">python:python</span>

<span class="c1">\####################</span>
<span class="c1">\## POSTGRES CONTAINER ##</span>
<span class="c1">\####################</span>
<span class="l-Scalar-Plain">postgres</span><span class="p-Indicator">:</span>
    <span class="l-Scalar-Plain">restart</span><span class="p-Indicator">:</span> <span class="l-Scalar-Plain">always</span>
    <span class="l-Scalar-Plain">image</span><span class="p-Indicator">:</span> <span class="l-Scalar-Plain">postgres</span>
    <span class="l-Scalar-Plain">expose</span><span class="p-Indicator">:</span>
        <span class="p-Indicator">-</span> <span class="s">"5432"</span>
</pre>

Cool, that's all !

now we can type this command

<pre class="code literal-block">
<span class="nv">$ </span>docker-compose --file build.yml up -d
</pre>

And docker-compose will start to create and run our Docker containers.
First it tries to pull/build the image specified then it creates and runs the
Docker container with our parameters and the right order.

In our example postgres will be created before the python container and nginx will be the last created container.

How to check which containers are running ?

<pre class="code literal-block">
<span class="nv">$ </span>docker-compose --file build.yml ps
</pre>

And how to see the logs of containers ?

<pre class="code literal-block">
<span class="nv">$ </span>docker-compose --file build.yml logs
</pre>

## Problems

I would like to tell more about some "issues" that I've met.

#### Postgres database

It is fucki*ng hard to create a postgres database without using psql or connect directly to the database.
In my example database must exist before or at the same time that app was running, essentially because without the database you'll get some errors.

So I've tried to use pyscopg2 to check if the database exists or not and then create it, but without great results.

The best solution probably is to create a new database during image creation, but in the official Postgres image this option is still not available.

In my case I've used the default "postgres" db.

#### Image and container rebuild

I think can be a good option to have the possibility to choice which containers recreate and which not and the same for the images.
For example I would like to have some data containers inside build.yml but it's risky, because with _rm_ you remove all containers inside your build.yml...

<pre class="code literal-block">
<span class="nv">$docker</span>-compose --file build.yml rm
<span class="c">\# SHIT MY DATABASE DATA ARE LOST !</span>
</pre>

Of course you have "--no-recreate" option but is referred to existing containers.

Now it's time for my questions.

Do I miss something ? Or maybe I could make something better ?

I like to hear your experiences about how to handle Docker orchestration !
