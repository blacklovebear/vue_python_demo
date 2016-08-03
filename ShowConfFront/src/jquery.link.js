/*
 * jQuery Link plugin
 * copy from jQuery Highlight plugin
 *
 * Based on link v3 by Johann Burkard
 * http://johannburkard.de/blog/programming/javascript/link-javascript-text-higlighting-jquery-plugin.html
 *
 * Code a little bit refactored and cleaned (in my humble opinion).
 * Most important changes:
 *  - has an option to link only entire words (wordsOnly - false by default),
 *  - has an option to be case sensitive (caseSensitive - false by default)
 *  - link element tag and class names can be specified in options
 *
 * Usage:
 *   // wrap every occurrance of text 'lorem' in content
 *   // with <span class='link'> (default options)
 *   $('#content').link('lorem');
 *
 *   // search for and link more terms at once
 *   // so you can save some time on traversing DOM
 *   $('#content').link(['lorem', 'ipsum']);
 *   $('#content').link('lorem ipsum');
 *
 *   // search only for entire word 'lorem'
 *   $('#content').link('lorem', { wordsOnly: true });
 *
 *   // search only for the entire word 'C#'
 *   // and make sure that the word boundary can also
 *   // be a 'non-word' character, as well as a regex latin1 only boundary:
 *   $('#content').link('C#', { wordsOnly: true , wordsBoundary: '[\\b\\W]' });
 *
 *   // don't ignore case during search of term 'lorem'
 *   $('#content').link('lorem', { caseSensitive: true });
 *
 *   // wrap every occurrance of term 'ipsum' in content
 *   // with <em class='important'>
 *   $('#content').link('ipsum', { element: 'em', className: 'important' });
 *
 *   // remove default link
 *   $('#content').unlink();
 *
 *   // remove custom link
 *   $('#content').unlink({ element: 'em', className: 'important' });
 *
 *
 * Copyright (c) 2009 Bartek Szopka
 *
 * Licensed under MIT license.
 *
 */

(function (factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['jquery'], factory);
    } else if (typeof exports === 'object') {
        // Node/CommonJS
        factory(require('jquery'));
    } else {
        // Browser globals
        factory(jQuery);
    }
}(function (jQuery) {
    jQuery.extend({
        link: function (node, re, nodeName, className, linkHref) {
            if (node.nodeType === 3) {
                var match = node.data.match(re);
                if (match) {
                  console.log(linkHref);

                  // <a v-link=\"{name: 'jsonview', params: {conf_id: entry[key]}, query:{kw: keyWord}}

                    // The new link Element Node
                    var link = document.createElement(nodeName || 'a');
                    link.className = className || 'link';

                    // 将扑捉到的信息作为参数传回
                    link.setAttribute('href', linkHref + match[1]);

                    // Note that we use the captured value to find the real index
                    // of the match. This is because we do not want to include the matching word boundaries
                    var capturePos = node.data.indexOf( match[1] , match.index );

                    // Split the node and replace the matching wordnode
                    // with the linked node
                    var wordNode = node.splitText(capturePos);
                    wordNode.splitText(match[1].length);

                    var wordClone = wordNode.cloneNode(true);
                    link.appendChild(wordClone);
                    wordNode.parentNode.replaceChild(link, wordNode);
                    return 1; //skip added node in parent
                }
            } else if ((node.nodeType === 1 && node.childNodes) && // only element nodes that have children
                    !/(script|style)/i.test(node.tagName) && // ignore script and style nodes
                    !(node.tagName === nodeName.toUpperCase() && node.className === className)) { // skip if already linked
                for (var i = 0; i < node.childNodes.length; i++) {
                    i += jQuery.link(node.childNodes[i], re, nodeName, className, linkHref);
                }
            }
            return 0;
        }
    });

    jQuery.fn.unlink = function (options) {
        var settings = {
          className: 'link',
          element: 'a'
        };

        jQuery.extend(settings, options);

        return this.find(settings.element + '.' + settings.className).each(function () {
            var parent = this.parentNode;
            parent.replaceChild(this.firstChild, this);
            parent.normalize();
        }).end();
    };
    // words 表示应该选中的关键字，linkHref表示选中后链接的地址，options表示其他的一些可配置参数
    jQuery.fn.link = function (words, linkHref, options) {
        var settings = {
          className: 'link',
          element: 'a',
          caseSensitive: false,
          wordsOnly: false,
          wordsBoundary: '\\b'
        };

        jQuery.extend(settings, options);

        if (typeof words === 'string') {
          words = [words];
        }
        words = jQuery.grep(words, function(word, i){
          return word != '';
        });

        // 注释点这段代码就放开了正则匹配
        // words = jQuery.map(words, function(word, i) {
        //   return word.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&');
        // });

        if (words.length === 0) {
          return this;
        };

        var flag = settings.caseSensitive ? '' : 'i';
        // The capture parenthesis will make sure we can match
        // only the matching word
        var pattern = '(' + words.join('|') + ')';
        if (settings.wordsOnly) {
            pattern = settings.wordsBoundary + pattern + settings.wordsBoundary;
        }
        var re = new RegExp(pattern, flag);

        return this.each(function () {
            jQuery.link(this, re, settings.element, settings.className, linkHref);
        });
    };
}));
