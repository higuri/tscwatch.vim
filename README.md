tscwatch.vim
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

Usage Example
-------------

### Compile 'example.ts'

    :e example.ts
    :TscWatchStart %
    ... some editing ...
    :w

This triggers compilation and the output will be shown in cmdline or quickfix.

#### Compilation succeeded

    Done: tsc --watch example.ts

#### Compilation failed

    1 example.ts|2 col 17| error TS2304: Cannot find name 'foo'.
    2 example.ts|3 col 12| error TS2304: Cannot find name 'bar'.
    [Quickfix List] tsc --watch example.ts

### Use tsconfig.json

If your project has 'tsconfig.json'
you can start tscwatch by simply running

    :TscWatchStart

> `tsc` searches for the tsconfig.json file starting in the current directory and continuing up the parent directory chain.


Instalation
-----------

### Prerequisite

* Vim compiled with Python 3+ support
* `tsc` in your PATH

You can check by

    $ vim --version | grep +python3

### Vundle

If you have Vundle installed, add the following line to your .vimrc

    Plugin 'higuri/tscwatch.vim

and then run

    :PluginInstall


Configuration
-------------

### Change `tsc` used by tscwatch.vim

If you want to use `tsc` installed to the local node_modules directory,
add the following line to your .vimrc

    let g:tscwatch_tsccmd = 'npx tsc'

