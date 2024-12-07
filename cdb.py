from cli import cli

if __name__ == '__main__':
    if True:
        cli(auto_envvar_prefix='CALIBRE')
    else:
        try:
            cli(auto_envvar_prefix='CALIBRE')
        except Exception as error:
            logger.error(repr(error))
