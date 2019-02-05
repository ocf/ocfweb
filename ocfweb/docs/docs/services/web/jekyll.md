[[!meta title="Jekyll"]]

[Jekyll](https://jekyllrb.com) is a popular static website generator, often
used for blogs and personal websites. Since all the content it generates is
static, it makes for very fast and simple websites.

## Set up your site

1. Go to either our [web-based SSH client](https://ssh.ocf.berkeley.edu/) or a
   terminal (using [[SSH|doc services/shell]] to connect to
   `ssh.ocf.berkeley.edu`) and sign in with your OCF username and password.

2. Create a new directory for your Jekyll project and name it whatever you
   want, then enter that directory:

   ```shell
   user@tsunami:~$ mkdir jekyll
   user@tsunami:~$ cd jekyll
   ```

3. Install the Jekyll gem and set up your site. Note that the specific jekyll
   path is only needed for setup since jekyll is being installed for only your
   user, but after this setup, you can just add `bundle exec` before any
   jekyll-related commands to get them to work:

   ```shell
   user@tsunami:~/jekyll$ gem install --user jekyll

   # The path used for jekyll below should be printed out as a warning when you
   # install jekyll using the above command, it'll be something like
   # "/home/u/us/username/.gem/ruby/2.3.0/bin" but can vary by Ruby version.
   user@tsunami:~/jekyll$ ~/.gem/ruby/2.3.0/bin/jekyll new --skip-bundle .
   user@tsunami:~/jekyll$ bundle install --path vendor/bundle
   ```

## Deploy your new site

1. Change the `baseurl` option in `_config.yml` file to the path you want your
   site available at. This is likely something like `"/~username"` or
   `"/~username/blog"` (make sure to replace `username` with your username!).

2. Build the site in `~/public_html` (make sure to also run this whenever you
   make changes to your site and want to publish them). This path should match
   whatever you used for your `baseurl` option, so if you chose `"/~username"`
   there, then use `~/public_html` here, if you chose `"/~username/blog"` then
   use `~/public_html/blog` here instead:

   ```shell
   user@tsunami:~/jekyll$ bundle exec jekyll build -d ~/public_html
   ```

3. Your site should now be up at `https://www.ocf.berkeley.edu/~username` (or
   whatever path you chose previously).

## Quick Start Guide

We've just created a default template site. Let's see how to customize it a
bit to make it yours:

- On your site, there should be a new welcome post (at some path like
  `https://www.ocf.berkeley.edu/~username/jekyll/current-date/welcome-to-jekyll.html`).
  This contains instructions on how to add a new post, but we've summarized the
  instructions below:

  In your site directory (`jekyll` for instance), there should be a
  subdirectory named `_posts`. Blog posts go there by default as Markdown
  files. Please follow the sample post file there to make your own (note the
  YAML header at the top in between `---` markers and the file name format with
  the date and a title).

- Other than blog posts, you can also make other pages (about, contact, etc.)
  that are linked at the top right of the site. An example is the `about.md`
  file already placed in your site directory (note the YAML header with
  `layout: page` to specify which layout to use).

- The `_config.yml` file in your site directory contains global site settings,
  where you can change the title of the site among other settings.

## Advanced Guide

For more advanced setup, please see the [Jekyll
Docs](https://jekyllrb.com/docs/home/).

Here are some docs that might be of interest:

- [Using a different
  theme](https://jekyllrb.com/docs/themes/#installing-a-theme) (Note that
  different themes might not be compatible with each other; the YAML header
  format might be different, for instance)

- [Using variables](https://jekyllrb.com/docs/variables/)
