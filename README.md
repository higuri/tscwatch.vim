vim-tsc
========

Vim plugin to run the TypeScript compiler in watch mode.

- Run `tsc --watch` asynchronously in vim.
- Show the each compilation result in vim.
- Compilation errors are shown in the quickfix window.

Command Usage
-------------

Start compilation by executing

	:TscWatchStart [arguments to tsc]

Stop compilation by executing

	:TscWatchStop

> `:TscWatchStop` is called automatically when vim exists.

### Example

Start tscwatch for 'example.ts'

    :TscWatchStart example.ts

Edit 'example.ts' and save it.

    :e example.ts
    ... some editing ...
    :w

This triggers compilation and the output will be shown in cmdline or quickfix.
* Compilation succeeded


    Done: tsc --watch example.ts

* Compilation failed


    1 example.ts|2 col 17| error TS2304: Cannot find name 'foo'.
    2 example.ts|3 col 12| error TS2304: Cannot find name 'bar'.
    [Quickfix List] tsc --watch example.ts


If you have 'tscconfig.json' in the current directory
you can start tscwatch by simply running

    :TscWatchStart


Instalation
-----------

### Vundle

If you have Vundle installed, add the following to your .vimrc

    Plugin 'higuri/vim-tsc'

and then run

    :PluginInstall

