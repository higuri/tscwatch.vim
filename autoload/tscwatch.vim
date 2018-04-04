"
" autoload/tscwatch.vim
"

let s:curdir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
let s:pyfile = s:curdir . '/python/test.py'
execute 'py3file ' . s:pyfile
python3 import vim

function! tscwatch#start(...)
    python3 tscwatch_start(vim.eval('a:000'))
endfunction

function! tscwatch#stop()
    python3 tscwatch_stop()
endfunction
