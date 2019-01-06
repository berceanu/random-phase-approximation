#!/usr/bin/env python3

import argparse
import sys

def main_init(args):
    project = init_project(
        name=args.project_id,
        root=os.getcwd(),
        workspace=args.workspace)
    _print_err("Initialized project '{}'.".format(project))

    
def main():
    parser = argparse.ArgumentParser(
        description="signac aids in the management, access and analysis of "
                    "large-scale computational investigations.")
    parser.add_argument(
        '--debug',
        action='store_true',
        help="Show traceback on error for debugging.")
    parser.add_argument(
        '--version',
        action='store_true',
        help="Display the version number and exit.")
    add_verbosity_argument(parser, default=2)
    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        help="Answer all questions with yes. Useful for scripted interaction.")
    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser('init')
    parser_init.add_argument(
        'project_id',
        type=str,
        help="Initialize a project with the given project id.")
    parser_init.add_argument(
        '-w', '--workspace',
        type=str,
        default='workspace',
        help="The path to the workspace directory.")
    parser_init.set_defaults(func=main_init)

    parser_project = subparsers.add_parser('project')
    parser_project.add_argument(
        '-w', '--workspace',
        action='store_true',
        help="Print the project's workspace path instead of the project id.")
    parser_project.add_argument(
        '-i', '--index',
        action='store_true',
        help="Generate and print an index for the project.")
    parser_project.add_argument(
        '-a', '--access',
        action='store_true',
        help="Create access module for indexing.")
    parser_project.set_defaults(func=main_project)

    parser_job = subparsers.add_parser('job')
    parser_job.add_argument(
        'statepoint',
        nargs='?',
        default='-',
        type=str,
        help="The job's statepoint in JSON format. "
             "Omit this argument to read from STDIN.")
    parser_job.add_argument(
        '-w', '--workspace',
        action='store_true',
        help="Print the job's workspace path instead of the job id.")
    parser_job.add_argument(
        '-c', '--create',
        action='store_true',
        help="Create the job's workspace directory if necessary.")
    parser_job.set_defaults(func=main_job)

    parser_statepoint = subparsers.add_parser(
        'statepoint',
        description="Print the statepoint(s) corresponding to one or "
                    "more job ids.")
    parser_statepoint.add_argument(
        'job_id',
        nargs='*',
        type=str,
        help="One or more job ids. The job corresponding to a job "
             "id must be initialized.")
    parser_statepoint.add_argument(
        '-p', '--pretty',
        type=int,
        nargs='?',
        const=3,
        help="Print state point in pretty format. "
             "An optional argument to this flag specifies the maximal "
             "depth a state point is printed.")
    parser_statepoint.add_argument(
        '-i', '--indent',
        type=int,
        nargs='?',
        const='2',
        help="Specify the indentation of the JSON formatted state point.")
    parser_statepoint.add_argument(
        '-s', '--sort',
        action='store_true',
        help="Sort the state point keys for output.")
    parser_statepoint.set_defaults(func=main_statepoint)

    parser_document = subparsers.add_parser(
        'document',
        description="Print the document(s) corresponding to one or "
                    "more job ids.")
    parser_document.add_argument(
        'job_id',
        nargs='*',
        type=str,
        help="One or more job ids. The job corresponding to a job "
             "id must be initialized.")
    parser_document.add_argument(
        '-p', '--pretty',
        type=int,
        nargs='?',
        const=3,
        help="Print document in pretty format. "
             "An optional argument to this flag specifies the maximal "
             "depth a document is printed.")
    parser_document.add_argument(
        '-i', '--indent',
        type=int,
        nargs='?',
        const='2',
        help="Specify the indentation of the JSON formatted state point.")
    parser_document.add_argument(
        '-s', '--sort',
        action='store_true',
        help="Sort the document keys for output in JSON format.")
    parser_document.add_argument(
        '-f', '--filter',
        type=str,
        nargs='+',
        help="Show documents of jobs matching this state point filter.")
    parser_document.add_argument(
        '-d', '--doc-filter',
        type=str,
        nargs='+',
        help="Show documents of job matching this document filter.")
    parser_document.add_argument(
        '--index',
        type=str,
        help="The filename of an index file.")
    parser_document.set_defaults(func=main_document)

    parser_remove = subparsers.add_parser('rm')
    parser_remove.add_argument(
        'job_id',
        type=str,
        nargs='+',
        help="One or more job ids of jobs to remove.")
    parser_remove.add_argument(
        '-c', '--clear',
        action='store_true',
        help="Do not completely remove, but only clear the job.")
    parser_remove.add_argument(
        '-i', '--interactive',
        action='store_true',
        help="Request confirmation before attempting to remove/clear "
             "each job.")
    parser_remove.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Be verbose when removing/clearing files.")
    parser_remove.set_defaults(func=main_remove)

    parser_move = subparsers.add_parser('move')
    parser_move.add_argument(
        'project',
        type=str,
        help="The root directory of the project to move one or more jobs to.")
    parser_move.add_argument(
        'job_id',
        nargs='+',
        type=str,
        help="One or more job ids of jobs to move. The job corresponding to a "
             "job id must be initialized.")
    parser_move.set_defaults(func=main_move)

    parser_clone = subparsers.add_parser('clone')
    parser_clone.add_argument(
        'project',
        type=str,
        help="The root directory of the project to clone one or more jobs in.")
    parser_clone.add_argument(
        'job_id',
        nargs='+',
        type=str,
        help="One or more job ids of jobs to clone. The job corresponding to a "
             "job id must be initialized.")
    parser_clone.set_defaults(func=main_clone)

    parser_index = subparsers.add_parser('index')
    parser_index.add_argument(
        'root',
        nargs='?',
        default='.',
        help="Specify the root path from where the master index is to be compiled.")
    parser_index.add_argument(
        '-t', '--tags',
        nargs='+',
        help="Specify tags for this master index compilation.")
    parser_index.set_defaults(func=main_index)

    parser_find = subparsers.add_parser(
        'find',
        description="""All filter arguments may be provided either directly in JSON
                       encoding or in a simplified form, e.g., -- $ signac find a 42 --
                       is equivalent to -- $ signac find '{"a": 42}'."""
    )
    parser_find.add_argument(
        'filter',
        type=str,
        nargs='*',
        help="A JSON encoded state point filter (key-value pairs).")
    parser_find.add_argument(
        '-d', '--doc-filter',
        type=str,
        nargs='+',
        help="A document filter.")
    parser_find.add_argument(
        '-i', '--index',
        type=str,
        help="The filename of an index file.")
    parser_find.add_argument(
        '-s', '--show',
        type=int,
        nargs='?',
        const=3,
        help="Show the state point and document of each job.")
    parser_find.add_argument(
        '-1', '--one-line',
        action='store_true',
        help="Print output in JSON and on one line.")
    parser_find.set_defaults(func=main_find)

    parser_view = subparsers.add_parser('view')
    parser_view.add_argument(
        'prefix',
        type=str,
        nargs='?',
        default='view',
        help="The path where the view is to be created.")
    parser_view.add_argument(
        'path',
        type=str,
        nargs='?',
        default='{{auto}}',
        help="The path used for the generation of the linked view hierarchy, "
             "defaults to '{{auto}}'.")
    selection_group = parser_view.add_argument_group('select')
    selection_group.add_argument(
        '-f', '--filter',
        type=str,
        nargs='+',
        help="Limit the view to jobs matching this state point filter.")
    selection_group.add_argument(
        '-d', '--doc-filter',
        type=str,
        nargs='+',
        help="Limit the view to jobs matching this document filter.")
    selection_group.add_argument(
        '-j', '--job-id',
        type=str,
        nargs='+',
        help="Limit the view to jobs with these job ids.")
    selection_group.add_argument(
        '-i', '--index',
        type=str,
        help="The filename of an index file.")
    parser_view.set_defaults(func=main_view)

    parser_schema = subparsers.add_parser('schema')
    parser_schema.add_argument(
        '-x', '--exclude-const',
        action='store_true',
        help="Exclude state point parameters, which are constant over the "
             "complete project data space.")
    parser_schema.add_argument(
        '-t', '--depth',
        type=int,
        default=0,
        help="A non-zero value will format the schema in a nested representation "
             "up to the specified depth. The default is a flat view (depth=0).")
    parser_schema.add_argument(
        '-p', '--precision',
        type=int,
        help="Round all numerical values up to the given precision.")
    parser_schema.add_argument(
        '-r', '--max-num-range',
        type=int,
        default=5,
        help="The maximum number of entries shown for a value range, defaults to 5.")
    selection_group = parser_schema.add_argument_group('select')
    selection_group.add_argument(
        '-f', '--filter',
        type=str,
        nargs='+',
        help="Detect schema only for jobs that match the state point filter.")
    selection_group.add_argument(
        '-d', '--doc-filter',
        type=str,
        nargs='+',
        help="Detect schema only for jobs that match the document filter.")
    selection_group.add_argument(
        '-j', '--job-id',
        type=str,
        nargs='+',
        help="Detect schema only for jobs with the given job ids.")
    parser_schema.set_defaults(func=main_schema)

    parser_shell = subparsers.add_parser('shell')
    selection_group = parser_shell.add_argument_group(
        'select',
        description="Specify one or more jobs to preset the `jobs` variable as a generator "
                    "over all job handles associated with the given selection. If the selection "
                    "contains only one job, an additional `job` variable is referencing that "
                    "single job, otherwise it is `None`.")
    selection_group.add_argument(
        '-f', '--filter',
        type=str,
        nargs='+',
        help="Reduce selection to jobs that match the given filter.")
    selection_group.add_argument(
        '-d', '--doc-filter',
        type=str,
        nargs='+',
        help="Reduce selection to jobs that match the given document filter.")
    selection_group.add_argument(
        '-j', '--job-id',
        type=str,
        nargs='+',
        help="Reduce selection to jobs that match the given job ids.")
    parser_shell.set_defaults(func=main_shell)

    parser_sync = subparsers.add_parser(
        'sync',
        description="""Use this command to synchronize this project with another project;
similar to the synchronization of two directories with `rsync`.
Data is always copied from the source to the destination.
For example: `signac sync /path/to/other/project -u --all-keys`
means "Synchronize all jobs within this project with those in the other project; overwrite
files if the source files is newer and overwrite all conflicting keys in the project and
job documents."
"""
    )
    parser_sync.add_argument(
        'source',
        help="The root directory of the project that this project should be synchronized with.")
    parser_sync.add_argument(
        'destination',
        nargs='?',
        help="Optional: The root directory of the project that should be modified for "
             "synchronization, defaults to the local project.")
    add_verbosity_argument(parser_sync, default=2)

    sync_group = parser_sync.add_argument_group('copy options')
    sync_group.add_argument(
        '-a', '--archive',
        action='store_true',
        help="archive mode; equivalent to: '-rltpog'")
    sync_group.add_argument(
        '-r', '--recursive',
        action='store_true',
        help="Do not skip sub-directories, but synchronize recursively.")
    sync_group.add_argument(
        '-l', '--links',
        action='store_true',
        help="Copy symbolic links as symbolic links pointing to the original source.")
    sync_group.add_argument(
        '-p', '--perms',
        action='store_true',
        help="Preserve permissions.")
    sync_group.add_argument(
        '-o', '--owner',
        action='store_true',
        help="Preserve owner.")
    sync_group.add_argument(
        '-g', '--group',
        action='store_true',
        help="Preserve group.")
    sync_group.add_argument(
        '-t', '--times',
        action='store_true',
        help="Preserve file modification times (requires -p).")
    sync_group.add_argument(
        '-x', '--exclude',
        type=str,
        nargs='?',
        const='.*',
        help="Exclude all files matching the given pattern. Exclude all files "
             "if this option is provided without any argument.")
    sync_group.add_argument(
        '-I', '--ignore-times',
        action='store_true',
        dest='deep',
        help="Never rely on file meta data such as the size or the modification time "
             "when determining file differences.")
    sync_group.add_argument(
        '--size-only',
        action='store_true',
        help="Ignore modification times during file comparison. Useful when synchronizing "
             "between file systems with different timestamp resolution.")
    sync_group.add_argument(
        '--round-times',
        action='store_true',
        help="Round modification times during file comparison. Useful when synchronizing "
             "between file systems with different timestamp resolution.")
    sync_group.add_argument(
        '-n', '--dry-run',
        action='store_true',
        help="Do not actually execute the synchronization. Increase the output verbosity "
             "to see messages about what would potentially happen.")
    sync_group.add_argument(
        '-u', '--update',
        action='store_true',
        help="Skip files with newer modification time stamp."
             "This is a short-cut for: --strategy=update.")

    strategy_group = parser_sync.add_argument_group('sync strategy')
    strategy_group.add_argument(
        '-s', '--strategy',
        type=str,
        choices=FileSync.keys(),
        help="Specify a synchronization strategy, for differing files.")
    strategy_group.add_argument(
        '-k', '--key',
        type=str,
        help="Specify a regular expression for keys that should be overwritten "
             "as part of the project and job document synchronization.")
    strategy_group.add_argument(
        '--all-keys',
        action='store_true',
        help="Overwrite all conflicting keys. Equivalent to `--key='.*'`.")
    strategy_group.add_argument(
        '--no-keys',
        action='store_true',
        help="Never overwrite any conflicting keys.")

    parser_sync.add_argument(
        '-w', '--allow-workspace',
        action='store_true',
        help="Allow the specification of a workspace (instead of a project) directory "
             "as the destination path.")
    parser_sync.add_argument(
        '--force',
        action='store_true',
        help="Ignore all warnings, just synchronize.")
    parser_sync.add_argument(
        '--parallel',
        type=int,
        nargs='?',
        const=True,
        help="Use multiple threads for synchronization."
             "You may optionally specify how many threads to "
             "use, otherwise all available processing units will be utilized.")
    parser_sync.add_argument(
        '--stats',
        action='store_true',
        help="Provide file transfer statistics.")
    parser_sync.add_argument(
        '-H', '--human-readable',
        action='store_true',
        help="Provide statistics with human readable formatting.")
    parser_sync.add_argument(
        '--json',
        action='store_true',
        help="Print statistics in JSON formatting.")

    selection_group = parser_sync.add_argument_group('select')
    selection_group.add_argument(
        '-f', '--filter',
        type=str,
        nargs='+',
        help="Only synchronize jobs that match the state point filter.")
    selection_group.add_argument(
        '-d', '--doc-filter',
        type=str,
        nargs='+',
        help="Only synchronize jobs that match the document filter.")
    selection_group.add_argument(
        '-j', '--job-id',
        type=str,
        nargs='+',
        help="Only synchronize jobs with the given job ids.")
    parser_sync.set_defaults(func=main_sync)

    parser_import = subparsers.add_parser(
        'import',
        description="""Import an existing dataset into this project. Optionally provide a file path
 based schema to specify the state point metadata. Providing a path based schema is only necessary
 if the data set was not previously exported from a signac project.""")
    parser_import.add_argument(
        'origin',
        default='.',
        nargs='?',
        help="The origin to import from. May be a path to a directory, a zipfile, or a tarball. "
             "Defaults to the current working directory.")
    parser_import.add_argument(
        'schema_path',
        nargs='?',
        help="Specify an optional import path, such as 'foo/{foo:int}'. Possible type definitions "
             "include bool, int, float, and str. The type is assumed to be 'str' if no type is "
             "specified.")
    parser_import.add_argument(
        '--move',
        action='store_true',
        help="Move the data upon import instead of copying. Can only be used when importing from "
             "a directory.")
    parser_import.add_argument(
        '--sync',
        action='store_true',
        help="Attempt recursive synchronization with default arguments.")
    parser_import.add_argument(
        '--sync-interactive',
        action='store_true',
        help="Synchronize the project with the origin data space interactively.")
    parser_import.set_defaults(func=main_import)

    parser_export = subparsers.add_parser(
        'export',
        description="""Export the project data space (or a subset) to a directory, a zipfile,
 or a tarball.""")
    parser_export.add_argument(
        'target',
        help="The target to export to. May be a path to a directory, a zipfile, or a tarball.",
    )
    parser_export.add_argument(
        'schema_path',
        nargs='?',
        help="Specify an optional export path, based on the job state point, e.g., "
             "'foo/{job.sp.foo}'.")
    parser_export.add_argument(
        '--move',
        action='store_true',
        help="Move data to export target instead of copying. Can only be used when exporting "
             "to a directory target.")
    selection_group = parser_export.add_argument_group('select')
    selection_group.add_argument(
        '-f', '--filter',
        type=str,
        nargs='+',
        help="Limit the jobs to export to those matching the state point filter.")
    selection_group.add_argument(
        '-d', '--doc-filter',
        type=str,
        nargs='+',
        help="Limit the jobs to export to those matching this document filter.")
    selection_group.add_argument(
        '-j', '--job-id',
        type=str,
        nargs='+',
        help="Limit the jobs to export to those matching the provided job ids.")
    parser_export.set_defaults(func=main_export)

    parser_update_cache = subparsers.add_parser(
        'update-cache',
        description="""Use this command to update the project's persistent state point cache.
This feature is still experimental and may be removed in future versions.""")
    parser_update_cache.set_defaults(func=main_update_cache)

    parser_config = subparsers.add_parser('config')
    parser_config.add_argument(
        '-g', '--global',
        dest='globalcfg',
        action='store_true',
        help="Modify the global configuration.")
    parser_config.add_argument(
        '-l', '--local',
        action='store_true',
        help="Modify the local configuration.")
    parser_config.add_argument(
        '-f', '--force',
        action='store_true',
        help="Skip sanity checks when modifying the configuration.")
    config_subparsers = parser_config.add_subparsers()

    parser_show = config_subparsers.add_parser('show')
    parser_show.add_argument(
        'key',
        type=str,
        nargs='*',
        help="The key(s) to show, omit to show the full configuration.")
    parser_show.set_defaults(func=main_config_show)

    parser_set = config_subparsers.add_parser('set')
    parser_set.add_argument(
        'key',
        type=str,
        help="The key to modify.")
    parser_set.add_argument(
        'value',
        type=str,
        nargs='*',
        help="The value to set key to.")
    parser_set.add_argument(
        '-f', '--force',
        action='store_true',
        help="Override any validation warnings.")
    parser_set.set_defaults(func=main_config_set)

    parser_host = config_subparsers.add_parser('host')
    parser_host.add_argument(
        'hostname',
        type=str,
        help="The name of the specified resource. "
             "Note: The name can be arbitrarily chosen.")
    parser_host.add_argument(
        'uri',
        type=str,
        nargs='?',
        help="Set the URI of the specified resource, for "
             "example: 'mongodb://localhost'.")
    parser_host.add_argument(
        '-u', '--username',
        type=str,
        help="Set the username for this resource.")
    parser_host.add_argument(
        '-p', '--password',
        type=str,
        nargs='?',
        const=True,
        help="Store a password for the specified resource.")
    parser_host.add_argument(
        '--update-pw',
        type=str,
        nargs='?',
        const=True,
        choices=PW_ENCRYPTION_SCHEMES,
        help="Update the password of the specified resource. "
             "Use in combination with -p/--password to store the "
             "new password. You can optionally specify the hashing "
             "algorithm used for the password encryption. Anything "
             "else but 'None' requires passlib! (default={})".format(
                 DEFAULT_PW_ENCRYPTION_SCHEME))
    parser_host.add_argument(
        '--show-pw',
        action='store_true',
        help="Show the password if it was stored and exit.")
    parser_host.add_argument(
        '-r', '--remove',
        action='store_true',
        help="Remove the specified resource.")
    parser_host.add_argument(
        '--test',
        action='store_true',
        help="Attempt connecting to the specified host.")
    parser_host.set_defaults(func=main_config_host)

    parser_verify = config_subparsers.add_parser('verify')
    parser_verify.set_defaults(func=main_config_verify)

    # This is a hack, as argparse itself does not
    # allow to parse only --version without any
    # of the other required arguments.
    if '--version' in sys.argv:
        print('signac', __version__)
        sys.exit(0)

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        log_level = logging.DEBUG if args.debug else [
            logging.CRITICAL, logging.ERROR,
            logging.WARNING, logging.INFO,
            logging.MORE, logging.DEBUG][min(args.verbosity, 5)]
        logging.basicConfig(level=log_level)

    if not hasattr(args, 'func'):
        parser.print_usage()
        sys.exit(2)
    try:
        args.func(args)
    except KeyboardInterrupt:
        _print_err()
        _print_err("Interrupted.")
        if args.debug:
            raise
        sys.exit(1)
    except RuntimeWarning as warning:
        _print_err("Warning: {}".format(warning))
        if args.debug:
            raise
        sys.exit(1)
    except Exception as error:
        _print_err('Error: {}'.format(error))
        if args.debug:
            raise
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()