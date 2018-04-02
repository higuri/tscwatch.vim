"
" plugin/tscwatch.vim
"

" TODO: support python2.
if !has('python3')
    finish
endif
if exists("g:loaded_tscwatch")
    finish
endif
let g:loaded_tscwatch = 1
let s:save_cpo = &cpo
set cpo&vim

command! TscWatch call tscwatch#tscwatch()

let &cpo = s:save_cpo
unlet s:save_cpo
