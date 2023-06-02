
.. image:: https://raw.githubusercontent.com/Nekmo/kuangcaowangyunmin/master/logo.png
    :width: 100%

|


.. image:: https://img.shields.io/github/workflow/status/Nekmo/kuangcaowangyunmin/Tests.svg?style=flat-square&maxAge=2592000
  :target: https://github.com/Nekmo/kuangcaowangyunmin/actions?query=workflow%3ATests
  :alt: Latest Tests CI build status

.. image:: https://img.shields.io/pypi/v/kuangcaowangyunmin.svg?style=flat-square
  :target: https://pypi.org/project/kuangcaowangyunmin/
  :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/kuangcaowangyunmin.svg?style=flat-square
  :target: https://pypi.org/project/kuangcaowangyunmin/
  :alt: Python versions

.. image:: https://img.shields.io/codeclimate/maintainability/Nekmo/kuangcaowangyunmin.svg?style=flat-square
  :target: https://codeclimate.com/github/Nekmo/kuangcaowangyunmin
  :alt: Code Climate

.. image:: https://img.shields.io/codecov/c/github/Nekmo/kuangcaowangyunmin/master.svg?style=flat-square
  :target: https://codecov.io/github/Nekmo/kuangcaowangyunmin
  :alt: Test coverage

.. image:: https://img.shields.io/requires/github/Nekmo/kuangcaowangyunmin.svg?style=flat-square
     :target: https://requires.io/github/Nekmo/kuangcaowangyunmin/requirements/?branch=master
     :alt: Requirements Status


###############
kuangcaowangyunmin
###############
Telegram-upload uses your personal Telegram account to upload and download files up to 2GiB (bots are limited to 50
MiB). Turn Telegram into your personal cloud!


To **install kuangcaowangyunmin**, run this command in your terminal:

.. code-block:: console

    $ kuangcaowangyunmin 2023_05_26_16_45_33.pp --to -1001569385968 --vif True --dzffn jjk -d --nobar True

vif 参数为 True 则忽略文件名后缀 强制以视频上传


dzffn 参数指定 ffmpeg 的定制化名字 


nobar 参数关闭进度条显示



.. code-block:: console

    $ sudo pip3 install -U kuangcaowangyunmin

This is the preferred method to install kuangcaowangyunmin, as it will always install the most recent stable release.
`More info in the documentation <https://docs.nekmo.org/kuangcaowangyunmin/installation.html>`_


To use this program you need an Telegram account and your *App api_id/api_hash* (get it in
`my.telegram.org <https://my.telegram.org/>`_). The first time you use kuangcaowangyunmin it requests your telephone,
api_id and api_hash. Bot tokens can not be used with this program (bot uploads are limited to 50MB). To **send files**
(by default it is uploaded to saved messages):

.. code-block:: console

    $ kuangcaowangyunmin file1.mp4 /path/to/file2.mkv

Credentials are saved in ``~/.config/kuangcaowangyunmin.json`` and ``~/.config/kuangcaowangyunmin.session``. You must make
sure that these files are secured. You can copy these files to authenticate ``kuangcaowangyunmin`` on more machines, but
it is advisable to create a session file for each machine. Upload options are available
`in the documentation <https://docs.nekmo.org/kuangcaowangyunmin/usage.html#kuangcaowangyunmin>`_.


You can download the files again from your saved messages (by default) or from a channel. All files will be
downloaded until the last text message.

.. code-block:: console

    $ telegram-download

The ``--delete-on-success`` option allows you to delete the Telegram message after downloading the file. This is
useful to send files to download to your saved messages and avoid downloading them again. You can use this option to
download files on your computer away from home.
`Read the documentation <https://docs.nekmo.org/kuangcaowangyunmin/usage.html#telegram-download>`_ for more info.


Features
========

* Upload multiples files (up to 2GiB per file)
* Download files.
* Add video thumbs.
* Delete local or remote file on success.

Docker
======
Run kuangcaowangyunmin without installing it on your system using Docker. Instead of ``kuangcaowangyunmin``
and ``telegram-download`` you should use ``upload`` and ``download``. Usage::


    docker run -v <files_dir>:/files/
               -v <config_dir>:/config
               -it nekmo/kuangcaowangyunmin:master
               <command> <args>

* ``<files_dir>``: upload or download directory.
* ``<config_dir>``: Directory that will be created to store the kuangcaowangyunmin configuration.
  It is created automatically.
* ``<command>``: ``upload`` and ``download``.
* ``<args>``: ``kuangcaowangyunmin`` and ``telegram-download`` arguments.

For example::

    docker run -v /media/data/:/files/
               -v $PWD/config:/config
               -it nekmo/kuangcaowangyunmin:master
               upload file_to_upload.txt


