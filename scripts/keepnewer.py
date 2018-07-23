# Copyright (C) 2018 Radiant Solutions (http://www.radiantsolutions.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
        delta = self.total_seconds(
            dest_file.last_update - src_file.last_update
        )
        if src_file.operation_name == 'download' and delta > 0:
            LOG.debug(
                "not syncing: %s -> %s, destination newer by %ss",
                src_file.src, src_file.dest, delta
            )

            # delta is positive, so the destination file is newer
            # what is s3, return False to keep it.
            return False
        else:
            return super(KeepNewerSync, self).determine_should_sync(
                src_file, dest_file
            )


def awscli_initialize(cli):
    cli.register('building-command-table.sync', register_sync_strategies)


def register_sync_strategies(command_table, session, **kwargs):
    strategy = KeepNewerSync(sync_type='file_at_src_and_dest')
    strategy.register_strategy(session)
