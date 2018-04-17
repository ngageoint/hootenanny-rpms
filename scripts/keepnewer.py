import logging

from awscli.customizations.s3.syncstrategy.base import SizeAndLastModifiedSync


LOG = logging.getLogger('awscli.customizations.s3.syncstrategy.keepnewer')


KEEP_NEWER = {
    'name': 'keep-newer',
    'action': 'store_true',
    'help_text': (
        'When syncing from S3 to local, keep local items that have timestamps '
        'newer than existing items in S3. The default behavior is to '
        'overwrite newer files with the S3 version.'
    )
}


class KeepNewerSync(SizeAndLastModifiedSync):

    ARGUMENT = KEEP_NEWER

    def determine_should_sync(self, src_file, dest_file):
        src_time = src_file.last_update
        dest_time = dest_file.last_update
        delta = dest_time - src_time
        cmd = src_file.operation_name

        if cmd == 'download' and self.total_seconds(delta) > 0:
            LOG.debug(
                "KeepNewerSync.determine_should_sync: %s -> %s, total_seconds: %s",
                src_file.src,
                src_file.dest,
                self.total_seconds(delta)
            )

            # delta is positive, so the destination file is newer
            # what is s3, return False to keep it.
            return False
        else:
            return super(KeepNewerSync, self).determine_should_sync(src_file, dest_file)


def awscli_initialize(cli):
    cli.register('building-command-table.sync', register_sync_strategies)


def register_sync_strategies(command_table, session, **kwargs):
    strategy = KeepNewerSync(sync_type='file_at_src_and_dest')
    strategy.register_strategy(session)
