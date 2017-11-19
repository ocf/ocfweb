[[!meta title="Jekyll"]]

[Jekyll](https://jekyllrb.com) is a popular static website generator.

## Set up

1. Go to our [web-based SSH client](https://ssh.ocf.berkeley.edu/) and sign in
   with your username and password. Or, in terminal, [[SSH|doc services/shell]]
   into `ssh.ocf.berkeley.edu`.

2. Set up [rbenv](https://github.com/rbenv/rbenv):
   ```shell
   git clone https://github.com/rbenv/rbenv.git ~/.rbenv
   echo 'export PATH="~/.rbenv/bin:$PATH"' >> ~/.bash_profile
   echo 'eval "$(rbenv init -)"' >> ~/.bash_profile
   source ~/.bash_profile
   mkdir -p "$(rbenv root)"/plugins
   git clone https://github.com/rbenv/ruby-build.git "$(rbenv root)"/plugins/ruby-build
   ```

3. Create and enter project directory "Jekyll_project" (can replace
   "Jekyll_project" with any name you'd like):
   ```shell
   mkdir Jekyll_project
   cd Jekyll_project
   ```

4. Configure ruby via [rbenv](https://github.com/rbenv/rbenv), then install
   jekyll:
   ```shell
   rbenv install -l | grep -v - | tail -1 | xargs rbenv install
   rbenv install -l | grep -v - | tail -1 | xargs rbenv local
   rbenv rehash
   gem install jekyll bundler
   ```

## Create a new (template) site

1. In project directory ("Jekyll_project"):
   ```shell
   jekyll new .
   ```

## Deploy

1. Change `baseurl` field in _config.yml file to '/~username'

2. Build the site in ~/public_html (run this also to reflect the changes you
   make):
   ```shell
   bundle exec jekyll build -d ~/public_html
   ```

3. Your site should be up at https://www.ocf.berkeley.edu/~username

## Quick Start Guide

We've created a default template site of the theme Minima. Let's see how to make
it yours:

1. In the site directory ("Jekyll_project"), there is a subdirectory _posts.
   Blog posts go there as Markdown files. Please follow the sample post file
   there to make your own (note the YAML header at the top in between "---"s and
   the file name format).

2. Other than blog posts, you can also make pages (about, contact, etc.) that
   are linked at the top right of the site. An example is the about.md file in
   the site directory (note the YAML header with layout: page).

3. In _config.yml in the site directory are global site settings, where you can
   change the title of the site among others.

## Advanced Guide

Please see [Jekyll Docs](https://jekyllrb.com/docs/home/)

Here are some that might be of interest:

1. [Using a different
   theme](https://jekyllrb.com/docs/themes/#installing-a-theme) (Themes might be
   non-compatible with each other: the YAML header format might be different,
   for instance)
2. [Using variables](https://jekyllrb.com/docs/variables/)
