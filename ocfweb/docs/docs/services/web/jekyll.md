[[!meta title="Jekyll"]]

[Jekyll](https://jekyllrb.com) is a popular static website generator.

## Set up 

1. Go to our [web-based SSH client](https://ssh.ocf.berkeley.edu/) and sign in
   with your username and password. Or, at terminal, SSH into tsuanami.ocf.berkeley.edu.

2. Install Jekyll locally:
```shell
  gem install jekyll --user-install 
```

3. Source the executable:
```shell
  echo "PATH=$PATH:~/.gem/ruby/2.1.0/bin">>~/.bash_profile
  source ~/.bash_profile
```

## Create a new (template) site

1. Create a new site in directory "jk" (can replace "jk" with any name you'd like):  
```shell
  jekyll new jk
```
Here it will prompt you to enter root password - abort by Ctrl-c.

2. Install dependencies:
```shell
  cd jk
  bundle install --path vendor/bundle
```

## Deploy 

1. Change baseurl field in _config.yml file to "/~{Your OCF username}".

2. Build the site in ~/public_html (run this also to reflect the changes you make):
```shell
bundle exec jekyll build -d ~/public_html
```

3. Your site should be up at ocf.berkeley.edu/~{Your OCF username}

## Quick Start Guide

We've created a default template site of the theme Minima. Let's see how to make it yours:

1. In the site directory ("jk"), there is a subdirectory _posts. Blog posts go there as md files. Please follow the sample post file there to make your own (note the YAML header at the top in between "---"s and the file name format).

2. Other than blog posts, you can also make pages (about, contact, etc.) that are linked at the top right of the site. An example is the about.md file in the site directory (note the YAML header with layout: page).

3. In _config.yml in the site directory are global site settings, where you can change the title of the site among others.  

## Advanced Guide

Please see [Jekyll Docs](https://jekyllrb.com/docs/home/)

Here are some that might be of interest:

1. [Using a different theme](https://jekyllrb.com/docs/themes/#installing-a-theme) (Themes might be non-compatible with each other: the YAML header format might be different, for instance)
2. [Using variables](https://jekyllrb.com/docs/variables/)

