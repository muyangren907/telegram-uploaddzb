# -*- coding: utf-8 -*-

"""Console script for telegram-upload."""

import click
from telegram_upload.client import Client
from telegram_upload.config import default_config, CONFIG_FILE
from telegram_upload.exceptions import catch
from telegram_upload.files import NoDirectoriesFiles, RecursiveFiles, NoLargeFiles, SplitFiles, is_valid_file

from telegram_upload.utils import async_to_sync

DIRECTORY_MODES = {
    'fail': NoDirectoriesFiles,
    'recursive': RecursiveFiles,
}
LARGE_FILE_MODES = {
    'fail': NoLargeFiles,
    'split': SplitFiles,
}


async def show_checkboxlist(iterator):
    # iterator = map(lambda x: (x, f'{x.text} by {x.chat.first_name}'), iterator)
    from prompt_toolkit import Application
    from prompt_toolkit.layout import Layout
    from telegram_upload.cli import IterableCheckboxList
    iterator = iterator.iter_files('me')
    try:
        checkbox_list = IterableCheckboxList(
            values=iterator
        )
        await checkbox_list._init(iterator)
    except IndexError:
        click.echo('No items were found. Exiting...', err=True)
        return []
    app = Application(full_screen=False, layout=Layout(checkbox_list), mouse_support=True)
    await app.run_async()


class MutuallyExclusiveOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help = kwargs.get('help', '')
        if self.mutually_exclusive:
            kwargs['help'] = help + (
                ' NOTE: This argument is mutually exclusive with'
                ' arguments: [{}].'.format(self.mutually_exclusive_text)
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(
                    self.name,
                    self.mutually_exclusive_text
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )

    @property
    def mutually_exclusive_text(self):
        return ', '.join([x.replace('_', '-') for x in self.mutually_exclusive])


@click.command()
@click.argument('files', nargs=-1)
@click.option('--to', default='me', help='Phone number, username, invite link or "me" (saved messages). '
                                         'By default "me".')
@click.option('--quchu', default='me', help='Phone number, username, invite link or "me" (saved messages). '
                                         'By default "me".')
@click.option('--vif', default=False, help='上传文件是否为视频文件 默认为False 可以上传任意后缀的视频文件 '
                                         'By default "False".')
@click.option('--nobar', default=False, help='是否禁用进度条显示 默认为False'
                                         'By default "False".')
@click.option('--dzffn', default='ffmpeg', help='定制ffmpeg名字 默认为ffmpeg'
                                         'By default "False".')
@click.option('--config', default=None, help='Configuration file to use. By default "{}".'.format(CONFIG_FILE))
@click.option('--c1', default=None, help='Configuration file to use. By default "{}".'.format(CONFIG_FILE))
@click.option('-d', '--delete-on-success', is_flag=True, help='Delete local file after successful upload.')
@click.option('--print-file-id', is_flag=True, help='Print the id of the uploaded file after the upload.')
@click.option('--force-file', is_flag=True, help='Force send as a file. The filename will be preserved '
                                                 'but the preview will not be available.')
@click.option('-f', '--forward', multiple=True, help='Forward the file to a chat (alias or id) or user (username, '
                                                     'mobile or id). This option can be used multiple times.')
@click.option('--directories', default='fail', type=click.Choice(list(DIRECTORY_MODES.keys())),
              help='Defines how to process directories. By default directories are not accepted and will raise an '
                   'error.')
@click.option('--large-files', default='fail', type=click.Choice(list(LARGE_FILE_MODES.keys())),
              help='Defines how to process large files unsupported for dxdmgch. By default large files are not '
                   'accepted and will raise an error.')
@click.option('--caption', type=str, help='Change file description. By default the file name.')
@click.option('--c2', type=str, default=None, help='Change file description. By default the file name.')
@click.option('--no-thumbnail', is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["thumbnail_file"],
              help='Disable thumbnail generation. For some known file formats, dxdmgch may still generate a '
                   'thumbnail or show a preview.')
@click.option('--thumbnail-file', default=None, cls=MutuallyExclusiveOption, mutually_exclusive=["no_thumbnail"],
              help='Path to the preview file to use for the uploaded file.')
@click.option('-p', '--proxy', default=None,
              help='Use an http proxy, socks4, socks5 or mtproxy. For example socks5://user:pass@1.2.3.4:8080 '
                   'for socks5 and mtproxy://secret@1.2.3.4:443 for mtproxy.')
@click.option('-a', '--album', is_flag=True,
              help='Send video or photos as an album.')
def upload(files, to, quchu, vif, nobar, dzffn, config, c1, delete_on_success, print_file_id, force_file, forward, directories, large_files, caption, c2,
           no_thumbnail, thumbnail_file, proxy, album):
    """Upload one or more files to dxdmgch using your personal account.
    The maximum file size is 2 GiB and by default they will be saved in
    your saved messages.
    """
    if c1 is not None:
        config = c1
    if c2 is not None:
        caption = c2
    if quchu != 'me':
        to = quchu
    client = Client(config or default_config(), proxy=proxy)
    client.start()
    files = filter(lambda file: is_valid_file(file, lambda message: click.echo(message, err=True)), files)
    files = DIRECTORY_MODES[directories](files)
    if directories == 'fail':
        # Validate now
        files = list(files)
    if no_thumbnail:
        thumbnail = False
    elif thumbnail_file:
        thumbnail = thumbnail_file
    else:
        thumbnail = None
    files_cls = LARGE_FILE_MODES[large_files]
    files = files_cls(files, caption=caption, thumbnail=thumbnail, force_file=force_file, dzffn=dzffn)
    # print(type(files))
    # print(files)
    if large_files == 'fail':
        # Validate now
        files = list(files)
    if album:
        client.send_files_as_album(to, vif, nobar, files, delete_on_success, print_file_id, forward)
    else:
        client.send_files(to, vif, nobar, files, delete_on_success, print_file_id, forward)


@click.command()
@click.option('--from', '-f', 'from_', default='me',
              help='Phone number, username, chat id or "me" (saved messages). By default "me".')
@click.option('--config', default=None, help='Configuration file to use. By default "{}".'.format(CONFIG_FILE))
@click.option('-d', '--delete-on-success', is_flag=True,
              help='Delete telegram message after successful download. Useful for creating a download queue.')
@click.option('-p', '--proxy', default=None,
              help='Use an http proxy, socks4, socks5 or mtproxy. For example socks5://user:pass@1.2.3.4:8080 '
                   'for socks5 and mtproxy://secret@1.2.3.4:443 for mtproxy.')
@click.option('-i', '--interactive', is_flag=True,
              help='Use interactive mode.')
def download(from_, config, delete_on_success, proxy, interactive):
    """Download all the latest messages that are files in a chat, by default download
    from "saved messages". It is recommended to forward the files to download to
    "saved messages" and use parameter ``--delete-on-success``. Forwarded messages will
    be removed from the chat after downloading, such as a download queue.
    """
    client = Client(config or default_config(), proxy=proxy)
    client.start()

    if interactive:
        # messages = async_to_sync(show_checkboxlist(map(lambda x: (x, f'{x.text} by {x.chat.first_name}'),
        #                                  client.iter_files(from_))))
        # messages = async_to_sync(show_checkboxlist(client.iter_files(from_)))
        messages = async_to_sync(show_checkboxlist(client))
    else:
        messages = client.find_files(from_)
    client.download_files(from_, messages, delete_on_success)


upload_cli = catch(upload)
download_cli = catch(download)


if __name__ == '__main__':
    import sys
    import re
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    commands = {'upload': upload_cli, 'download': download_cli}
    if len(sys.argv) < 2:
        sys.stderr.write('A command is required. Available commands: {}\n'.format(
            ', '.join(commands)
        ))
        sys.exit(1)
    if sys.argv[1] not in commands:
        sys.stderr.write('{} is an invalid command. Valid commands: {}\n'.format(
            sys.argv[1], ', '.join(commands)
        ))
        sys.exit(1)
    fn = commands[sys.argv[1]]
    sys.argv = [sys.argv[0]] + sys.argv[2:]
    sys.exit(fn())
