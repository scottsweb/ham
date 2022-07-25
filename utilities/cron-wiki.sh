#!/bin/bash

# docker exec -it wiki sh -c "tiddlywiki ./*mywiki --render \"[\!is[system]\!tag[private]]\""
# tiddlywiki ./*mywiki --render "[!is[system]!tag[private]]" $:/core/save/all static/index.html text/plain "" exportFilter
# tiddlywiki ./*mywiki --rendertiddlers [!is[system]!tag[private]] $:/core/templates/static.tiddler.html static text/plain --rendertiddler $:/core/templates/static.template.html static.html text/plain --rendertiddler $:/core/templates/static.template.css static/static.css text/plain
# tiddlywiki --rendertiddlers [!is[system]tag[Live]] $:/didaxy/templates/static.tiddler.html static text/plain --rendertiddler $:/didaxy/templates/static.template.css static/static.css text/plain --savetiddler $:/didaxy/favicon.png static/favicon.png
# tiddlywiki ./*mywiki --render "[!is[system]!tag[private]]" "[encodeuricomponent[]addprefix[export/]addsuffix[.html]]" $:/core/templates/tiddlywiki5.html text/plain
# tiddlywiki ./*mywiki --rendertiddler $:/core/save/all static/index.html text/plain "" exportFilter "[!tag[private]]"
# tiddlywiki ./*mywiki --rendertiddler $:/core/templates/tiddlywiki5.html index.html text/plain "" exportFilter "[!tag[private]]"
# tiddlywiki ./*mywiki --rendertiddler "$:/plugins/tiddlywiki/tiddlyweb/save/offline" index.html text/plain "" publishFilter "-[tag[private]] -[has[draft.of]] +[[$:/export.css]]"
# tiddlywiki ./readonly --rendertiddler "$:/plugins/tiddlywiki/tiddlyweb/save/offline" index.html text/plain "" publishFilter "-[tag[private]] -[has[draft.of]]"

# git checkout master
# cd ../
# git add .
# git commit -am "Saved on: `date`"
# git push origin master
# git checkout gh-pages
# git merge master
# git push origin gh-pages
# git checkout master

#docker exec -it wiki sh -c 'tiddlywiki ./mywiki --rendertiddler "$:/favicon.ico" favicon.ico image/x-icon'
# --savetiddler "$:/favicon.ico" favicon.ico # works only when icon mime type changed
docker exec -it wiki sh -c 'tiddlywiki ./mywiki --savetiddlers [is[image]] images --setfield [is[image]] _canonical_uri $:/core/templates/canonical-uri-external-image text/plain --setfield [is[image]] text "" text/plain --rendertiddler "$:/export" index.html text/plain "" publishFilter "-[tag[private]] -[has[draft.of]]"'
