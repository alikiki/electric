# electric

`electric` is a static site generator that I use to generate my [personal website](https://hajeon.xyz/). It's also the name of the markup language that I use to decorate my blog posts. My original website ran on Jekyll, but it felt too clunky and overpowered for my needs. Because Jekyll has a lot of dependencies (such as Liquid), it was sometimes frustrating to debug and I always thought that a static site generator wouldn't be **that** hard to make. Well, I was wrong - this was pretty hard to make. 

`electric` is extremely specific to my blogging workflow, and while there are plans to extend functionality of both the language and the site generator, I don't really have any intention of extending it past my own needs. 

## `electric`: the language

The `electric` language is just a simple macro language - similar to Markdown. The syntax is pretty Lisp-y, but that's because I only really know how to make Lisp-y interpreters. In terms of style, it's a combination of Markdown and LaTeX. The tokenizer, parser, and interpreters are all homemade, so no dependencies too!

The main way to use `electric` is with the following syntax: `@operation{arg1||arg2||...||argn}`. For example, to bold a piece of text, do `@b{a piece of text}`. For functions with arity greater than 1 e.g. links, do `@link{someURL.com||a description of the URL}`. And that's it! You can define you own macros by going into `lang/program.py` and adding your desired function into the standard environment. 

## `electric`: the static site generator

`electric` works in a **really** simple way. You define source and target paths in the `config.json` file, and `electric` builds the files according to the templates in the `templates/` folder. That's it! (By the way, `electric` only builds source files that end in the `.electric` extension). 

Do you want a good feedback loop in your blogging workflow? Running `python main.py` builds the files in real-time, allowing you to get instant feedback about how your writing looks on the webpage itself. 

Similar to the language, `electric` the site generator has almost no dependencies, other than [https://github.com/gorakhargosh/watchdog/](watchdog). Just `pip install watchdog`, and you're good to go. 





