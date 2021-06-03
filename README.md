# Export docs

**Description**:  Export docs to a single file

Currently in alpha phase

## Dependencies

mkdocs

## Configuration

-

## Usage

Install this plugin (it will also install mkdocs if required)

```shell
$ pip install git+https://github.com/simon-dt/MkdocsExportPlugin.git
```

> **Note**. Since this package is in alpha stage, it is not yet available from pypi, so the only way to install it is via git.

### Customization

The layout of the exported page is a template file with jinja2 embedded contents. The package provides such a template by default, with the following content:

```markdown
[
    {% for page in pages %}
    {
        "title": "{{page.title}}",
        "file": "{{page.file.name}}",
        "content":"{{page.content|escape}}"
    }{%if loop.nextitem %},{%endif%}
    {% endfor %}
]
```

You can also provide your own template. The `page` object contains all the metadata in a mkdocs page, and in addition a `.filename` attribute, which contains the file name of the source of the page (relative to the docs folder), which can be used to link to that page.

The full customizable options for the plugin are:

* `export_folder`: Folder in which the file will be written (`export` by default, relative to the folder in which `mkdocs` is invoked). It can be set to an absolute path, such as `/tmp/mysite/export`. The required folders are created.
* `export_filename`: File to which the data is written. (`docs.json` by default)
* `export_template`: Path to the file which contains the template for the export page. It is `None` by default, which means that the package-provided template is used. It can be an absolute path, or relative to the folder in which `mkdocs` is run.

## How to test the software

-

## Known issues

-
