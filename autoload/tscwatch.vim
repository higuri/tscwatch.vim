"
" autoload/tscwatch.vim
"

let s:curdir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
let s:pyfile = s:curdir . '/python/test.py'
execute 'pyxfile ' . s:pyfile

function! tscwatch#tscwatch()
    pythonx tscwatch_test()
endfunction
