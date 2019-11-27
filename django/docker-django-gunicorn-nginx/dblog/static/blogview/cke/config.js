/**
* @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
* For licensing, see LICENSE.html or http://ckeditor.com/license
*/
CKEDITOR.editorConfig = function( config ) {
    // Define changes to default configuration here. For example:
    config.language = 'zh-cn';
    config.toolbarGroups = [
        { name: 'mode'},
        { name: 'pbckcode'},
        { name: 'doctools'},
        { name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
        { name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
        { name: 'forms' },
        '/',
        { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
        { name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align' ] },
        { name: 'links' },
        { name: 'insert' },
        '/',
        { name: 'styles' },
        { name: 'colors' },
        { name: 'tools' },
        { name: 'others' },
        { name: 'about' }
    ];

    config.pasteFromWordRemoveFontStyles = false;
    config.pasteFromWordRemoveStyles = false;

    config.allowedContent = true;
    config.extraPlugins = 'pbckcode';
    config.pbckcode = {
        modes :  [
            ["C9Search"     , "c9search"],
            ["C/C++"        , "c_pp"],
            ["C#"           , "csharp"],
            ["Clojure"      , "clojure"],
            ["CoffeeScript" , "coffee"],
            ["ColdFusion"   , "coldfusion"],
            ["CSS"          , "css"],
            ["Diff"         , "diff"],
            ["Glsl"         , "glsl"],
            ["Go"           , "golang"],
            ["Groovy"       , "groovy"],
            ["haXe"         , "haxe"],
            ["HTML"         , "html"],
            ["Jade"         , "jade"],
            ["Java"         , "java"],
            ["JavaScript"   , "javascript"],
            ["JSON"         , "json"],
            ["JSP"          , "jsp"],
            ["JSX"          , "jsx"],
            ["LaTeX"        , "latex"],
            ["LESS"         , "less"],
            ["Liquid"       , "liquid"],
            ["Lua"          , "lua"],
            ["LuaPage"      , "luapage"],
            ["Markdown"     , "markdown"],
            ["OCaml"        , "ocaml"],
            ["OpenSCAD"     , "scad"],
            ["Perl"         , "perl"],
            ["pgSQL"        , "pgsql"],
            ["PHP"          , "php"],
            ["Powershell"   , "powershel1"],
            ["Python"       , "python"],
            ["R"            , "ruby"],
            ["Scala"        , "scala"],
            ["SCSS/Sass"    , "scss"],
            ["SH"           , "sh"],
            ["SQL"          , "sql"],
            ["SVG"          , "svg"],
            ["Tcl"          , "tcl"],
            ["Textile"      , "textile"],
            ["Text"         , "text"],
            ["XML"          , "xml"],
            ["XQuery"       , "xq"],
            ["YAML"         , "yaml"]
        ],

        // theme: "clouds_midnight",
        // theme: "cobalt",
        // theme: "idle_fingers",
        // theme: "kr_theme",
        // theme: "merbivore",
        // theme: "merbivore_soft",
        // theme: "mono_industrial",
        // theme: "monokai",
        // theme: "pastel_on_dark",
        theme: "solarized_dark",
        // theme: "tomorrow_night",
        // theme: "tomorrow_night_blue",
        // theme: "tomorrow_night_bright",
        // theme: "tomorrow_night_eighties",
        // theme: "twilight",
        // theme: "vibrant_ink",

        highlighter : "PRETTIFY"
    };
};
