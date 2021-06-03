from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type

import os
import json
import jinja2
import urllib.parse
from pathlib import Path

def _extract_meta(meta_data, data_name):
    if data_name in meta_data:
        return meta_data[data_name]
    else:
        return []


def _retrievedata(page, config):
    if config['site_url'] is None:
        url = '/' + page.file.url
    else:
        url = urllib.parse.urljoin(config['site_url'], page.file.url)
    data = {
        'title': page.title,
        'file_name': page.file.name,
        'url': url,
        'tags': _extract_meta(page.meta, 'tags'),
        'description': _extract_meta(page.meta, 'description')
    }
    return data


def _make_new_json(filepath):
    data_template = [{'test':'okay'}]
    with open(filepath, mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data_template, ensure_ascii=False, indent=2))


def _add_data_to(filepath, additional_data):
    if not os.path.isfile(filepath):
        _make_new_json(filepath)

    with open(filepath, mode='r', encoding='utf-8') as f:
        data = json.load(f)

    with open(filepath, mode='w', encoding='utf-8') as f:
        data.append(additional_data)
        f.write(json.dumps(data, ensure_ascii=False, indent=2))


class ExportPlugin(BasePlugin):
    """
    Creates "export.json" file containing all docs using the template
    """

    config_scheme = (
        ('export_folder', Type(str, default='export')),
        ('export_filename', Type(str, default='docs.json')),
        ('export_template', Type(str))
    )

    def __init__(self):
        self.docsData = []
        self.export_filename = "docs.json"
        self.export_folder = "export"
        self.export_template = None

    def on_config(self, config):
        # Re assign the options
        self.export_filename = Path(self.config.get("export_filename") or self.export_filename)
        self.export_folder = Path(self.config.get("export_folder") or self.export_folder)
        # Make sure that the export folder is absolute, and exists
        if not self.export_folder.is_absolute():
            self.export_folder = Path(config["docs_dir"]) / ".." / self.export_folder
        if not self.export_folder.exists():
            self.export_folder.mkdir(parents=True)

        if self.config.get("export_template"):
            self.export_template = Path(self.config.get("export_template"))

    def on_page_markdown(self, markdown, **kwargs):
        config = kwargs.get('config')
        page = kwargs.get('page')

        if config['site_url'] is None:
            url = '/' + page.file.url
        else:
            url = urllib.parse.urljoin(config['site_url'], page.file.url)

        self.docsData.append(page)
        return markdown

    def on_post_build(self, **kwargs):
        if self.export_template is None:
            templ_path = Path(__file__).parent  / Path("templates")
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(str(templ_path))
                )
            templ = environment.get_template("export.json.template")
        else:
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(searchpath=str(self.export_template.parent))
            )
            templ = environment.get_template(str(self.export_template.name))
        output_text = templ.render(
                pages=self.docsData,
        )

        with open(str(self.export_folder / self.export_filename), "w") as f:
            f.write(output_text)