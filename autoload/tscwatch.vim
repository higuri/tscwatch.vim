"
" autoload/tscwatch.vim
"

let s:curdir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
let s:pyfile = s:curdir . '/python/test.py'
execute 'pyxfile ' . s:pyfile
pythonx import vim

function! tscwatch#start(args)
    pythonx tscwatch_start(vim.eval('a:args'))
endfunction

function! tscwatch#stop()
    pythonx tscwatch_stop()
endfunction
